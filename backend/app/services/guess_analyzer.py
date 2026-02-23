from datetime import datetime, date
from sqlalchemy import func, case as sql_case
from app.models import db, Blogger, WeiboPost, OfficialResult, BloggerStats


class GuessAnalyzerService:
    """竞猜分析服务"""
    
    @classmethod
    def analyze_daily_guesses(cls, target_date=None):
        """
        分析指定日期的竞猜结果
        
        Args:
            target_date: 目标日期，默认为今天
            
        Returns:
            dict: 分析结果
        """
        if target_date is None:
            target_date = date.today()
        
        # 获取当天的官方结果
        official_results = OfficialResult.query.filter_by(guess_date=target_date).all()
        official_map = {r.guess_round: r.result for r in official_results}
        
        # 获取当天所有博主的预测（不再限制is_guess_related）
        blogger_predictions = WeiboPost.query.filter_by(
            guess_date=target_date
        ).all()
        
        # 按博主分组统计
        results = {}
        for pred in blogger_predictions:
            blogger_id = pred.blogger_id
            if blogger_id not in results:
                results[blogger_id] = {
                    'blogger_id': blogger_id,
                    'blogger_nickname': pred.blogger.nickname if pred.blogger else '未知',
                    'predictions': [],
                    'correct': 0,
                    'wrong': 0,
                    'unknown': 0
                }
            
            # 判断预测是否正确
            official_result = official_map.get(pred.guess_round)
            if official_result:
                if pred.guess_prediction == 'unknown':
                    status = 'unknown'
                    results[blogger_id]['unknown'] += 1
                elif pred.guess_prediction == official_result:
                    status = 'correct'
                    results[blogger_id]['correct'] += 1
                else:
                    status = 'wrong'
                    results[blogger_id]['wrong'] += 1
            else:
                status = 'pending'  # 官方结果未录入
            
            results[blogger_id]['predictions'].append({
                'round': pred.guess_round,
                'prediction': pred.guess_prediction,
                'official_result': official_result,
                'status': status,
                'content': pred.content[:100] + '...' if len(pred.content) > 100 else pred.content
            })
        
        # 计算准确率
        for blogger_id, data in results.items():
            valid_guesses = data['correct'] + data['wrong']
            if valid_guesses > 0:
                data['accuracy_rate'] = round((data['correct'] / valid_guesses) * 100, 2)
            else:
                data['accuracy_rate'] = 0.00
        
        # 按准确率由高到低排序
        sorted_results = sorted(results.values(), key=lambda x: x['accuracy_rate'], reverse=True)
        
        return {
            'date': target_date.strftime('%Y-%m-%d'),
            'total_rounds': len(official_results),
            'blogger_count': len(results),
            'results': sorted_results
        }
    
    @classmethod
    def get_blogger_stats(cls, blogger_id, start_date=None, end_date=None):
        """
        获取博主统计信息
        
        Args:
            blogger_id: 博主ID
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            dict: 统计信息
        """
        blogger = Blogger.query.get(blogger_id)
        if not blogger:
            return None
        
        # 构建查询
        query = db.session.query(
            func.count(WeiboPost.id).label('total'),
            func.sum(sql_case((WeiboPost.guess_prediction == 'left', 1), (WeiboPost.guess_prediction == 'right', 1), else_=0)).label('valid'),
            func.sum(sql_case((OfficialResult.result == WeiboPost.guess_prediction, 1), else_=0)).label('correct')
        ).join(
            OfficialResult,
            (WeiboPost.guess_date == OfficialResult.guess_date) & 
            (WeiboPost.guess_round == OfficialResult.guess_round)
        ).filter(
            WeiboPost.blogger_id == blogger_id
            # 不再限制is_guess_related
        )
        
        if start_date:
            query = query.filter(WeiboPost.guess_date >= start_date)
        if end_date:
            query = query.filter(WeiboPost.guess_date <= end_date)
        
        result = query.first()
        
        total = result.total or 0
        valid = result.valid or 0
        correct = result.correct or 0
        wrong = valid - correct
        
        accuracy = round((correct / valid) * 100, 2) if valid > 0 else 0.00
        
        return {
            'blogger_id': blogger_id,
            'blogger_nickname': blogger.nickname,
            'total_guesses': total,
            'valid_guesses': valid,
            'correct_guesses': correct,
            'wrong_guesses': wrong,
            'accuracy_rate': accuracy,
            'start_date': start_date.strftime('%Y-%m-%d') if start_date else None,
            'end_date': end_date.strftime('%Y-%m-%d') if end_date else None
        }
    
    @classmethod
    def get_leaderboard(cls, date_range='7d'):
        """
        获取博主排行榜
        
        Args:
            date_range: 时间范围(7d/30d/all)
            
        Returns:
            list: 排行榜数据
        """
        from datetime import timedelta
        
        end_date = date.today()
        if date_range == '7d':
            start_date = end_date - timedelta(days=7)
        elif date_range == '30d':
            start_date = end_date - timedelta(days=30)
        else:
            start_date = None
        
        # 获取所有博主
        bloggers = Blogger.query.filter_by(is_active=True).all()
        
        leaderboard = []
        for blogger in bloggers:
            stats = cls.get_blogger_stats(blogger.id, start_date, end_date)
            if stats and stats['valid_guesses'] > 0:
                leaderboard.append(stats)
        
        # 按准确率排序
        leaderboard.sort(key=lambda x: x['accuracy_rate'], reverse=True)
        
        # 添加排名
        for i, item in enumerate(leaderboard):
            item['rank'] = i + 1
        
        return leaderboard
    
    @classmethod
    def update_daily_stats(cls, target_date=None):
        """
        更新每日统计
        
        Args:
            target_date: 目标日期
            
        Returns:
            int: 更新的记录数
        """
        if target_date is None:
            target_date = date.today()
        
        # 获取当天分析结果
        analysis = cls.analyze_daily_guesses(target_date)
        
        count = 0
        for result in analysis['results']:
            blogger_id = result['blogger_id']
            
            # 查找或创建统计记录
            stat = BloggerStats.query.filter_by(
                blogger_id=blogger_id,
                stat_date=target_date
            ).first()
            
            if not stat:
                stat = BloggerStats(
                    blogger_id=blogger_id,
                    stat_date=target_date
                )
                db.session.add(stat)
            
            # 更新统计
            stat.total_guesses = len(result['predictions'])
            stat.correct_guesses = result['correct']
            stat.wrong_guesses = result['wrong']
            stat.unknown_guesses = result['unknown']
            stat.calculate_accuracy()
            
            count += 1
        
        db.session.commit()
        return count
