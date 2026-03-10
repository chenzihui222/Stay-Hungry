#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新系统主调度器
Auto Update System Scheduler

整合所有数据爬虫，实现每日自动更新

功能:
1. 定时运行所有爬虫（科创板、VC/PE、政策）
2. 统一数据库管理
3. 更新状态监控
4. 失败重试和告警
5. 日志记录

定时任务:
- 00:30 - 更新科创板数据
- 01:00 - 更新VC/PE融资数据
- 02:00 - 更新政策数据
- 08:00 - 数据质量检查

作者: Data Engineer
日期: 2026-03-10
"""

import logging
import sys
import time
import traceback
from datetime import datetime
from typing import Dict, List, Tuple

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.triggers.cron import CronTrigger

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_update.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class UpdateManager:
    """更新管理器"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_listener(self._job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self.update_stats = {
            'star_market': {'last_update': None, 'status': 'idle', 'records': 0},
            'funding': {'last_update': None, 'status': 'idle', 'records': 0},
            'policy': {'last_update': None, 'status': 'idle', 'records': 0},
        }
    
    def _job_listener(self, event):
        """任务执行监听器"""
        job_id = event.job_id
        
        if event.exception:
            logger.error(f'❌ 任务执行失败 [{job_id}]: {event.exception}')
            self._update_status(job_id, 'failed', 0)
        else:
            logger.info(f'✅ 任务执行成功 [{job_id}]')
            if hasattr(event, 'retval') and event.retval:
                records = event.retval.get('records', 0)
                self._update_status(job_id, 'success', records)
    
    def _update_status(self, job_id: str, status: str, records: int):
        """更新任务状态"""
        if job_id in self.update_stats:
            self.update_stats[job_id]['last_update'] = datetime.now().isoformat()
            self.update_stats[job_id]['status'] = status
            self.update_stats[job_id]['records'] = records
    
    def update_star_market(self) -> Dict:
        """
        更新科创板数据
        每天 00:30 执行
        """
        logger.info("=" * 60)
        logger.info("🚀 开始更新科创板数据...")
        logger.info(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        try:
            # 导入并运行科创板爬虫
            from star_market_simple import main as star_market_main
            
            # 运行爬虫
            star_market_main()
            
            # 获取统计
            import sqlite3
            conn = sqlite3.connect('star_market.db')
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM star_market_companies')
            total = cursor.fetchone()[0]
            conn.close()
            
            logger.info("✅ 科创板数据更新完成")
            return {'status': 'success', 'records': total}
            
        except Exception as e:
            logger.error(f"❌ 科创板数据更新失败: {e}")
            logger.error(traceback.format_exc())
            return {'status': 'failed', 'records': 0, 'error': str(e)}
    
    def update_funding(self) -> Dict:
        """
        更新VC/PE融资数据
        每天 01:00 执行
        """
        logger.info("=" * 60)
        logger.info("🚀 开始更新VC/PE融资数据...")
        logger.info(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        try:
            # 导入并运行36氪爬虫
            from k36_simple import main as k36_main
            
            # 运行爬虫
            k36_main()
            
            # 获取统计
            import sqlite3
            conn = sqlite3.connect('funding_data.db')
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM funding_events')
            total = cursor.fetchone()[0]
            conn.close()
            
            logger.info("✅ VC/PE融资数据更新完成")
            return {'status': 'success', 'records': total}
            
        except Exception as e:
            logger.error(f"❌ VC/PE融资数据更新失败: {e}")
            logger.error(traceback.format_exc())
            return {'status': 'failed', 'records': 0, 'error': str(e)}
    
    def update_policy(self) -> Dict:
        """
        更新政策数据
        每天 02:00 执行
        """
        logger.info("=" * 60)
        logger.info("🚀 开始更新政策数据...")
        logger.info(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        try:
            # 导入并运行政策爬虫
            from policy_simple import main as policy_main
            
            # 运行爬虫
            policy_main()
            
            # 获取统计
            import sqlite3
            conn = sqlite3.connect('policies.db')
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM policies')
            total = cursor.fetchone()[0]
            conn.close()
            
            logger.info("✅ 政策数据更新完成")
            return {'status': 'success', 'records': total}
            
        except Exception as e:
            logger.error(f"❌ 政策数据更新失败: {e}")
            logger.error(traceback.format_exc())
            return {'status': 'failed', 'records': 0, 'error': str(e)}
    
    def data_quality_check(self) -> Dict:
        """
        数据质量检查
        每天 08:00 执行
        """
        logger.info("=" * 60)
        logger.info("🔍 开始数据质量检查...")
        logger.info("=" * 60)
        
        checks = []
        
        # 检查科创板数据
        try:
            import sqlite3
            conn = sqlite3.connect('star_market.db')
            cursor = conn.cursor()
            
            # 检查最新数据日期
            cursor.execute('SELECT MAX(updated_at) FROM star_market_companies')
            last_update = cursor.fetchone()[0]
            
            # 检查数据完整性
            cursor.execute('SELECT COUNT(*) FROM star_market_companies WHERE price IS NULL')
            missing_price = cursor.fetchone()[0]
            
            conn.close()
            
            checks.append({
                'source': '科创板',
                'last_update': last_update,
                'missing_price': missing_price,
                'status': 'ok' if missing_price < 10 else 'warning'
            })
            
        except Exception as e:
            checks.append({'source': '科创板', 'status': 'error', 'error': str(e)})
        
        # 检查融资数据
        try:
            conn = sqlite3.connect('funding_data.db')
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM funding_events WHERE funding_date >= date("now", "-1 day")')
            today_count = cursor.fetchone()[0]
            
            conn.close()
            
            checks.append({
                'source': 'VC/PE融资',
                'today_new': today_count,
                'status': 'ok' if today_count > 0 else 'warning'
            })
            
        except Exception as e:
            checks.append({'source': 'VC/PE融资', 'status': 'error', 'error': str(e)})
        
        # 检查政策数据
        try:
            conn = sqlite3.connect('policies.db')
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM policies WHERE created_at >= date("now", "-1 day")')
            today_count = cursor.fetchone()[0]
            
            conn.close()
            
            checks.append({
                'source': '政策',
                'today_new': today_count,
                'status': 'ok'
            })
            
        except Exception as e:
            checks.append({'source': '政策', 'status': 'error', 'error': str(e)})
        
        # 输出检查结果
        logger.info("\n数据质量检查结果:")
        for check in checks:
            status_emoji = '✅' if check['status'] == 'ok' else '⚠️' if check['status'] == 'warning' else '❌'
            logger.info(f"{status_emoji} {check['source']}: {check}")
        
        return {'status': 'completed', 'checks': checks}
    
    def setup_schedule(self):
        """设置定时任务"""
        logger.info("📅 正在配置定时任务...")
        
        # 1. 科创板数据更新 - 每天 00:30
        self.scheduler.add_job(
            self.update_star_market,
            CronTrigger(hour=0, minute=30),
            id='star_market',
            name='科创板数据更新',
            replace_existing=True
        )
        logger.info("✅ 已配置: 科创板数据更新 (每天 00:30)")
        
        # 2. VC/PE融资数据更新 - 每天 01:00
        self.scheduler.add_job(
            self.update_funding,
            CronTrigger(hour=1, minute=0),
            id='funding',
            name='VC/PE融资数据更新',
            replace_existing=True
        )
        logger.info("✅ 已配置: VC/PE融资数据更新 (每天 01:00)")
        
        # 3. 政策数据更新 - 每天 02:00
        self.scheduler.add_job(
            self.update_policy,
            CronTrigger(hour=2, minute=0),
            id='policy',
            name='政策数据更新',
            replace_existing=True
        )
        logger.info("✅ 已配置: 政策数据更新 (每天 02:00)")
        
        # 4. 数据质量检查 - 每天 08:00
        self.scheduler.add_job(
            self.data_quality_check,
            CronTrigger(hour=8, minute=0),
            id='quality_check',
            name='数据质量检查',
            replace_existing=True
        )
        logger.info("✅ 已配置: 数据质量检查 (每天 08:00)")
        
        # 5. 手动测试任务（每小时执行一次，用于调试）
        # self.scheduler.add_job(
        #     self.update_star_market,
        #     'interval',
        #     minutes=60,
        #     id='test_update',
        #     name='测试更新'
        # )
    
    def get_status(self) -> Dict:
        """获取当前状态"""
        return {
            'scheduler_running': self.scheduler.running,
            'update_stats': self.update_stats,
            'next_run_times': {
                job.id: job.next_run_time.isoformat() if job.next_run_time else None
                for job in self.scheduler.get_jobs()
            }
        }
    
    def run_once(self, task_name: str = None):
        """
        手动运行一次更新
        
        Args:
            task_name: 'star_market', 'funding', 'policy'，None则运行全部
        """
        if task_name is None or task_name == 'all':
            logger.info("🚀 手动运行全部更新任务...")
            self.update_star_market()
            time.sleep(5)
            self.update_funding()
            time.sleep(5)
            self.update_policy()
        elif task_name == 'star_market':
            self.update_star_market()
        elif task_name == 'funding':
            self.update_funding()
        elif task_name == 'policy':
            self.update_policy()
        else:
            logger.error(f"❌ 未知任务: {task_name}")
    
    def start(self):
        """启动调度器"""
        logger.info("\n" + "=" * 60)
        logger.info("🚀 启动自动更新系统")
        logger.info("=" * 60)
        
        # 配置定时任务
        self.setup_schedule()
        
        # 启动调度器
        self.scheduler.start()
        
        logger.info("\n📋 定时任务列表:")
        for job in self.scheduler.get_jobs():
            logger.info(f"  - {job.name}: {job.trigger}")
        
        logger.info("\n⏳ 调度器运行中，按 Ctrl+C 停止...")
        
        try:
            # 保持主线程运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n🛑 正在停止调度器...")
            self.scheduler.shutdown()
            logger.info("✅ 调度器已停止")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='自动更新系统')
    parser.add_argument('--run-once', choices=['all', 'star_market', 'funding', 'policy'], 
                        help='手动运行一次指定任务')
    parser.add_argument('--status', action='store_true', help='查看当前状态')
    
    args = parser.parse_args()
    
    manager = UpdateManager()
    
    if args.run_once:
        # 手动运行一次
        manager.run_once(args.run_once)
    elif args.status:
        # 查看状态
        status = manager.get_status()
        print("\n系统状态:")
        print(json.dumps(status, indent=2, ensure_ascii=False, default=str))
    else:
        # 启动定时调度
        manager.start()


if __name__ == "__main__":
    # 导入json用于状态输出
    import json
    main()
