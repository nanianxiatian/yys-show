from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from app.models import SystemConfig
from .weibo_spider import WeiboSpiderService
from .guess_analyzer import GuessAnalyzerService


class SchedulerService:
    """定时任务调度服务"""
    
    _instance = None
    _scheduler = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._scheduler = BackgroundScheduler()
            cls._instance.spider_service = None
        return cls._instance
    
    def __init__(self):
        # 确保实例属性存在
        if not hasattr(self, 'spider_service'):
            self.spider_service = None
    
    def _get_spider_service(self):
        """延迟初始化爬虫服务"""
        if self.spider_service is None:
            self.spider_service = WeiboSpiderService()
        return self.spider_service
    
    def start(self):
        """启动调度器"""
        if not SchedulerService._scheduler.running:
            self._add_jobs()
            SchedulerService._scheduler.start()
            print(f"[{datetime.now()}] 定时任务调度器已启动")
    
    def shutdown(self):
        """关闭调度器"""
        if SchedulerService._scheduler.running:
            SchedulerService._scheduler.shutdown()
            print(f"[{datetime.now()}] 定时任务调度器已关闭")
    
    def _add_jobs(self):
        """添加定时任务"""
        # 获取配置（使用try-except防止表不存在时出错）
        try:
            cron_hours = SystemConfig.get_value('spider_cron_hours', '11,13,15,17,19,21,23')
            cron_minute = int(SystemConfig.get_value('spider_cron_minute', '30'))
        except:
            cron_hours = '11,13,15,17,19,21,23'
            cron_minute = 30

        # 添加自动爬虫任务
        # 每天 11:30, 13:30, 15:30, 17:30, 19:30, 21:30, 23:30 执行
        SchedulerService._scheduler.add_job(
            func=self._auto_spider_job,
            trigger=CronTrigger(
                hour=cron_hours,
                minute=cron_minute
            ),
            id='auto_spider',
            name='自动爬取微博',
            replace_existing=True
        )

        # 添加每日统计任务(每天凌晨1点执行)
        SchedulerService._scheduler.add_job(
            func=self._daily_stats_job,
            trigger=CronTrigger(hour=1, minute=0),
            id='daily_stats',
            name='每日统计分析',
            replace_existing=True
        )

        print(f"[{datetime.now()}] 已添加定时任务:")
        print(f"  - 自动爬虫: 每天 {cron_hours.replace(',', ', ')}:{cron_minute:02d}")
        print(f"  - 每日统计: 每天 01:00")
    
    def _auto_spider_job(self):
        """自动爬虫任务"""
        print(f"[{datetime.now()}] 开始执行自动爬虫任务...")

        # 检查是否启用自动爬虫
        try:
            enabled = SystemConfig.get_value('spider_auto_enabled', 'true')
        except:
            enabled = 'true'

        if enabled.lower() != 'true':
            print(f"[{datetime.now()}] 自动爬虫已禁用，跳过")
            return

        try:
            result = self._get_spider_service().spider_all_bloggers(spider_type='auto')
            if result['success']:
                print(f"[{datetime.now()}] 自动爬虫完成: 共爬取 {result['total_posts']} 条微博")
            else:
                print(f"[{datetime.now()}] 自动爬虫失败: {result.get('error')}")
        except Exception as e:
            print(f"[{datetime.now()}] 自动爬虫异常: {str(e)}")
    
    def _daily_stats_job(self):
        """每日统计任务"""
        print(f"[{datetime.now()}] 开始执行每日统计任务...")
        
        try:
            from datetime import date, timedelta
            # 统计昨天的数据
            yesterday = date.today() - timedelta(days=1)
            count = GuessAnalyzerService.update_daily_stats(yesterday)
            print(f"[{datetime.now()}] 每日统计完成: 更新了 {count} 条记录")
        except Exception as e:
            print(f"[{datetime.now()}] 每日统计异常: {str(e)}")
    
    def get_jobs(self):
        """获取所有任务"""
        if not SchedulerService._scheduler or not SchedulerService._scheduler.running:
            return []
        
        jobs = []
        for job in SchedulerService._scheduler.get_jobs():
            # 检查任务是否被暂停
            job_state = SchedulerService._scheduler.get_job(job.id)
            is_paused = job_state.next_run_time is None if job_state else True
            
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run_time': job.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if job.next_run_time else None,
                'trigger': str(job.trigger),
                'paused': is_paused
            })
        return jobs
    
    def pause_job(self, job_id):
        """暂停任务"""
        SchedulerService._scheduler.pause_job(job_id)
    
    def resume_job(self, job_id):
        """恢复任务"""
        SchedulerService._scheduler.resume_job(job_id)
    
    def run_spider_now(self):
        """立即执行爬虫"""
        self._auto_spider_job()
