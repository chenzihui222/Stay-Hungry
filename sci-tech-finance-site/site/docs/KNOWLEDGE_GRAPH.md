# 研究知识图谱使用文档

## 📋 功能概述

研究知识图谱可视化展示了研究报告、研究笔记和标签之间的关系网络。

## 🎯 功能特性

### 节点类型

| 类型 | 颜色 | 形状 | 说明 |
|------|------|------|------|
| 🔵 研究报告 | 深蓝色 | 圆形 | 系统内的研究报告 |
| 🟢 研究笔记 | 绿色 | 圆形 | 用户创建的研究笔记 |
| 🟠 标签 | 橙色 | 方形 | 笔记的关键词标签 |

### 关系类型

- **报告 → 笔记**：实线箭头，表示笔记来源于某篇报告
- **笔记 → 标签**：虚线箭头，表示笔记包含该标签

## 🚀 使用方法

### 1. 访问知识图谱

1. 进入"研究笔记"页面
2. 点击顶部的"学习图谱"标签
3. 点击"知识图谱"按钮（默认为学习热力图）

### 2. 交互操作

| 操作 | 效果 |
|------|------|
| **点击节点** | 显示节点详细信息面板 |
| **拖拽节点** | 调整节点位置 |
| **双击空白处** | 关闭信息面板 |
| **滚轮缩放** | 放大/缩小图谱 |
| **拖拽画布** | 移动视图 |

### 3. 控制按钮

- **🔄 重置布局**：重新计算图谱布局
- **⛶ 适应屏幕**：将图谱适应到容器大小

### 4. 节点信息面板

点击任意节点会显示：

**报告节点：**
- 类型
- 分类
- 发布时间
- 查看报告链接

**笔记节点：**
- 类型
- 关联的报告
- 标签列表

**标签节点：**
- 类型
- 关联的笔记数量

## 🗂️ 数据结构

### 示例数据格式

```javascript
// 报告节点
{
    id: 'r1',
    label: '科创板IPO分析',
    type: 'report',
    date: '2026-03-08',
    category: '科创板',
    url: 'report-viewer.html?file=r1.md'
}

// 笔记节点
{
    id: 'n1',
    label: '笔记-科创板观察',
    type: 'note',
    reportId: 'r1',  // 关联的报告ID
    tags: ['科创板', 'IPO']
}

// 标签节点
{
    id: 't1',
    label: '科创板',
    type: 'tag'
}

// 边（关系）
{
    id: 'e-r1-n1',
    source: 'r1',
    target: 'n1',
    type: 'report-note'  // 报告到笔记
}

{
    id: 'e-n1-t1',
    source: 'n1',
    target: 't1',
    type: 'note-tag'  // 笔记到标签
}
```

## 🔧 技术实现

### 使用的库

- **Cytoscape.js** (v3.26.0)：强大的网络图可视化库
- **COSE 布局**：Compound Spring Embedder，自动排列节点

### 核心代码

```javascript
// 初始化图谱
cy = cytoscape({
    container: document.getElementById('cy'),
    elements: graphData,
    style: [...],
    layout: {
        name: 'cose',
        ...
    }
});

// 添加事件监听
cy.on('tap', 'node', function(evt) {
    showNodeInfo(evt.target);
});
```

### 样式配置

```javascript
// 报告节点样式
{
    selector: 'node[type="report"]',
    style: {
        'background-color': '#1e3a5f',
        'width': 50,
        'height': 50,
        ...
    }
}

// 笔记节点样式
{
    selector: 'node[type="note"]',
    style: {
        'background-color': '#10b981',
        'width': 40,
        'height': 40,
        ...
    }
}

// 标签节点样式
{
    selector: 'node[type="tag"]',
    style: {
        'background-color': '#f59e0b',
        'shape': 'rectangle',
        ...
    }
}
```

## 🎨 自定义样式

### 修改节点颜色

编辑 CSS 部分：

```css
/* 报告节点颜色 */
.legend-node.report-node {
    background: #1e3a5f;
}

/* 笔记节点颜色 */
.legend-node.note-node {
    background: #10b981;
}

/* 标签节点颜色 */
.legend-node.tag-node {
    background: #f59e0b;
}
```

### 修改节点大小

编辑 JavaScript：

```javascript
// 报告节点
'width': 60,  // 修改大小
'height': 60,

// 笔记节点
'width': 50,
'height': 50,
```

## 📊 未来扩展

### 1. 连接真实数据

目前使用示例数据，未来可以连接：

```javascript
function generateGraphData() {
    const data = [];
    
    // 从 localStorage 获取笔记
    const savedNotes = localStorage.getItem('stayHungryNotes_' + currentUser.id);
    const notes = savedNotes ? JSON.parse(savedNotes) : [];
    
    // 从 ReportsData 获取报告
    const reports = ReportsData.reports;
    
    // 构建节点和边...
    
    return data;
}
```

### 2. 添加更多交互

- **搜索高亮**：搜索节点并高亮显示
- **路径分析**：显示两个节点之间的最短路径
- **聚类分析**：自动识别知识社群
- **时间轴**：按时间维度查看知识演变

### 3. 导出功能

```javascript
// 导出为图片
cy.png({
    bg: 'white',
    full: true,
    scale: 2
});

// 导出为 JSON
const json = cy.json();
```

## 🐛 故障排查

### 图谱不显示

**检查：**
1. 浏览器控制台是否有错误
2. Cytoscape.js 是否正确加载
3. 容器元素是否存在

### 节点重叠

**解决：**
```javascript
layout: {
    name: 'cose',
    nodeOverlap: 20,  // 减小重叠
    nodeRepulsion: 400000,  // 增加斥力
    ...
}
```

### 性能问题

**优化：**
1. 限制节点数量（分页加载）
2. 使用 WebGL 渲染（cy.js 3.0+）
3. 减少动画效果

## 📚 参考资料

- [Cytoscape.js 官方文档](https://js.cytoscape.org/)
- [COSE 布局算法](https://github.com/cytoscape/cytoscape.js-cose)
- [网络图可视化最佳实践](https://medium.com/@d3noob)

## 🎉 总结

现在你可以：
1. ✅ 可视化研究报告和笔记的关系网络
2. ✅ 通过颜色快速识别不同类型的节点
3. ✅ 点击节点查看详细信息
4. ✅ 拖拽调整布局
5. ✅ 缩放和移动视图

知识图谱让研究工作更加直观和高效！
