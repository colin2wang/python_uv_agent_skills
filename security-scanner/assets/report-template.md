# 代码安全漏洞扫描报告

## 扫描概览

**扫描时间**：{{ scan_time }}
**扫描范围**：{{ scan_scope }}
**项目类型**：{{ project_type }}
**文件总数**：{{ total_files }}
**代码行数**：{{ total_lines }}

---

## 风险等级统计

| 风险等级 | 数量 | 占比 |
|---------|------|------|
| 🚨 严重 | {{ critical_count }} | {{ critical_percent }}% |
| 🔴 高危 | {{ high_count }} | {{ high_percent }}% |
| 🟡 中危 | {{ medium_count }} | {{ medium_percent }}% |
| 🟢 低危 | {{ low_count }} | {{ low_percent }}% |
| **总计** | **{{ total_vulnerabilities }}** | **100%** |

---

## 详细漏洞列表

### 🚨 严重漏洞（{{ critical_count }} 个）

#### 漏洞 #{{ id }}：{{ vulnerability_type }}
- **风险等级**：🚨 严重
- **发现时间**：{{ discovery_time }}
- **文件路径**：`{{ file_path }}`
- **文件名**：{{ file_name }}
- **行号**：第 {{ line_number }} 行
- **函数/类**：{{ function_or_class }}（可选）
- **影响范围**：{{ impact }}
- **风险描述**：{{ description }}

**受影响的代码段**：
```{{ language }}
{{ vulnerable_code }}
```

**修复建议**：
```{{ language }}
{{ fixed_code }}
```

**修复要点**：
1. {{ fix_point_1 }}
2. {{ fix_point_2 }}
3. {{ fix_point_3 }}

**验证步骤**：
```bash
{{ validation_commands }}
```

**参考链接**：{{ reference_url }}

---

### 🔴 高危漏洞（{{ high_count }} 个）

#### 漏洞 #{{ id }}：{{ vulnerability_type }}
- **风险等级**：🔴 高危
- **发现时间**：{{ discovery_time }}
- **文件路径**：`{{ file_path }}`
- **文件名**：{{ file_name }}
- **行号**：第 {{ line_number }} 行
- **函数/类**：{{ function_or_class }}（可选）
- **影响范围**：{{ impact }}
- **风险描述**：{{ description }}

**受影响的代码段**：
```{{ language }}
{{ vulnerable_code }}
```

**修复建议**：
```{{ language }}
{{ fixed_code }}
```

**修复要点**：
1. {{ fix_point_1 }}
2. {{ fix_point_2 }}

**验证步骤**：
```bash
{{ validation_commands }}
```

**参考链接**：{{ reference_url }}

---

### 🟡 中危漏洞（{{ medium_count }} 个）

#### 漏洞 #{{ id }}：{{ vulnerability_type }}
- **风险等级**：🟡 中危
- **发现时间**：{{ discovery_time }}
- **文件路径**：`{{ file_path }}`
- **文件名**：{{ file_name }}
- **行号**：第 {{ line_number }} 行
- **影响范围**：{{ impact }}
- **风险描述**：{{ description }}

**受影响的代码段**：
```{{ language }}
{{ vulnerable_code }}
```

**修复建议**：{{ fix_suggestion }}

**修复要点**：{{ fix_points }}

---

### 🟢 低危漏洞（{{ low_count }} 个）

#### 漏洞 #{{ id }}：{{ vulnerability_type }}
- **风险等级**：🟢 低危
- **发现时间**：{{ discovery_time }}
- **文件路径**：`{{ file_path }}`
- **文件名**：{{ file_name }}
- **行号**：第 {{ line_number }} 行
- **影响范围**：{{ impact }}
- **风险描述**：{{ description }}

**受影响的代码段**：
```{{ language }}
{{ vulnerable_code }}
```

**修复建议**：{{ fix_suggestion }}

---

## 修复优先级建议

### 第一优先级（立即修复）
1. **{{ vulnerability_1 }}**
   - 文件：`{{ file_path_1 }}`
   - 风险：严重/高危
   - 影响：{{ impact_1 }}

2. **{{ vulnerability_2 }}**
   - 文件：`{{ file_path_2 }}`
   - 风险：严重/高危
   - 影响：{{ impact_2 }}

**说明**：这些漏洞可被直接利用，导致严重安全后果。

### 第二优先级（本周内修复）
1. **{{ vulnerability_3 }}**
   - 文件：`{{ file_path_3 }}`
   - 风险：中危
   - 影响：{{ impact_3 }}

2. **{{ vulnerability_4 }}**
   - 文件：`{{ file_path_4 }}`
   - 风险：中危
   - 影响：{{ impact_4 }}

**说明**：这些漏洞存在利用风险，但需要特定条件。

### 第三优先级（下次迭代修复）
1. **{{ vulnerability_5 }}**
   - 文件：`{{ file_path_5 }}`
   - 风险：低危
   - 影响：{{ impact_5 }}

2. **{{ vulnerability_6 }}**
   - 文件：`{{ file_path_6 }}`
   - 风险：低危
   - 影响：{{ impact_6 }}

**说明**：这些是安全最佳实践建议，建议逐步改进。

---

## 安全建议

### 立即采取的措施
1. {{ immediate_action_1 }}
2. {{ immediate_action_2 }}
3. {{ immediate_action_3 }}

### 长期改进计划
1. {{ long_term_improvement_1 }}
2. {{ long_term_improvement_2 }}
3. {{ long_term_improvement_3 }}

### 安全最佳实践
- {{ best_practice_1 }}
- {{ best_practice_2 }}
- {{ best_practice_3 }}

---

## 扫描结论

**总体安全评分**：{{ security_score }}/100

**总结**：{{ summary }}

**建议**：{{ recommendation }}

---

## 附录：临时文件清单

本次扫描生成的临时文件（已合并至本报告）：
{{ temp_files_list }}

---

**报告生成工具**：Security Scanner Skill
**报告版本**：1.1
**生成时间**：{{ generation_time }}
