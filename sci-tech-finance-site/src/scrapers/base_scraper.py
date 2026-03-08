#!/usr/bin/env python3
"""
科创金融数据抓取系统 - 基类模块
提供统一的数据抓取接口和JSON输出格式
"""

import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import hashlib

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class DataItem:
    """统一数据项格式"""
    
    def __init__(
        self,
        date: str,
        title: str,
        type: str,  # 'policy', 'vc', 'market'
        content: str,
        source: str,
        url: str = "",
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.date = date
        self.title = title
        self.type = type
        self.content = content
        self.source = source
        self.url = url
        self.tags: List[str] = tags if tags is not None else []
        self.metadata: Dict[str, Any] = metadata if metadata is not None else {}
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """生成唯一ID"""
        content_str = f"{self.date}_{self.title}_{self.source}"
        return hashlib.md5(content_str.encode()).hexdigest()[:12]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'id': self.id,
            'date': self.date,
            'title': self.title,
            'type': self.type,
            'content': self.content,
            'source': self.source,
            'url': self.url,
            'tags': self.tags,
            'metadata': self.metadata,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DataItem':
        """从字典创建对象"""
        item = cls(
            date=data['date'],
            title=data['title'],
            type=data['type'],
            content=data['content'],
            source=data['source'],
            url=data.get('url', ''),
            tags=data.get('tags', []),
            metadata=data.get('metadata', {})
        )
        item.id = data.get('id', item._generate_id())
        item.created_at = data.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return item


class BaseScraper(ABC):
    """数据抓取器基类"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.logger = logging.getLogger(self.__class__.__name__)
        self.items: List[DataItem] = []
        
    @abstractmethod
    def scrape(self) -> List[DataItem]:
        """执行抓取操作，返回数据项列表"""
        pass
    
    def save_to_json(self, filename: Optional[str] = None) -> Path:
        """保存数据到JSON文件"""
        if filename is None:
            filename = f"{self.__class__.__name__.lower()}_{self.today}.json"
        
        output_file = self.data_dir / filename
        
        data = {
            'scraper_type': self.__class__.__name__,
            'scrape_date': self.today,
            'total_items': len(self.items),
            'items': [item.to_dict() for item in self.items]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"数据已保存: {output_file} ({len(self.items)} 条)")
        return output_file
    
    def save_to_ndjson(self, filename: Optional[str] = None) -> Path:
        """保存为NDJSON格式（每行一个JSON对象）"""
        if filename is None:
            filename = f"{self.__class__.__name__.lower()}_{self.today}.ndjson"
        
        output_file = self.data_dir / filename
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in self.items:
                f.write(json.dumps(item.to_dict(), ensure_ascii=False) + '\n')
        
        self.logger.info(f"NDJSON数据已保存: {output_file} ({len(self.items)} 条)")
        return output_file
    
    def load_from_json(self, filepath: Path) -> List[DataItem]:
        """从JSON文件加载数据"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.items = [DataItem.from_dict(item) for item in data.get('items', [])]
        self.logger.info(f"已加载 {len(self.items)} 条数据")
        return self.items
    
    def deduplicate(self) -> int:
        """去重，返回去重后的数量"""
        seen_ids = set()
        unique_items = []
        
        for item in self.items:
            if item.id not in seen_ids:
                seen_ids.add(item.id)
                unique_items.append(item)
        
        removed = len(self.items) - len(unique_items)
        self.items = unique_items
        
        if removed > 0:
            self.logger.info(f"去重完成: 移除 {removed} 条重复数据")
        
        return len(self.items)
    
    def filter_by_date(self, start_date: str, end_date: str) -> List[DataItem]:
        """按日期范围过滤"""
        filtered = [
            item for item in self.items
            if start_date <= item.date <= end_date
        ]
        return filtered
    
    def run(self) -> List[DataItem]:
        """运行抓取流程"""
        self.logger.info(f"{'='*60}")
        self.logger.info(f"开始运行 {self.__class__.__name__}")
        self.logger.info(f"{'='*60}")
        
        try:
            self.items = self.scrape()
            self.deduplicate()
            
            self.logger.info(f"{'='*60}")
            self.logger.info(f"抓取完成: 共 {len(self.items)} 条数据")
            self.logger.info(f"{'='*60}")
            
            return self.items
            
        except Exception as e:
            self.logger.error(f"抓取失败: {e}")
            raise


class DataMerger:
    """数据合并器"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.all_items: List[DataItem] = []
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def add_items(self, items: List[DataItem]):
        """添加数据项"""
        self.all_items.extend(items)
        self.logger.info(f"添加 {len(items)} 条数据，当前总计 {len(self.all_items)} 条")
    
    def deduplicate(self) -> int:
        """全局去重"""
        seen_ids = set()
        unique_items = []
        
        for item in self.all_items:
            if item.id not in seen_ids:
                seen_ids.add(item.id)
                unique_items.append(item)
        
        removed = len(self.all_items) - len(unique_items)
        self.all_items = unique_items
        
        self.logger.info(f"全局去重: 移除 {removed} 条重复，剩余 {len(self.all_items)} 条")
        return len(self.all_items)
    
    def save_all(self, date_str: Optional[str] = None) -> Path:
        """保存所有合并后的数据"""
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        output_file = self.data_dir / f'all_data_{date_str}.json'
        
        # 按类型和日期排序
        sorted_items = sorted(
            self.all_items,
            key=lambda x: (x.type, x.date),
            reverse=True
        )
        
        data = {
            'export_date': date_str,
            'total_items': len(sorted_items),
            'type_summary': self._get_type_summary(),
            'source_summary': self._get_source_summary(),
            'items': [item.to_dict() for item in sorted_items]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"合并数据已保存: {output_file}")
        return output_file
    
    def save_by_type(self, date_str: Optional[str] = None) -> Dict[str, Path]:
        """按类型分别保存"""
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        type_files = {}
        
        for item_type in ['policy', 'vc', 'market']:
            items = [item for item in self.all_items if item.type == item_type]
            
            if items:
                output_file = self.data_dir / f'{item_type}_data_{date_str}.json'
                
                data = {
                    'export_date': date_str,
                    'type': item_type,
                    'total_items': len(items),
                    'items': [item.to_dict() for item in items]
                }
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                type_files[item_type] = output_file
                self.logger.info(f"{item_type} 数据已保存: {output_file} ({len(items)} 条)")
        
        return type_files
    
    def _get_type_summary(self) -> Dict[str, int]:
        """获取类型统计"""
        summary = {}
        for item in self.all_items:
            summary[item.type] = summary.get(item.type, 0) + 1
        return summary
    
    def _get_source_summary(self) -> Dict[str, int]:
        """获取来源统计"""
        summary = {}
        for item in self.all_items:
            summary[item.source] = summary.get(item.source, 0) + 1
        return summary


if __name__ == '__main__':
    # 测试代码
    print("科创金融数据抓取基类模块")
    print("=" * 60)
    
    # 创建示例数据项
    item = DataItem(
        date="2026-03-08",
        title="测试数据",
        type="policy",
        content="这是一条测试数据内容",
        source="测试来源",
        tags=["测试", "示例"],
        metadata={"key": "value"}
    )
    
    print(f"示例数据项:")
    print(json.dumps(item.to_dict(), ensure_ascii=False, indent=2))
