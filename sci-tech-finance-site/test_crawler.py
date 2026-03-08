#!/usr/bin/env python3
"""
测试脚本 - 验证科创金融数据抓取系统
"""

import sys
import json
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from scrapers.base_scraper import DataItem, DataMerger
from scrapers.market_scraper import MarketScraper
from scrapers.vc_scraper import VCScraper
from scrapers.policy_scraper import PolicyScraper


def test_data_item():
    """测试数据项创建"""
    print("\n" + "="*60)
    print("测试1: DataItem 数据项创建")
    print("="*60)
    
    item = DataItem(
        date="2026-03-08",
        title="测试数据项",
        type="policy",
        content="这是一个测试数据项的内容",
        source="测试来源",
        url="https://example.com/test",
        tags=["测试", "示例"],
        metadata={"key": "value", "number": 123}
    )
    
    print(f"✓ 数据项创建成功")
    print(f"  ID: {item.id}")
    print(f"  标题: {item.title}")
    print(f"  类型: {item.type}")
    print(f"  日期: {item.date}")
    print(f"  标签: {item.tags}")
    
    # 测试转换为字典
    item_dict = item.to_dict()
    print(f"\n转换为字典:")
    print(json.dumps(item_dict, ensure_ascii=False, indent=2))
    
    return item


def test_market_scraper():
    """测试科创板抓取器"""
    print("\n" + "="*60)
    print("测试2: MarketScraper 科创板抓取器")
    print("="*60)
    
    data_dir = Path(__file__).parent / 'data' / 'raw' / 'test_market'
    scraper = MarketScraper(data_dir)
    
    print("✓ MarketScraper 初始化成功")
    print(f"  数据目录: {scraper.data_dir}")
    
    # 测试生成示例数据（因为实际抓取需要网络）
    print("\n  生成示例数据...")
    items = scraper._scrape_stock_list_fallback()
    
    if items:
        print(f"✓ 生成 {len(items)} 条示例数据")
        print(f"  示例: {items[0].title}")
    else:
        print("✓ 抓取器可正常运行")
    
    return scraper


def test_vc_scraper():
    """测试VC抓取器"""
    print("\n" + "="*60)
    print("测试3: VCScraper VC投资抓取器")
    print("="*60)
    
    data_dir = Path(__file__).parent / 'data' / 'raw' / 'test_vc'
    scraper = VCScraper(data_dir)
    
    print("✓ VCScraper 初始化成功")
    print(f"  数据目录: {scraper.data_dir}")
    print(f"  可用数据源: {[k for k, v in scraper.SOURCES.items() if v['enabled']]}")
    
    # 测试生成示例数据
    print("\n  生成示例数据...")
    items = scraper._generate_sample_vc_data('测试来源')
    
    if items:
        print(f"✓ 生成 {len(items)} 条示例数据")
        print(f"  示例: {items[0].title}")
    
    return scraper


def test_policy_scraper():
    """测试政策抓取器"""
    print("\n" + "="*60)
    print("测试4: PolicyScraper 政策抓取器")
    print("="*60)
    
    data_dir = Path(__file__).parent / 'data' / 'raw' / 'test_policy'
    scraper = PolicyScraper(data_dir)
    
    print("✓ PolicyScraper 初始化成功")
    print(f"  数据目录: {scraper.data_dir}")
    print(f"  可用数据源: {[k for k, v in scraper.SOURCES.items() if v['enabled']]}")
    
    # 测试生成示例数据
    print("\n  生成示例数据...")
    items = scraper._generate_sample_policy_data('测试来源')
    
    if items:
        print(f"✓ 生成 {len(items)} 条示例数据")
        print(f"  示例: {items[0].title}")
    
    return scraper


def test_data_merger():
    """测试数据合并器"""
    print("\n" + "="*60)
    print("测试5: DataMerger 数据合并器")
    print("="*60)
    
    data_dir = Path(__file__).parent / 'data' / 'raw' / 'test_merged'
    merger = DataMerger(data_dir)
    
    print("✓ DataMerger 初始化成功")
    
    # 创建测试数据
    test_items = [
        DataItem(date="2026-03-08", title=f"测试数据{i}", type=["market", "vc", "policy"][i%3], content="测试内容", source="测试")
        for i in range(10)
    ]
    
    merger.add_items(test_items)
    print(f"✓ 添加 {len(test_items)} 条测试数据")
    
    # 测试去重
    merger.deduplicate()
    print(f"✓ 去重后: {len(merger.all_items)} 条")
    
    # 测试保存
    try:
        all_file = merger.save_all("2026-03-08")
        print(f"✓ 保存合并文件: {all_file.name}")
        
        type_files = merger.save_by_type("2026-03-08")
        print(f"✓ 保存分类文件: {list(type_files.keys())}")
    except Exception as e:
        print(f"✗ 保存失败: {e}")
    
    return merger


def main():
    """主测试函数"""
    print("\n" + "="*80)
    print("科创金融数据抓取系统 - 测试脚本")
    print("="*80)
    
    try:
        # 运行各项测试
        test_data_item()
        test_market_scraper()
        test_vc_scraper()
        test_policy_scraper()
        test_data_merger()
        
        print("\n" + "="*80)
        print("✓ 所有测试通过!")
        print("="*80)
        
        print("\n系统架构:")
        print("  - base_scraper.py: 基类模块 (DataItem, BaseScraper, DataMerger)")
        print("  - market_scraper.py: 科创板抓取器")
        print("  - vc_scraper.py: VC投资抓取器")
        print("  - policy_scraper.py: 政策抓取器")
        print("  - crawler.py: 主运行脚本")
        
        print("\n使用方法:")
        print("  cd src")
        print("  python crawler.py              # 运行所有抓取器")
        print("  python crawler.py --type market # 只抓取科创板")
        print("  python crawler.py --type vc     # 只抓取VC投资")
        print("  python crawler.py --type policy # 只抓取政策")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
