"""
后台任务管理器
用于管理长时间运行的任务
"""
import threading
import uuid
from datetime import datetime, timedelta
from typing import Dict, Callable, Any

# 全局存储（模块级别，所有线程共享）
_tasks = {}
_app = None
_lock = threading.Lock()


class TaskManager:
    """简单的内存任务管理器"""
    
    @staticmethod
    def init_app(app):
        """初始化 Flask 应用"""
        global _app
        _app = app
    
    @staticmethod
    def create_task(task_type: str, params: dict = None) -> str:
        """创建新任务"""
        task_id = str(uuid.uuid4())
        task = {
            'id': task_id,
            'type': task_type,
            'params': params or {},
            'status': 'pending',  # pending, running, completed, failed
            'progress': 0,
            'result': None,
            'error': None,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'completed_at': None
        }
        with _lock:
            _tasks[task_id] = task
        return task_id
    
    @staticmethod
    def get_task(task_id: str) -> dict:
        """获取任务状态"""
        with _lock:
            task = _tasks.get(task_id)
            # 返回副本，避免外部修改
            return task.copy() if task else None
    
    @staticmethod
    def update_task(task_id: str, **kwargs):
        """更新任务状态"""
        with _lock:
            if task_id in _tasks:
                _tasks[task_id].update(kwargs)
                _tasks[task_id]['updated_at'] = datetime.now()
    
    @staticmethod
    def complete_task(task_id: str, result: Any = None):
        """完成任务"""
        with _lock:
            if task_id in _tasks:
                _tasks[task_id].update({
                    'status': 'completed',
                    'progress': 100,
                    'result': result,
                    'completed_at': datetime.now()
                })
    
    @staticmethod
    def fail_task(task_id: str, error: str):
        """标记任务失败"""
        with _lock:
            if task_id in _tasks:
                _tasks[task_id].update({
                    'status': 'failed',
                    'error': error,
                    'completed_at': datetime.now()
                })
    
    @staticmethod
    def run_task_async(task_id: str, func: Callable, *args, **kwargs):
        """异步运行任务（在 Flask 应用上下文中）"""
        def wrapper():
            global _app
            if _app is None:
                TaskManager.fail_task(task_id, "Flask应用未初始化")
                return
            
            with _app.app_context():
                try:
                    TaskManager.update_task(task_id, status='running')
                    result = func(*args, **kwargs)
                    TaskManager.complete_task(task_id, result)
                except Exception as e:
                    import traceback
                    error_msg = f"{str(e)}\n{traceback.format_exc()}"
                    TaskManager.fail_task(task_id, error_msg)
        
        thread = threading.Thread(target=wrapper, daemon=True)
        thread.start()
        return thread
    
    @staticmethod
    def cleanup_old_tasks(max_age_hours: int = 24):
        """清理旧任务"""
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        with _lock:
            to_remove = [
                task_id for task_id, task in _tasks.items()
                if task['created_at'] < cutoff
            ]
            for task_id in to_remove:
                del _tasks[task_id]


# 保持向后兼容的实例方式
task_manager = TaskManager()
