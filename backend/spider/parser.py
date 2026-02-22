import re
from datetime import datetime, time


class GuessParser:
    """竞猜内容解析器"""
    
    # 关键词匹配
    GUESS_KEYWORDS = ['对弈竞猜', '对弈', '竞猜']
    
    # 预测结果匹配模式
    PREDICTION_PATTERNS = {
        'left': [
            r'左[边侧]?', r'红[色方]?', r'左边赢', r'红方赢',
            r'压左', r'押左', r'选左', r'投左',
            r'左边胜', r'红方胜', r'左胜', r'红胜',
            r'我红', r'压红', r'押红', r'选红', r'投红',  # 直接表达
            r'left'  # 红蓝转换后的匹配
        ],
        'right': [
            r'右[边侧]?', r'蓝[色方]?', r'右边赢', r'蓝方赢',
            r'压右', r'押右', r'选右', r'投右',
            r'右边胜', r'蓝方胜', r'右胜', r'蓝胜',
            r'我蓝', r'压蓝', r'押蓝', r'选蓝', r'投蓝',  # 直接表达
            r'right'  # 红蓝转换后的匹配
        ]
    }
    
    # 红蓝转换映射（按长度降序，避免部分替换）
    COLOR_MAPPING = {
        '红色': 'left',
        '蓝色': 'right',
        '红方': 'left',
        '蓝方': 'right',
        '红': 'left',
        '蓝': 'right'
    }
    
    @classmethod
    def is_guess_related(cls, content):
        """
        判断是否包含对弈竞猜相关内容
        支持：对弈竞猜关键词 或 左/右/红/蓝预测关键字
        
        Args:
            content: 微博内容
            
        Returns:
            bool: 是否相关
        """
        if not content:
            return False
            
        content_lower = content.lower()
        
        # 检查是否包含对弈竞猜关键词
        for keyword in cls.GUESS_KEYWORDS:
            if keyword in content_lower:
                return True
        
        # 检查是否包含预测关键字（左/右/红/蓝）
        # 简单匹配：单独出现的左、右、红、蓝
        prediction_keywords = ['左', '右', '红', '蓝']
        for keyword in prediction_keywords:
            if keyword in content:
                return True
                
        return False
    
    @classmethod
    def parse_prediction(cls, content):
        """
        解析预测结果(左/右)
        
        Args:
            content: 微博内容
            
        Returns:
            str: 'left', 'right', 或 'unknown'
        """
        if not content:
            return 'unknown'
        
        # 检查是否同时包含红、蓝、翻盘中任意2个或更多
        # 如果同时存在多个冲突信号，需要人工判断
        conflict_keywords = ['红', '蓝', '翻盘']
        found_count = 0
        for keyword in conflict_keywords:
            if keyword in content:
                found_count += 1
        
        # 如果找到2个或更多冲突关键词，返回unknown需要人工判断
        if found_count >= 2:
            return 'unknown'
        
        left_score = 0
        right_score = 0
        
        # 第一步：先匹配包含"我蓝"、"压蓝"、"我红"、"压红"等直接表达（最高权重）
        direct_patterns = {
            'left': [r'我红', r'压红', r'押红', r'选红', r'投红'],
            'right': [r'我蓝', r'压蓝', r'押蓝', r'选蓝', r'投蓝']
        }
        
        for pattern in direct_patterns['left']:
            if re.search(pattern, content, re.IGNORECASE):
                left_score += 10  # 直接表达权重最高
                
        for pattern in direct_patterns['right']:
            if re.search(pattern, content, re.IGNORECASE):
                right_score += 10  # 直接表达权重最高
        
        # 如果已经有直接表达的结果，直接返回（避免后续干扰）
        if left_score > right_score:
            return 'left'
        elif right_score > left_score:
            return 'right'
        
        # 第二步：进行红蓝转换后匹配其他模式
        converted_content = cls._convert_colors(content)
        
        # 统计左右匹配次数（排除已经匹配过的直接表达模式）
        other_left_patterns = [p for p in cls.PREDICTION_PATTERNS['left'] if p not in direct_patterns['left']]
        other_right_patterns = [p for p in cls.PREDICTION_PATTERNS['right'] if p not in direct_patterns['right']]
        
        for pattern in other_left_patterns:
            matches = re.findall(pattern, converted_content, re.IGNORECASE)
            left_score += len(matches)
            
        for pattern in other_right_patterns:
            matches = re.findall(pattern, converted_content, re.IGNORECASE)
            right_score += len(matches)
        
        # 判断结果
        if left_score > right_score:
            return 'left'
        elif right_score > left_score:
            return 'right'
        else:
            return 'unknown'
    
    @classmethod
    def _convert_colors(cls, content):
        """
        将红蓝转换为左右
        
        Args:
            content: 原始内容
            
        Returns:
            str: 转换后的内容
        """
        for color, side in cls.COLOR_MAPPING.items():
            content = content.replace(color, side)
        return content
    
    @classmethod
    def parse_guess_round(cls, publish_time, content=None):
        """
        根据发布时间推断竞猜轮次
        
        竞猜时间: 10:00, 12:00, 14:00, 16:00, 18:00, 20:00, 22:00
        博主预测发布时间: 竞猜开始后的任意时间
        
        轮次判断逻辑:
        - 10:00-11:59 发布的 -> 第1轮 (10:00竞猜)
        - 12:00-13:59 发布的 -> 第2轮 (12:00竞猜)
        - 14:00-15:59 发布的 -> 第3轮 (14:00竞猜)
        - 以此类推...
        
        Args:
            publish_time: 发布时间(datetime对象)
            content: 微博内容(可选，用于辅助判断)
            
        Returns:
            int: 轮次(1-7)，无法判断返回None
        """
        if not publish_time:
            return None
            
        hour = publish_time.hour
        minute = publish_time.minute
        
        # 根据发布时间判断轮次
        # 发布时间落在哪个竞猜时间段，就是第几轮
        # 10:00-11:59 -> 第1轮
        # 12:00-13:59 -> 第2轮
        # 14:00-15:59 -> 第3轮
        # 16:00-17:59 -> 第4轮
        # 18:00-19:59 -> 第5轮
        # 20:00-21:59 -> 第6轮
        # 22:00-23:59 -> 第7轮
        
        if 10 <= hour < 12:
            return 1
        elif 12 <= hour < 14:
            return 2
        elif 14 <= hour < 16:
            return 3
        elif 16 <= hour < 18:
            return 4
        elif 18 <= hour < 20:
            return 5
        elif 20 <= hour < 22:
            return 6
        elif 22 <= hour < 24:
            return 7
        
        # 如果不在上述时间段，返回None
        return None
    
    @classmethod
    def parse_guess_date(cls, publish_time):
        """
        获取竞猜日期
        
        Args:
            publish_time: 发布时间
            
        Returns:
            date: 竞猜日期
        """
        if not publish_time:
            return None
            
        # 如果是23:30之后发布的，属于当天的竞猜
        # 如果是00:00-01:30发布的，属于前一天的竞猜(第7轮)
        if publish_time.hour < 2:
            # 跨天的第7轮，日期算前一天
            from datetime import timedelta
            return (publish_time - timedelta(days=1)).date()
        
        return publish_time.date()
    
    @classmethod
    def parse_weibo(cls, weibo_data):
        """
        解析微博数据
        
        Args:
            weibo_data: 微博原始数据字典
            
        Returns:
            dict: 解析后的数据
        """
        content = weibo_data.get('content', '')
        publish_time = weibo_data.get('publish_time')
        
        is_related = cls.is_guess_related(content)
        prediction = cls.parse_prediction(content) if is_related else 'unknown'
        guess_round = cls.parse_guess_round(publish_time, content) if is_related else None
        guess_date = cls.parse_guess_date(publish_time) if is_related else None
        
        return {
            'is_guess_related': is_related,
            'guess_prediction': prediction,
            'guess_round': guess_round,
            'guess_date': guess_date,
            'parsed_content': content
        }
