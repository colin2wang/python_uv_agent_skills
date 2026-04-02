# HTML格式指南与分页控制

本文档提供HTML转PDF的格式规范、CSS分页控制方法和常见问题解决方案。

## 目录
- [HTML基本结构](#html基本结构)
- [CSS引用方式](#css引用方式)
- [分页控制](#分页控制)
- [页眉页脚设置](#页眉页脚设置)
- [中文支持](#中文支持)
- [常见问题](#常见问题)

## HTML基本结构

### 标准HTML5模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文档标题</title>
    
    <!-- 外部CSS -->
    <link rel="stylesheet" href="styles.css">
    
    <!-- CDN CSS库 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- 内嵌样式 -->
    <style>
        body {
            font-family: 'SimSun', serif;
            line-height: 1.6;
        }
        
        @media print {
            .no-print {
                display: none;
            }
        }
    </style>
</head>
<body>
    <h1>文档标题</h1>
    
    <div class="content">
        <p>内容段落...</p>
    </div>
</body>
</html>
```

### 关键要素

- **DOCTYPE声明**：必须使用`<!DOCTYPE html>`
- **字符编码**：通过`<meta charset="UTF-8">`指定
- **语言属性**：设置`<html lang="zh-CN">`支持中文

## CSS引用方式

### 1. 外部CSS文件

```html
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="./css/print.css">
```

**注意事项**：
- 使用相对路径或绝对路径
- 确保CSS文件可访问
- 支持多个CSS文件同时引用

### 2. CDN引用

```html
<!-- Bootstrap -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Tailwind CSS -->
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@3.3.0/dist/tailwind.min.css" rel="stylesheet">

<!-- Font Awesome -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
```

**注意事项**：
- 需要网络连接
- 转换速度可能较慢
- 建议离线环境使用本地CSS

### 3. 内嵌样式

```html
<style>
    body {
        font-family: 'Microsoft YaHei', sans-serif;
        margin: 0;
        padding: 0;
    }
    
    h1 {
        color: #333;
        page-break-after: avoid;
    }
    
    table {
        page-break-inside: avoid;
    }
</style>
```

### 4. 内联样式

```html
<div style="color: red; font-size: 16px;">
    内联样式内容
</div>
```

## 分页控制

### CSS分页属性

WeasyPrint支持以下CSS分页属性：

#### 1. page-break-before

控制元素前的分页行为。

```css
/* 强制在此元素前分页 */
.section {
    page-break-before: always;
}

/* 避免在此元素前分页 */
h2 {
    page-break-before: avoid;
}

/* 左页/右页（用于双面打印） */
.chapter {
    page-break-before: left;
}
```

#### 2. page-break-after

控制元素后的分页行为。

```css
/* 标题后不分页 */
h1, h2, h3 {
    page-break-after: avoid;
}

/* 章节结束后分页 */
.chapter {
    page-break-after: always;
}
```

#### 3. page-break-inside

控制元素内部是否允许分页。

```css
/* 表格内不允许分页 */
table {
    page-break-inside: avoid;
}

/* 图片内不允许分页 */
img {
    page-break-inside: avoid;
}

/* 代码块内不允许分页 */
pre {
    page-break-inside: avoid;
}
```

### 分页控制示例

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        /* 每个章节强制分页 */
        .chapter {
            page-break-before: always;
        }
        
        /* 标题和内容不分页 */
        h1, h2, h3 {
            page-break-after: avoid;
        }
        
        /* 表格整体不分页 */
        table {
            page-break-inside: avoid;
        }
        
        /* 图片不分页 */
        img {
            page-break-inside: avoid;
            max-width: 100%;
        }
        
        /* 段落不被截断 */
        p {
            orphans: 3;  /* 页底至少保留3行 */
            widows: 3;   /* 页首至少保留3行 */
        }
    </style>
</head>
<body>
    <h1>第一章</h1>
    <p>章节内容...</p>
    
    <div class="chapter">
        <h1>第二章</h1>
        <p>章节内容...</p>
    </div>
    
    <div class="chapter">
        <h1>第三章</h1>
        <p>章节内容...</p>
    </div>
</body>
</html>
```

## 页眉页脚设置

### 使用CSS @page规则

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: A4;
            margin: 2.5cm;
            
            /* 页眉 */
            @top-center {
                content: "文档标题";
                font-size: 10pt;
                color: #666;
            }
            
            /* 页脚 */
            @bottom-center {
                content: "第 " counter(page) " 页 / 共 " counter(pages) " 页";
                font-size: 10pt;
                color: #666;
            }
            
            /* 首页不显示页眉页脚 */
            @page :first {
                @top-center {
                    content: none;
                }
            }
        }
    </style>
</head>
<body>
    <h1>文档内容</h1>
    <p>...</p>
</body>
</html>
```

### 使用HTML元素作为页眉页脚

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            @top-center {
                content: element(header);
            }
            @bottom-center {
                content: element(footer);
            }
        }
        
        #header {
            position: running(header);
        }
        
        #footer {
            position: running(footer);
        }
    </style>
</head>
<body>
    <!-- 页眉 -->
    <div id="header">
        <span>文档标题</span>
        <span style="float: right;">公司名称</span>
    </div>
    
    <!-- 页脚 -->
    <div id="footer">
        <span>第 <span class="page-number"></span> 页</span>
    </div>
    
    <!-- 文档内容 -->
    <h1>正文内容</h1>
    <p>...</p>
</body>
</html>
```

## 中文支持

### 字体设置

```css
body {
    /* 优先使用系统中文字体 */
    font-family: 
        'Microsoft YaHei',      /* Windows */
        'PingFang SC',          /* macOS */
        'Source Han Sans CN',   /* 思源黑体 */
        'SimSun',               /* 宋体 */
        sans-serif;
}

/* 标题字体 */
h1, h2, h3 {
    font-family: 
        'Microsoft YaHei',
        'PingFang SC',
        sans-serif;
}
```

### 使用@font-face加载字体

```css
@font-face {
    font-family: 'MyChineseFont';
    src: url('./fonts/SourceHanSansCN-Regular.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
}

body {
    font-family: 'MyChineseFont', sans-serif;
}
```

## 常见问题

### 1. CSS样式未生效

**原因**：
- CSS文件路径错误
- CSS选择器优先级不足
- 外部CSS无法访问

**解决方案**：
```html
<!-- 使用绝对路径或正确的相对路径 -->
<link rel="stylesheet" href="./css/styles.css">

<!-- 提高选择器优先级 -->
<style>
    body .content p {
        color: red !important;
    }
</style>
```

### 2. 分页位置不理想

**解决方案**：
```css
/* 明确指定分页点 */
.page-break {
    page-break-before: always;
}

/* 避免不当分页 */
h1, h2, h3, h4, h5, h6 {
    page-break-after: avoid;
}

table, figure, img {
    page-break-inside: avoid;
}
```

### 3. 中文显示为方块或乱码

**原因**：系统缺少中文字体

**解决方案**：
```css
/* 方法1：指定系统字体 */
body {
    font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
}

/* 方法2：嵌入字体文件 */
@font-face {
    font-family: 'ChineseFont';
    src: url('./fonts/MyFont.ttf');
}
```

### 4. 图片未显示

**原因**：
- 图片路径错误
- 图片格式不支持

**解决方案**：
```html
<!-- 使用相对路径 -->
<img src="./images/photo.jpg" alt="照片">

<!-- 使用绝对路径 -->
<img src="/full/path/to/image.jpg" alt="照片">

<!-- 使用Base64编码 -->
<img src="data:image/png;base64,iVBORw0KGgoAAAANS..." alt="图片">
```

### 5. 表格跨页被截断

**解决方案**：
```css
table {
    page-break-inside: avoid;
}

/* 如果表格太长无法避免，可以允许内部跨页但保持表头 */
thead {
    display: table-header-group;
}

tfoot {
    display: table-footer-group;
}
```

### 6. 外部CSS加载失败

**原因**：网络问题或CDN不可访问

**解决方案**：
```html
<!-- 优先使用本地CSS -->
<link rel="stylesheet" href="./css/bootstrap.min.css">

<!-- 离线环境备用方案 -->
<script>
    // 检测CSS是否加载
    if (!document.styleSheets.length) {
        console.warn('CSS加载失败，使用内联样式');
    }
</script>
```

## 最佳实践

### 1. 打印友好设计

```css
@media print {
    /* 隐藏不必要的元素 */
    .no-print, .nav, .sidebar {
        display: none;
    }
    
    /* 调整颜色 */
    body {
        color: black;
        background: white;
    }
    
    /* 显示链接URL */
    a[href]:after {
        content: " (" attr(href) ")";
    }
    
    /* 避免分页 */
    h1, h2, h3 {
        page-break-after: avoid;
    }
}
```

### 2. 响应式布局

```css
/* 使用百分比或相对单位 */
.container {
    width: 100%;
    max-width: 210mm;  /* A4宽度 */
}

/* 避免固定像素值 */
.content {
    padding: 5%;
    font-size: 12pt;
}
```

### 3. 性能优化

```html
<!-- 压缩CSS文件 -->
<link rel="stylesheet" href="./css/styles.min.css">

<!-- 合并多个CSS文件 -->
<link rel="stylesheet" href="./css/all.css">

<!-- 避免过多外部资源 -->
<style>
    /* 内嵌关键CSS */
</style>
```
