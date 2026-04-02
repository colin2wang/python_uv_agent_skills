# 常见安全漏洞类型与检查清单

## 目录
1. [SQL 注入](#sql-注入)
2. [XSS 跨站脚本攻击](#xss-跨站脚本攻击)
3. [敏感信息泄露](#敏感信息泄露)
4. [命令注入](#命令注入)
5. [不安全的反序列化](#不安全的反序列化)
6. [路径遍历](#路径遍历)
7. [CSRF 跨站请求伪造](#csrf-跨站请求伪造)
8. [不安全的随机数](#不安全的随机数)
9. [Semgrep 工具使用](#semgrep-工具使用)

## 概览
本文档列出常见的安全漏洞类型、识别特征和检查要点，用于指导代码安全扫描。

## 核心内容

### SQL 注入

**风险等级**：严重

**漏洞描述**：
攻击者通过在输入字段中注入恶意 SQL 代码，操纵数据库查询。

**识别特征**：
- 直接拼接 SQL 语句：`"SELECT * FROM users WHERE name = '" + user_input + "'"`
- 使用字符串格式化构建查询：`f"SELECT * FROM users WHERE id = {user_id}"`
- 未使用参数化查询或 ORM

**检查要点**：
1. 搜索所有数据库查询代码
2. 检查是否使用参数化查询（prepared statements）
3. 验证用户输入是否经过适当的过滤和转义
4. 确认是否使用了 ORM 框架（如 Django ORM、SQLAlchemy）

**修复建议**：
```python
# ❌ 错误：字符串拼接
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# ✅ 正确：参数化查询
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

---

### XSS 跨站脚本攻击

**风险等级**：高危

**漏洞描述**：
攻击者在网页中注入恶意脚本，窃取用户信息或执行恶意操作。

**识别特征**：
- 直接输出用户输入到 HTML：`<div>{{ user_input }}</div>`
- 使用 `innerHTML` 或 `dangerouslySetInnerHTML`
- 未对输出进行 HTML 转义

**检查要点**：
1. 搜索所有输出用户数据的位置
2. 检查是否使用了自动转义的模板引擎
3. 验证是否设置了适当的 Content Security Policy (CSP)
4. 确认对富文本内容进行了过滤（DOMPurify 等）

**修复建议**：
```html
<!-- ❌ 错误：直接输出 -->
<div>{{ user_input }}</div>

<!-- ✅ 正确：自动转义 -->
<div>{{ user_input|escape }}</div>

<!-- 或使用 DOMPurify 过滤富文本 -->
<script>
  const clean = DOMPurify.sanitize(userInput);
  element.innerHTML = clean;
</script>
```

---

### 敏感信息泄露

**风险等级**：严重

**漏洞描述**：
密钥、密码、API Token 等敏感信息硬编码在代码中。

**识别特征**：
- 硬编码密码：`password = "admin123"`
- API 密钥：`api_key = "sk-1234567890"`
- 数据库连接字符串：`connection_string = "mongodb://user:pass@host"`

**检查要点**：
1. 搜索常见敏感关键词：password, secret, key, token, api_key, private_key
2. 检查配置文件和常量定义
3. 验证是否使用环境变量或密钥管理服务
4. 确认敏感信息未被提交到版本控制系统

**修复建议**：
```python
# ❌ 错误：硬编码
api_key = "sk-1234567890abcdef"

# ✅ 正确：使用环境变量
import os
api_key = os.getenv("OPENAI_API_KEY")

# ✅ 或使用密钥管理服务（如 AWS Secrets Manager）
```

---

### 命令注入

**风险等级**：严重

**漏洞描述**：
攻击者通过输入恶意命令，在服务器上执行任意系统命令。

**识别特征**：
- 使用 `os.system()` 执行用户输入：`os.system("ping " + user_input)`
- 使用 `subprocess.call()` 未正确转义：`subprocess.call(["ls", user_input])`
- 使用 `eval()` 或 `exec()` 执行用户代码

**检查要点**：
1. 搜索所有系统命令执行代码
2. 检查是否使用 `subprocess` 的安全调用方式（列表形式）
3. 验证用户输入是否经过白名单验证
4. 确认是否使用 `shlex.quote()` 对参数进行转义

**修复建议**：
```python
# ❌ 错误：字符串拼接
import os
os.system("ls " + user_directory)

# ✅ 正确：使用 subprocess 列表形式
import subprocess
subprocess.run(["ls", user_directory], check=True)

# ✅ 或使用白名单验证
allowed_dirs = ["home", "tmp", "var"]
if user_directory not in allowed_dirs:
    raise ValueError("Invalid directory")
```

---

### 不安全的反序列化

**风险等级**：高危

**漏洞描述**：
反序列化不可信的数据可能导致远程代码执行。

**识别特征**：
- 使用 `pickle.load()` 反序列化用户数据
- 使用不安全的反序列化库（如 Java 的 ObjectInputStream）

**检查要点**：
1. 搜索所有反序列化操作
2. 检查反序列化的数据来源是否可信
3. 验证是否使用了安全的序列化格式（JSON、MessagePack）
4. 确认是否对反序列化对象进行了类型验证

**修复建议**：
```python
# ❌ 错误：反序列化不可信数据
import pickle
data = pickle.loads(user_input)

# ✅ 正确：使用 JSON
import json
data = json.loads(user_input)

# ✅ 或使用安全的序列化库（如 PyYAML 的 safe_load）
import yaml
data = yaml.safe_load(user_input)
```

---

### 路径遍历

**风险等级**：中危

**漏洞描述**：
攻击者通过构造特殊路径访问系统任意文件。

**识别特征**：
- 直接使用用户输入作为文件路径：`open(user_filename)`
- 未验证路径合法性：`os.path.join(base_dir, user_input)`

**检查要点**：
1. 搜索所有文件操作代码
2. 检查是否使用 `os.path.abspath()` 规范化路径
3. 验证路径是否在允许的目录范围内
4. 确认是否限制了文件访问权限

**修复建议**：
```python
import os

# ❌ 错误：直接使用用户输入
with open(user_filename) as f:
    data = f.read()

# ✅ 正确：路径验证
safe_path = os.path.abspath(os.path.join(base_dir, user_filename))
if not safe_path.startswith(os.path.abspath(base_dir)):
    raise ValueError("Invalid path")
with open(safe_path) as f:
    data = f.read()
```

---

### CSRF 跨站请求伪造

**风险等级**：中危

**漏洞描述**：
攻击者诱导用户在已登录的网站上执行非预期操作。

**识别特征**：
- 表单缺少 CSRF Token
- 状态改变操作未验证请求来源

**检查要点**：
1. 搜索所有 POST/PUT/DELETE 请求处理
2. 检查是否使用了 CSRF 保护中间件
3. 验证敏感操作是否验证了 Referer 头
4. 确认是否使用了 SameSite Cookie 属性

**修复建议**：
```python
# ✅ 使用 Django CSRF 保护
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def change_password(request):
    # 表单处理
    pass

# ✅ 或使用 Flask-WTF
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

---

### 不安全的随机数

**风险等级**：低危（特定场景下高危）

**漏洞描述**：
使用可预测的随机数生成器，导致密钥、Token 等可被预测。

**识别特征**：
- 使用 `random.random()` 生成安全相关数据
- 使用时间戳作为随机种子

**检查要点**：
1. 搜索所有随机数生成代码
2. 检查安全敏感场景（Token、密钥生成）是否使用密码学安全的随机数
3. 验证是否使用了 `secrets` 或 `os.urandom()`

**修复建议**：
```python
# ❌ 错误：使用普通随机数生成 Token
import random
token = ''.join(random.choices('0123456789abcdef', k=32))

# ✅ 正确：使用密码学安全的随机数
import secrets
token = secrets.token_hex(32)

# ✅ 或使用 os.urandom()
import os
token = os.urandom(32).hex()
```

## 示例

### 示例 1：Python Web 应用安全扫描
检查以下文件：
- `app.py` - 主应用文件
- `models.py` - 数据库模型
- `views.py` - 视图函数

重点关注：
- 数据库查询是否使用参数化
- 用户输入是否正确转义
- 敏感配置是否使用环境变量

### 示例 2：前端代码安全扫描
检查以下文件：
- `index.html` - HTML 模板
- `app.js` - JavaScript 代码

重点关注：
- DOM 操作是否安全
- 是否使用 `innerHTML` 输出用户数据
- API 调用是否验证响应数据

### 示例 3：配置文件安全检查
检查以下文件：
- `.env` - 环境变量
- `config.py` - 配置文件
- `settings.py` - 设置文件

重点关注：
- 是否包含硬编码的密钥
- 敏感信息是否已移除
- 文件权限是否正确
---

## 代码定位与修复建议示例

### 示例 1：SQL 注入漏洞定位

**临时文件：`.tmp-security-sqli-001.md`**

```markdown
# SQL 注入漏洞 - #001

## 漏洞信息
- **漏洞类型**：SQL 注入
- **风险等级**：🚨 严重
- **发现时间**：2024-03-23 10:30:00

## 代码定位
- **文件路径**：`./app/views/user.py`
- **文件名**：user.py
- **行号**：42-45
- **函数**：`get_user_by_id()`

## 受影响的代码段
```python
def get_user_by_id(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchone()
```

## 风险描述
直接使用用户输入构建 SQL 查询，攻击者可通过 `user_id` 参数注入恶意 SQL 代码，导致数据泄露或数据库被破坏。

## 修复建议

### 方案 1：使用参数化查询（推荐）
```python
def get_user_by_id(user_id):
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()
```

### 方案 2：使用 ORM（如 Django ORM）
```python
from app.models import User

def get_user_by_id(user_id):
    return User.objects.get(id=user_id)
```

## 修复要点
1. 使用参数化查询，禁止字符串拼接
2. 验证 `user_id` 参数类型（确保为整数）
3. 考虑添加输入白名单验证

## 验证步骤
```bash
# 测试正常输入
curl http://localhost:8000/user?id=1

# 测试恶意输入（应被阻止）
curl http://localhost:8000/user?id=1'; DROP TABLE users; --
```
```

---

### 示例 2：敏感信息泄露定位

**临时文件：`.tmp-security-secret-001.md`**

```markdown
# 敏感信息泄露漏洞 - #001

## 漏洞信息
- **漏洞类型**：敏感信息泄露（硬编码密钥）
- **风险等级**：🚨 严重
- **发现时间**：2024-03-23 10:35:00

## 代码定位
- **文件路径**：`./config/settings.py`
- **文件名**：settings.py
- **行号**：15-18

## 受影响的代码段
```python
# API 配置
OPENAI_API_KEY = "sk-proj-abc123def456ghi789jkl012mno345pqr"
DATABASE_PASSWORD = "admin123"
SECRET_KEY = "django-insecure-@#$%secretkey"
```

## 风险描述
敏感凭证硬编码在代码中，可能导致：
1. 凭证被提交到版本控制系统
2. 代码泄露时凭证一并泄露
3. 未授权人员可访问相关服务

## 修复建议

### 方案 1：使用环境变量（推荐）
```python
import os
from pathlib import Path

# 从环境变量读取敏感信息
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD")

# 或使用 python-dotenv
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")
```

### 方案 2：使用密钥管理服务
```python
# AWS Secrets Manager
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

OPENAI_API_KEY = get_secret('openai-api-key')['api_key']
```

## 环境变量配置示例
创建 `.env` 文件（添加到 `.gitignore`）：
```env
OPENAI_API_KEY=sk-proj-your-actual-key-here
DB_PASSWORD=your-secure-password
SECRET_KEY=your-django-secret-key
```

## 修复要点
1. 移除所有硬编码的敏感信息
2. 使用环境变量或密钥管理服务
3. 将 `.env` 文件添加到 `.gitignore`
4. 提供默认配置示例文件（如 `.env.example`）

## 验证步骤
```bash
# 1. 检查代码中是否还有硬编码凭证
grep -r "sk-" . --include="*.py"
grep -r "password = " . --include="*.py"

# 2. 确认 .env 在 .gitignore 中
cat .gitignore | grep "\.env"

# 3. 测试环境变量加载
python -c "from config.settings import OPENAI_API_KEY; print(OPENAI_API_KEY[:10] + '...')"
```
```

---

### 示例 3：XSS 漏洞定位

**临时文件：`.tmp-security-xss-001.md`**

```markdown
# XSS 跨站脚本攻击漏洞 - #001

## 漏洞信息
- **漏洞类型**：XSS 跨站脚本攻击
- **风险等级**：🔴 高危
- **发现时间**：2024-03-23 10:40:00

## 代码定位
- **文件路径**：`./app/templates/comment.html`
- **文件名**：comment.html
- **行号**：23-27

## 受影响的代码段
```html
<div class="comment">
  <h4>{{ comment.author }}</h4>
  <div class="content">{{ comment.content|safe }}</div>
  <small>{{ comment.timestamp }}</small>
</div>
```

## 风险描述
使用 `|safe` 过滤器导致 HTML 转义被禁用，攻击者可在评论中注入恶意脚本，窃取用户 Cookie 或执行恶意操作。

## 修复建议

### 方案 1：移除 safe 过滤器（推荐）
```html
<div class="comment">
  <h4>{{ comment.author }}</h4>
  <div class="content">{{ comment.content }}</div>
  <small>{{ comment.timestamp }}</small>
</div>
```

### 方案 2：使用 DOMPurify 过滤富文本
```html
<div class="comment">
  <h4>{{ comment.author }}</h4>
  <div class="content" id="comment-{{ comment.id }}"></div>
  <small>{{ comment.timestamp }}</small>
</div>

<script src="https://cdn.jsdelivr.net/npm/dompurify@3.0.6/dist/purify.min.js"></script>
<script>
  const content = {{ comment.content|tojson }};
  document.getElementById('comment-{{ comment.id }}').innerHTML = DOMPurify.sanitize(content);
</script>
```

## 修复要点
1. 移除不必要的 `|safe` 过滤器
2. 如果需要富文本，使用 DOMPurify 等库过滤
3. 设置 Content-Security-Policy 响应头
4. 对用户输入进行服务器端验证

## CSP 配置示例
```python
# Django settings.py
SECURE_CONTENT_SECURITY_POLICIES = {
    'default-src': ["'self'"],
    'script-src': ["'self'", "https://cdn.jsdelivr.net"],
    'style-src': ["'self'", "'unsafe-inline'"],
}
```

## 验证步骤
```bash
# 1. 搜索所有 |safe 过滤器
grep -r "|safe" ./app/templates/

# 2. 测试 XSS 攻击（应在页面中显示为文本而非执行）
curl -X POST http://localhost:8000/comment \
  -d "content=<script>alert('XSS')</script>"

# 3. 使用浏览器开发者工具检查 CSP 头
curl -I http://localhost:8000/comment/1 | grep Content-Security-Policy
```
```

---

## 临时文件命名规范

### 文件命名格式
```
.tmp-{漏洞类型英文缩写}-{序号}.md
```

### 漏洞类型缩写
| 漏洞类型 | 缩写 | 示例 |
|---------|------|------|
| SQL 注入 | sqli | .tmp-sqli-001.md |
| XSS | xss | .tmp-xss-001.md |
| 敏感信息泄露 | secret | .tmp-secret-001.md |
| 命令注入 | cmdi | .tmp-cmdi-001.md |
| 路径遍历 | path | .tmp-path-001.md |
| CSRF | csrf | .tmp-csrf-001.md |
| 不安全的反序列化 | deser | .tmp-deser-001.md |
| 不安全的随机数 | random | .tmp-random-001.md |

### 临时文件结构模板
```markdown
# {漏洞类型} - #{序号}

## 漏洞信息
- **漏洞类型**：{漏洞类型名称}
- **风险等级**：{风险等级 Emoji + 文字}
- **发现时间**：{时间戳}

## 代码定位
- **文件路径**：`./{相对路径}/{文件名}`
- **文件名**：{文件名}
- **行号**：{起始行}-{结束行}
- **函数/类**：{函数名或类名}（可选）

## 受影响的代码段
```{编程语言}
{受影响的代码段}
```

## 风险描述
{详细的风险描述，包括可能的攻击场景和影响}

## 修复建议

### 方案 1：{方案名称}
```{编程语言}
{修复代码示例}
```

### 方案 2：{方案名称}（可选）
```{编程语言}
{修复代码示例}
```

## 修复要点
1. {修复要点 1}
2. {修复要点 2}
3. {修复要点 3}

## 验证步骤
```bash
{验证命令或步骤}
```
```
---

## Semgrep 工具使用

### 工具简介

Semgrep 是一个开源的静态代码分析工具，支持多种编程语言的安全扫描和代码质量检查。

**主要特点**：
- 支持多种语言：Python, JavaScript, TypeScript, Java, Go, Ruby, PHP, C/C++ 等
- 快速扫描：基于 AST（抽象语法树）的规则匹配
- 可自定义规则：支持编写自定义规则
- 丰富的规则库：内置 2000+ 安全规则
- 多种输出格式：JSON, SARIF, 文本等

### 安装 Semgrep

```bash
# 使用 pip 安装
pip install semgrep

# 使用 Homebrew（macOS）
brew install semgrep

# 使用 Docker
docker run --rm -v "${PWD}:/src" returntocorp/semgrep
```

### 基本用法

#### 调用脚本扫描

```bash
# 扫描整个项目
python scripts/semgrep_scan.py ./app --report

# 扫描特定目录
python scripts/semgrep_scan.py ./src

# 扫描特定文件
python scripts/semgrep_scan.py ./app/views.py

# 排除测试目录和虚拟环境
python scripts/semgrep_scan.py ./src --exclude tests/,venv/,node_modules/

# 使用特定规则集
python scripts/semgrep_scan.py ./src --rules p/security-audit
```

#### 常用规则集

- `auto`: 自动检测语言并使用推荐规则（默认）
- `p/security-audit`: Python 安全审计规则
- `p/javascript`: JavaScript 安全规则
- `p/cwe`: CWE 漏洞规则
- `p/owasp-top-10`: OWASP Top 10 规则
- `path/to/custom-rule.yml`: 自定义规则文件

### Semgrep 规则示例

#### 示例 1：检测 SQL 注入

**规则文件：`rules/python-sql-injection.yml`**

```yaml
rules:
  - id: python-sql-injection
    patterns:
      - pattern-either:
          - pattern: |
              $SQL = "..." + $USER_INPUT
              db.execute($SQL)
          - pattern: |
              $SQL = f"...{$USER_INPUT}..."
              db.execute($SQL)
          - pattern: |
              db.execute("...{}".format($USER_INPUT))
    languages: [python]
    severity: ERROR
    message: Possible SQL injection via string formatting
    metadata:
      cwe: "CWE-89: SQL Injection"
      references:
        - https://owasp.org/www-community/attacks/SQL_Injection
```

#### 示例 2：检测硬编码密钥

**规则文件：`rules/python-hardcoded-secrets.yml`**

```yaml
rules:
  - id: python-hardcoded-api-key
    patterns:
      - pattern-regex: '(?i)(api[_-]?key|secret[_-]?key|password|token)\s*=\s*["\'](?![a-z]{20,})[a-zA-Z0-9]{20,}["\']'
    languages: [python]
    severity: ERROR
    message: Hardcoded API key or secret detected
    metadata:
      cwe: "CWE-798: Use of Hard-coded Credentials"
      references:
        - https://cwe.mitre.org/data/definitions/798.html
```

#### 示例 3：检测 XSS 漏洞

**规则文件：`rules/python-xss.yml`**

```yaml
rules:
  - id: python-xss-django
    patterns:
      - pattern: |
          $HTML = HttpResponse(...)
          return $HTML
    languages: [python]
    severity: WARNING
    message: Possible XSS vulnerability in Django response
    metadata:
      cwe: "CWE-79: Cross-site Scripting"
```

#### 示例 4：检测命令注入

**规则文件：`rules/python-command-injection.yml`**

```yaml
rules:
  - id: python-command-injection
    patterns:
      - pattern-either:
          - pattern: os.system("..." + $USER_INPUT)
          - pattern: subprocess.call("..." + $USER_INPUT)
          - pattern: subprocess.run("..." + $USER_INPUT, ...)
          - pattern: eval("..." + $USER_INPUT)
    languages: [python]
    severity: ERROR
    message: Possible command injection via string concatenation
    metadata:
      cwe: "CWE-78: OS Command Injection"
```

#### 示例 5：检测不安全的随机数

**规则文件：`rules/python-insecure-random.yml`**

```yaml
rules:
  - id: python-insecure-random
    patterns:
      - pattern: random.$METHOD(...)
      - metavariable-regex:
          metavariable: $METHOD
          regex: "(random|randint|choice|shuffle)"
    languages: [python]
    severity: WARNING
    message: Use of insecure random number generator. Use secrets module instead.
    metadata:
      cwe: "CWE-330: Use of Insufficiently Random Values"
      references:
        - https://docs.python.org/3/library/secrets.html
```

### 输出结果解析

#### JSON 格式输出

脚本输出的 JSON 格式：

```json
{
  "error": false,
  "summary": {
    "total_findings": 5,
    "by_severity": {
      "ERROR": 2,
      "WARNING": 2,
      "INFO": 1
    }
  },
  "findings": [
    {
      "rule_id": "python.sql-injection",
      "severity": "ERROR",
      "message": "Possible SQL injection via string formatting",
      "file": "app/views.py",
      "line": 42,
      "column": 10,
      "end_line": 42,
      "end_column": 50,
      "code_snippet": "query = f'SELECT * FROM users WHERE id = {user_id}'",
      "fix": "Use parameterized query instead of string formatting",
      "cwe": ["CWE-89"],
      "references": [
        "https://owasp.org/www-community/attacks/SQL_Injection"
      ]
    }
  ]
}
```

#### 严重性映射

| Semgrep 严重性 | 风险等级 | Emoji |
|---------------|---------|-------|
| ERROR | 严重 | 🚨 |
| WARNING | 高危 | 🔴 |
| INFO | 中危 | 🟡 |
| UNKNOWN | 低危 | 🟢 |

### 自定义规则

#### 规则结构

```yaml
rules:
  - id: <唯一规则ID>
    patterns:
      - pattern-regex: <正则表达式模式>
      # 或
      - pattern: <代码模式>
    languages: [python, javascript, ...]
    severity: ERROR | WARNING | INFO
    message: <问题描述>
    metadata:
      category: security
      technology: [django, flask, ...]
      cwe: <CWE编号>
      references:
        - <参考链接>
```

#### 编写自定义规则示例

**检测使用 md5 哈希**

```yaml
rules:
  - id: insecure-hash-md5
    patterns:
      - pattern: hashlib.md5(...)
    languages: [python]
    severity: WARNING
    message: MD5 is not a secure hash function. Use SHA-256 instead.
    metadata:
      cwe: "CWE-327: Use of a Broken or Risky Cryptographic Algorithm"
```

**检测未验证的用户输入**

```yaml
rules:
  - id: unvalidated-user-input
    patterns:
      - pattern: |
          $INPUT = request.$METHOD.get(...)
          ...
          dangerous_function($INPUT)
    languages: [python]
    severity: WARNING
    message: User input should be validated before use
```

### 与智能体配合使用

#### 工作流程

1. **智能体调用 Semgrep 脚本**
   ```bash
   python scripts/semgrep_scan.py ./app --report
   ```

2. **脚本返回 JSON 结果**
   - 包含漏洞摘要和详细信息
   - 标注文件路径、行号、代码段

3. **智能体分析结果**
   - 解析 JSON 输出
   - 识别高风险漏洞
   - 分析漏洞上下文

4. **智能体生成报告**
   - 为每个漏洞生成临时 markdown 文件
   - 提供详细的修复建议
   - 汇总生成总体报告

#### 最佳实践

1. **结合使用**
   - Semgrep 用于快速扫描和识别已知模式
   - 智能体用于深度分析和上下文理解
   - 两者结合提高扫描准确性和覆盖率

2. **规则选择**
   - 默认使用 `auto` 规则集
   - 对于特定安全审计，使用 `p/security-audit`
   - 对于特定项目，编写自定义规则

3. **排除路径**
   - 排除测试代码：`--exclude tests/,spec/`
   - 排除第三方库：`--exclude node_modules/,vendor/`
   - 排除生成的代码：`--exclude migrations/`

4. **结果验证**
   - Semgrep 可能产生误报
   - 智能体需验证每个发现
   - 结合代码上下文判断是否为真实漏洞

### 常见问题

#### Q: Semgrep 未安装怎么办？

**A**: 安装 Semgrep：
```bash
pip install semgrep
```

或使用智能体手动分析功能。

#### Q: 如何减少误报？

**A**:
1. 使用更精确的规则
2. 排除已知安全的代码路径
3. 让智能体验证每个发现
4. 编写项目特定的自定义规则

#### Q: 支持哪些编程语言？

**A**:
Semgrep 支持以下语言：
- Python, JavaScript, TypeScript
- Java, Go, Ruby, PHP
- C, C++, C#
- Kotlin, Swift, Rust
- HTML, CSS, JSON, YAML 等

#### Q: 扫描速度慢怎么办？

**A**:
1. 缩小扫描范围，只扫描关键目录
2. 排除第三方库目录
3. 使用更少的规则集
4. 并行扫描多个目标

### 参考资源

- [Semgrep 官方文档](https://semgrep.dev/docs/)
- [Semgrep 规则库](https://semgrep.dev/explore)
- [编写自定义规则](https://semgrep.dev/docs/writing-rules/overview)
- [Semgrep CLI 参考](https://semgrep.dev/docs/cli-reference)
