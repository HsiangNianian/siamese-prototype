# Siamese Prototype 文档

这是 Siamese Prototype 项目的文档目录。

## 构建文档

### 安装依赖

```bash
uv sync --group docs
```

### 构建 HTML 文档

```bash
# 在 docs 目录中
make html

# 或者直接使用 sphinx-build
sphinx-build -b html . _build/html
```

### 开发模式

```bash
# 增量构建，适合开发
make dev

# 启动本地服务器查看文档
make serve
```

## 文档结构

- `index.rst` - 主页面
- `installation.rst` - 安装指南
- `quickstart.rst` - 快速开始
- `user_guide/` - 用户指南
- `api/` - API 参考
- `examples/` - 示例
- `contributing.rst` - 贡献指南

## 主题

文档使用 Furo 主题，这是一个现代化的 Sphinx 主题，提供：

- 响应式设计
- 深色/浅色模式切换
- 优秀的可读性
- 现代化的导航

## 本地开发

1. 安装文档依赖：`uv sync --group docs`
2. 进入 docs 目录：`cd docs`
3. 构建文档：`make html`
4. 查看文档：打开 `_build/html/index.html`

## 部署

文档可以部署到：

- Read the Docs
- GitHub Pages
- 任何静态文件托管服务

## 注意事项

- 所有代码示例都应该是可运行的
- 保持文档与代码同步
- 使用中文编写文档
- 遵循 reStructuredText 语法 