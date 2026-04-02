---
name: security-scanner
description: 自动扫描代码中的安全漏洞并提供修复方案；当用户需要检查代码安全性、生成漏洞报告或获取安全修复建议时使用
dependency:
  system:
    - pip install semgrep 2>/dev/null || echo "Semgrep not installed, will use manual analysis"
    - semgrep --version 2>/dev/null || true
metadata: { "copaw": { "emoji": "🔒" } }
---

# 代码安全漏洞扫描器

## 任务目标
- 本 Skill 用于：自动扫描代码仓库的安全风险并生成详细的漏洞报告
- 能力包含：安全漏洞识别、风险等级评估、修复方案生成
- 触发条件：用户需要代码安全审查、漏洞扫描报告、或安全修复建议

## 前置准备
- 确保代码仓库已上传到当前目录
- 准备待扫描的文件路径或目录路径

## 操作步骤

### 1. 扫描准备
- 确认代码位置和范围（单个文件、目录或整个仓库）
- 识别编程语言和技术栈（Python、JavaScript、Java 等）
- 确定扫描深度（快速扫描 vs 深度分析）

### 2. 执行安全扫描

#### 方式 1：使用 Semgrep 自动扫描（推荐）
- 调用脚本 `scripts/semgrep_scan.py` 执行自动化扫描
- 参数说明：
  - `target_path`: 扫描目标路径（文件或目录），Windows 系统需使用绝对路径
  - `--rules`: Semgrep 规则集（默认：auto，自动检测编程语言）
  - `--exclude`: 排除的路径（逗号分隔，例如：tests/,venv/,node_modules/）
  - `--report`: 生成可读格式的报告（默认输出 JSON 格式）
  - `--timeout`: 扫描超时时间（秒，默认：600）
- 执行示例：
  ```bash
  # 扫描整个项目并生成可读报告
  python scripts/semgrep_scan.py ./app --report

  # 扫描特定文件并排除测试目录
  python scripts/semgrep_scan.py ./src --exclude tests/,venv/

  # 自定义超时时间
  python scripts/semgrep_scan.py ./app --timeout 1200 --report
  ```
- 输出格式：
  - **JSON 格式**（默认）：结构化数据，包含扫描统计和详细漏洞列表
  - **可读报告**（使用 `--report`）：人类可读的文本报告，包含风险等级和修复建议
- 扫描统计信息：
  - 扫描文件数量
  - 扫描完成状态
  - Semgrep 返回码
  - 按严重等级分类的漏洞统计
- Semgrep 支持的语言：Python, JavaScript, TypeScript, Java, Go, Ruby, PHP, C/C++ 等
- 优势：快速、准确、支持多种安全规则

#### 方式 2：智能体手动分析
- 智能体遍历代码文件，分析潜在安全风险
- 检查范围包括但不限于：
  - SQL 注入风险
  - XSS 跨站脚本攻击
  - 敏感信息泄露（密钥、密码硬编码）
  - 不安全的反序列化
  - 路径遍历漏洞
  - 不安全的随机数生成
  - 命令注入风险
  - 不安全的依赖项
- 参考常见漏洞检查清单，逐项验证

### 3. 风险等级评估
- 对每个发现的漏洞进行风险等级分类：
  - **严重**：可直接利用导致数据泄露或系统入侵
  - **高危**：可能被利用造成严重影响
  - **中危**：存在安全隐患但利用难度较高
  - **低危**：轻微安全问题，建议修复
- 统计各风险等级的漏洞数量

### 4. 生成漏洞报告
- 使用标准报告模板生成结构化报告
- 报告包含：
  - 扫描概览（文件数量、代码行数、漏洞总数）
  - 风险等级统计
  - 详细漏洞列表（位置、类型、影响、修复建议）
  - 优先级排序的修复计划

### 5. 提供修复方案
- 为每个漏洞提供具体的修复代码建议
- 修复方案包括：
  - 问题代码定位（包含文件相对路径、文件名、行号）
  - 受影响的代码段展示
  - 安全的替代实现
  - 最佳实践建议
  - 修复后的代码示例

### 6. 生成临时问题记录
- 为每个发现的漏洞生成临时 markdown 文件
- 临时文件命名：`.tmp-security-{漏洞类型}-{序号}.md`
- 每个临时文件包含：
  - 漏洞类型和风险等级
  - 文件路径和行号
  - 受影响的代码段
  - 具体的修复建议和代码示例
- 临时文件保存在当前工作目录（`./`）

### 7. 生成总体报告
- 合并所有临时文件内容，生成统一的安全漏洞报告
- 报告使用标准模板，包含：
  - 扫描概览和风险统计（文件数量、漏洞总数、按严重等级分类）
  - 所有漏洞的详细信息（代码段、路径、行号、修复建议）
  - 修复优先级建议
- 清理所有临时文件（`.tmp-*.md`）

## 资源索引
- 必要脚本：见 [scripts/semgrep_scan.py](scripts/semgrep_scan.py)（用途：执行 Semgrep 自动化扫描；参数：target_path, --rules, --exclude, --report）
- 领域参考：见 [references/security-vulnerabilities.md](references/security-vulnerabilities.md)（常见安全漏洞类型、检查清单、Semgrep 规则示例）
- 输出资产：见 [assets/report-template.md](assets/report-template.md)（漏洞报告模板）

## 注意事项
- 扫描范围越大，分析时间越长
- 优先关注严重和高危漏洞
- 修复建议需结合实际业务场景验证
- 建议定期进行安全扫描，建立安全意识

## 使用示例

### 示例 1：使用 Semgrep 扫描 Python Web 应用
- 功能：使用 Semgrep 自动扫描 Flask/Django 应用中的安全漏洞
- 执行方式：调用 `scripts/semgrep_scan.py` + 智能体分析结果
- 关键要点：重点关注 SQL 注入和 XSS 风险
- 命令示例：`python scripts/semgrep_scan.py ./app --report`

### 示例 2：智能体手动扫描前端代码
- 功能：检查 JavaScript/TypeScript 中的客户端安全问题
- 执行方式：智能体分析 DOM 操作、API 调用、用户输入处理
- 关键要点：重点关注 XSS 和敏感信息泄露

### 示例 3：快速安全审查
- 功能：对新增代码进行安全审查
- 执行方式：使用 Semgrep 快速扫描或仅扫描变更的文件
- 关键要点：快速识别高风险安全问题
- 命令示例：`python scripts/semgrep_scan.py ./src/new_feature/ --exclude tests/,venv/`

### 示例 4：自定义超时时间
- 功能：对大型代码仓库进行深度扫描
- 执行方式：增加超时时间避免扫描中断
- 关键要点：适用于代码量大或规则复杂的情况
- 命令示例：`python scripts/semgrep_scan.py ./large-project --timeout 1800 --report`
