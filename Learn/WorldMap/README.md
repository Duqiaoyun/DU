# World Map 记忆工具

个人用世界地图可视化工具，用于记忆全球国家和地区的位置、名称、简写。

## 使用

双击 `index.html` 在 Chrome / Edge 打开即可。所有状态（主题、视图、记忆进度）自动保存在浏览器 localStorage，换浏览器或清缓存会丢失。

## 操作

- **拖拽地图**：旋转地球（3D）/ 平移地图（2D）
- **滚轮**：缩放
- **点击国家**：弹出浮层显示名字，三选一评估
  - ✅ 记对了：国家变绿
  - ❌ 没记住：国家变红
  - 跳过：不计入统计

## 界面

- **顶栏**：主题切换、重置进度
- **左栏**：视图切换（3D/2D）、显示开关（中/英/ISO）、进度统计

## 开发

只有生成 `data/names.json` 需要一次 Node（已提交完成品，一般不用重跑）：

    node scripts/build-names.mjs > data/names.json

所有逻辑在 `index.html`，修改后浏览器刷新即可。

## 数据源

- 地理边界：[world-atlas](https://github.com/topojson/world-atlas)（基于 Natural Earth 1:110m，公共领域）
- 国名字典：手写于 `scripts/build-names.mjs`，基于 ISO 3166-1 numeric 编码
