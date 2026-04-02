---
name: html-to-pdf
description: 将HTML文件转换为高质量PDF，支持CSS渲染（包括外部CSS库）和智能分页控制；当用户需要将网页、HTML文档转为PDF或需要保留样式布局时使用
dependency:
  python:
    - weasyprint==60.2
    - pillow==10.2.0
metadata: { "copaw": { "emoji": "📄" } }
---

# HTML转PDF转换器

## 任务目标
- 将HTML文件转换为高质量PDF文档
- 支持完整的CSS渲染，包括外部CSS库（如Bootstrap、Tailwind等）
- 提供智能分页控制，可通过CSS规则精确控制分页行为
- 保留HTML原有的样式、布局和排版

## 前置准备
- 环境要求：Python 3.8+
- 包管理：推荐使用uv管理依赖
  ```bash
  # 使用uv初始化项目
  uv init html-pdf-project
  cd html-pdf-project
  
  # 安装依赖
  uv add weasyprint==60.2 pillow==10.2.0
  ```

- 系统依赖说明：
  - WeasyPrint需要系统级依赖：Pango、Cairo、GObject
  - macOS: `brew install pango cairo`
  - Ubuntu/Debian: `sudo apt-get install libpango-1.0-0 libpangocairo-1.0-0`
  - Windows: 依赖库已打包在weasyprint中，无需额外安装

## 操作步骤

### 1. 准备HTML文件
- 确保HTML文件格式正确，符合标准HTML5规范
- 支持的CSS引用方式：
  - 外部CSS文件：`<link rel="stylesheet" href="styles.css">`
  - CDN引用：`<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">`
  - 内嵌样式：`<style>...</style>`
  - 内联样式：`style="..."`
- 详细的HTML格式要求和分页控制方法，参见 [references/html_format_guide.md](references/html_format_guide.md)

### 2. 执行转换脚本
- 脚本名称：**`scripts/html_to_pdf.py`**
- 基本用法：
  ```bash
  uv run python scripts/html_to_pdf.py input.html
  ```
- 指定输出路径：
  ```bash
  uv run python scripts/html_to_pdf.py input.html --output output.pdf
  ```
- 自定义页面设置：
  ```bash
  uv run python scripts/html_to_pdf.py input.html \
    --page-size A4 \
    --margin "2cm 2cm 2cm 2cm" \
    --output custom.pdf
  ```

### 3. 验证输出结果
- 检查PDF文件是否正确生成
- 验证CSS样式是否正确渲染
- 确认分页位置是否符合预期
- 检查中文字体是否正常显示

## 资源索引
- 转换脚本：[scripts/html_to_pdf.py](scripts/html_to_pdf.py)
  - 用途：执行HTML到PDF的转换
  - 主要参数：input_file（必需）、output（可选）、page-size（可选）、margin（可选）

- 格式参考：[references/html_format_guide.md](references/html_format_guide.md)
  - 何时读取：准备HTML文件时、需要控制分页行为时、配置页眉页脚时
  - 内容：HTML格式规范、CSS分页属性、常见问题解决方案

## 注意事项
- **网络连接**：使用外部CSS库（如CDN）时需要网络连接，离线环境请使用本地CSS文件
- **分页控制**：通过CSS的`@page`规则和`page-break-*`属性控制分页，详见references
- **中文字体**：确保系统安装了中文字体，或通过CSS的`@font-face`指定字体路径
- **复杂布局**：建议在HTML中使用打印友好的CSS媒体查询`@media print`
- **性能优化**：大文件转换可能需要较长时间，建议对大型HTML进行分块处理

## 常见问题
- **CSS未生效**：检查CSS文件路径是否正确，外部CSS是否可访问
- **分页位置不理想**：使用CSS的`page-break-before`、`page-break-after`属性手动控制
- **中文显示为方块**：安装中文字体或在CSS中指定支持中文的字体
- **图片未显示**：检查图片路径，建议使用相对路径或绝对路径，确保可访问
