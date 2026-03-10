#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务调度器 - 每日自动更新政策数据

使用 APScheduler 实现定时任务
"""

import logging
import sys
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

# 导入爬虫
from policy_simple import main as policy_crawler_main

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def job_listener(event):
    """任务执行监听器"""
    if event.exception:
        logger.error(f'任务执行出错: {event.job_id}')
    else:
        logger.info(f'任务执行成功: {event.job_id}')


def daily_policy_update():
    """每日政策更新任务"""
    logger.info("=" * 60)
    logger.info("执行每日政策数据更新...")
    logger.info(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        policy_crawler_main()
        logger.info("✅ 每日政策更新完成")
    except Exception as e:
        logger.error(f"❌ 每日政策更新失败: {e}", exc_info=True)


def main():
    """主函数 - 启动调度器"""
    logger.info("🚀 启动定时任务调度器...")
    
    scheduler = BlockingScheduler()
    
    # 添加任务监听器
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    
    # 添加每日政策更新任务
    # 每天 09:00 执行
    scheduler.add_job(
        daily_policy_update,
        'cron',
        hour=9,
        minute=0,
        id='daily_policy_update',
        name='每日政策数据更新',
        replace_existing=True
    )
    
    # 添加测试任务（每5分钟执行一次，用于调试）
    # scheduler.add_job(
    #     daily_policy_update,
    #     'interval',
    #     minutes=5,
    #     id='test_policy_update',
    #     name='测试-政策数据更新'
    # )
    
    logger.info("📅 定时任务已配置:")
    logger.info("  - 每日 09:00 自动更新政策数据")
    logger.info("\n⏳ 调度器运行中，按 Ctrl+C 停止...")
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("\n🛑 调度器已停止")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
