#!/usr/bin/env python3
"""
科创金融数据抓取系统 - 主程序
自动抓取科创板、VC投资、政策数据，统一输出JSON格式
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from scrapers.base_scraper import DataMerger
from scrapers.market_scraper import MarketScraper
from scrapers.vc_scraper import VCScraper
from scrapers.policy_scraper import PolicyScraper


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('crawler.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class SciTechFinanceCrawler:
    """科创金融数据抓取系统"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """初始化爬虫系统"""
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / 'data' / 'raw'
        
        self.data_dir: Path = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化各模块抓取器
        self.market_scraper = MarketScraper(self.data_dir / 'market')
        self.vc_scraper = VCScraper(self.data_dir / 'vc')
        self.policy_scraper = PolicyScraper(self.data_dir / 'policy')
        
        # 数据合并器
        self.merger = DataMerger(self.data_dir / 'merged')
        
        self.today = datetime.now().strftime('%Y-%m-%d')
        
    def run_all(self) -> Dict[str, Any]:
        """运行所有抓取任务"""
        logger.info("=" * 80)
        logger.info("科创金融数据抓取系统启动")
        logger.info("=" * 80)
        
        results = {
            'date': self.today,
            'market': [],
            'vc': [],
            'policy': [],
            'total_count': 0
        }
        
        # 1. 抓取科创板数据
        try:
            logger.info("\n[1/3] 开始抓取科创板数据...")
            market_items = self.market_scraper.run()
            results['market'] = [item.to_dict() for item in market_items]
            results['total_count'] += len(market_items)
            
            # 保存
            self.market_scraper.save_to_json()
            self.market_scraper.save_to_ndjson()
            self.merger.add_items(market_items)
            
            logger.info(f"✓ 科创板数据抓取完成: {len(market_items)} 条")
            
        except Exception as e:
            logger.error(f"✗ 科创板数据抓取失败: {e}")
        
        # 2. 抓取VC投资数据
        try:
            logger.info("\n[2/3] 开始抓取VC投资数据...")
            vc_items = self.vc_scraper.run()
            results['vc'] = [item.to_dict() for item in vc_items]
            results['total_count'] += len(vc_items)
            
            # 保存
            self.vc_scraper.save_to_json()
            self.vc_scraper.save_to_ndjson()
            self.merger.add_items(vc_items)
            
            logger.info(f"✓ VC投资数据抓取完成: {len(vc_items)} 条")
            
        except Exception as e:
            logger.error(f"✗ VC投资数据抓取失败: {e}")
        
        # 3. 抓取政策数据
        try:
            logger.info("\n[3/3] 开始抓取政策数据...")
            policy_items = self.policy_scraper.run()
            results['policy'] = [item.to_dict() for item in policy_items]
            results['total_count'] += len(policy_items)
            
            # 保存
            self.policy_scraper.save_to_json()
            self.policy_scraper.save_to_ndjson()
            self.merger.add_items(policy_items)
            
            logger.info(f"✓ 政策数据抓取完成: {len(policy_items)} 条")
            
        except Exception as e:
            logger.error(f"✗ 政策数据抓取失败: {e}")
        
        # 4. 合并数据
        try:
            logger.info("\n[4/4] 合并所有数据...")
            self.merger.deduplicate()
            
            # 保存合并后的数据
            merged_file = self.merger.save_all(self.today)
            type_files = self.merger.save_by_type(self.today)
            
            results['merged_file'] = str(merged_file)
            results['type_files'] = {k: str(v) for k, v in type_files.items()}
            
            logger.info(f"✓ 数据合并完成")
            logger.info(f"  - 合并文件: {merged_file}")
            logger.info(f"  - 分类文件: {type_files}")
            
        except Exception as e:
            logger.error(f"✗ 数据合并失败: {e}")
        
        # 5. 生成统计报告
        report = self.generate_report(results)
        results['report'] = report
        
        # 保存统计报告
        self.save_report(report)
        
        logger.info("=" * 80)
        logger.info(f"数据抓取全部完成！总计: {results['total_count']} 条")
        logger.info("=" * 80)
        
        return results
    
    def generate_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """生成抓取报告"""
        report = {
            'date': self.today,
            'summary': {
                'total_items': results['total_count'],
                'market_items': len(results.get('market', [])),
                'vc_items': len(results.get('vc', [])),
                'policy_items': len(results.get('policy', []))
            },
            'sources': {}
        }
        
        # 统计各来源数据量
        all_items = (results.get('market', []) + 
                    results.get('vc', []) + 
                    results.get('policy', []))
        
        for item in all_items:
            source = item.get('source', 'Unknown')
            report['sources'][source] = report['sources'].get(source, 0) + 1
        
        return report
    
    def save_report(self, report: Dict[str, Any]):
        """保存报告"""
        report_file = self.data_dir / 'reports' / f'crawler_report_{self.today}.json'
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"报告已保存: {report_file}")
        
        # 同时保存最新报告
        latest_report_file = self.data_dir / 'reports' / 'latest_report.json'
        with open(latest_report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report_file
    
    def run_single(self, scraper_type: str) -> List[Any]:
        """运行单个抓取器"""
        if scraper_type == 'market':
            return self.market_scraper.run()
        elif scraper_type == 'vc':
            return self.vc_scraper.run()
        elif scraper_type == 'policy':
            return self.policy_scraper.run()
        else:
            raise ValueError(f"未知的抓取器类型: {scraper_type}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='科创金融数据抓取系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python crawler.py                    # 运行所有抓取器
  python crawler.py --type market      # 只抓取科创板数据
  python crawler.py --type vc          # 只抓取VC投资数据
  python crawler.py --type policy      # 只抓取政策数据
        """
    )
    
    parser.add_argument(
        '--type',
        choices=['market', 'vc', 'policy', 'all'],
        default='all',
        help='选择要运行的抓取器类型 (默认: all)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='指定输出目录 (默认: data/raw)'
    )
    
    args = parser.parse_args()
    
    # 初始化爬虫系统
    data_dir = Path(args.output) if args.output else None
    crawler = SciTechFinanceCrawler(data_dir)
    
    # 运行抓取
    if args.type == 'all':
        results = crawler.run_all()
        
        # 打印摘要
        print("\n" + "=" * 80)
        print("抓取结果摘要")
        print("=" * 80)
        print(f"日期: {results['date']}")
        print(f"总计: {results['total_count']} 条数据")
        print(f"  - 科创板: {len(results['market'])} 条")
        print(f"  - VC投资: {len(results['vc'])} 条")
        print(f"  - 政策: {len(results['policy'])} 条")
        print(f"\n合并文件: {results.get('merged_file', 'N/A')}")
        print("=" * 80)
        
    else:
        items = crawler.run_single(args.type)
        print(f"\n抓取完成: {len(items)} 条数据")
        
        # 保存
        if args.type == 'market':
            crawler.market_scraper.save_to_json()
        elif args.type == 'vc':
            crawler.vc_scraper.save_to_json()
        elif args.type == 'policy':
            crawler.policy_scraper.save_to_json()


if __name__ == '__main__':
    main()
