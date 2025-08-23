# Hướng Dẫn Viết Chatmode Hiệu Quả

## 📋 Cấu Trúc Chuẩn Của Chatmode

### 1. Front Matter (YAML Header)
```yaml
---
description: 'Mô tả ngắn gọn về chức năng của chatmode'
model: GPT-4.1 (tùy chọn)
title: 'Tên chatmode' (tùy chọn)
tools: ['tool1', 'tool2', 'tool3'] (tùy chọn - danh sách công cụ cần thiết)
---
```

### 2. Phần Chính (Markdown Content)
- **Tiêu đề chính**: Tên vai trò/chế độ
- **Mục tiêu chính**: Định nghĩa rõ ràng vai trò và nhiệm vụ
- **Hướng dẫn chi tiết**: Các bước thực hiện cụ thể
- **Quy tắc và nguyên tắc**: Các ràng buộc và hướng dẫn
- **Ví dụ**: Minh họa cách thực hiện (nếu cần)

## 🎯 Các Loại Chatmode Phổ Biến

### 1. **Expert/Specialist Modes**
- Tập trung vào chuyên môn cụ thể
- Cung cấp kiến thức sâu và best practices
- Ví dụ: `expert-dotnet-software-engineer`, `azure-principal-architect`

### 2. **Process/Workflow Modes**
- Hướng dẫn quy trình làm việc cụ thể
- Có workflow và checklist rõ ràng
- Ví dụ: `tdd-green`, `debug`, `implementation-plan`

### 3. **Behavioral Modes**
- Định nghĩa cách tương tác và giao tiếp
- Tập trung vào soft skills
- Ví dụ: `mentor`, `critical-thinking`

### 4. **Task-Specific Modes**
- Thực hiện một nhiệm vụ cụ thể
- Có input/output rõ ràng
- Ví dụ: `prompt-engineer`, `specification`

## ✍️ Nguyên Tắc Viết Chatmode Hiệu Quả

### 1. **Clarity (Rõ ràng)**
- Sử dụng ngôn ngữ đơn giản, dễ hiểu
- Tránh thuật ngữ mơ hồ
- Định nghĩa rõ vai trò và kết quả mong muốn

### 2. **Specificity (Cụ thể)**
- Đưa ra hướng dẫn chi tiết, có thể thực hiện được
- Cung cấp ví dụ cụ thể
- Định nghĩa rõ input và output

### 3. **Structure (Cấu trúc)**
- Sử dụng headings, bullet points, numbering
- Tổ chức thông tin theo logic
- Dễ scan và tìm kiếm thông tin

### 4. **Actionability (Khả năng thực hiện)**
- Mỗi hướng dẫn phải có thể thực hiện được
- Cung cấp bước cụ thể, không mơ hồ
- Có thể đo lường được kết quả

## 📝 Checklist Viết Chatmode

### Pre-Writing
- [ ] Xác định rõ mục đích và đối tượng sử dụng
- [ ] Nghiên cứu các chatmode tương tự
- [ ] Định nghĩa scope và ranh giới
- [ ] Xác định tools cần thiết

### Structure & Content
- [ ] Front matter đầy đủ và chính xác
- [ ] Tiêu đề mô tả rõ vai trò
- [ ] Mục tiêu chính được định nghĩa rõ ràng
- [ ] Hướng dẫn có thể thực hiện được
- [ ] Sử dụng format markdown đúng chuẩn

### Quality Assurance
- [ ] Ngôn ngữ đơn giản, dễ hiểu
- [ ] Không có typo hoặc lỗi grammar
- [ ] Logic flow hợp lý
- [ ] Có ví dụ minh họa (nếu cần)
- [ ] Test với scenarios khác nhau

### Advanced Features
- [ ] Workflow/process rõ ràng
- [ ] Error handling và edge cases
- [ ] Integration với tools
- [ ] Performance considerations
- [ ] Compliance và security

## 🛠️ Cheat Sheet - Các Thành Phần Quan Trọng

### 1. **Role Definition**
```markdown
# [Role Name] mode instructions

You are in [role] mode. Your task is to [primary objective].
```

### 2. **Primary Objectives**
```markdown
Your primary goal is to:
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]
```

### 3. **Guidelines/Rules**
```markdown
## Guidelines
- **Rule 1**: Specific instruction
- **Rule 2**: Another instruction
- **Don't**: What to avoid
```

### 4. **Workflow/Process**
```markdown
## Workflow
1. **Phase 1**: Description
   - Step 1.1
   - Step 1.2
2. **Phase 2**: Description
   - Step 2.1
   - Step 2.2
```

### 5. **Tools Integration**
```markdown
Use the following tools:
- `tool1` for [purpose]
- `tool2` for [purpose]
```

### 6. **Output Format**
```markdown
## Output Format
Provide your response in the following format:
- [Format requirement 1]
- [Format requirement 2]
```

### 7. **Examples**
```markdown
## Examples
<examples>
<example>
<user>Sample input</user>
<response>Expected output</response>
</example>
</examples>
```

## 💡 Best Practices Từ Awesome-Copilot

### 1. **From Beast Mode**
- Autonomous execution với clear workflow
- Extensive research requirements
- Tool usage guidelines
- Error handling và iteration

### 2. **From Mentor Mode**
- Socratic questioning approach
- Challenge assumptions
- Provide guidance, not direct answers
- Use examples from real scenarios

### 3. **From Debug Mode**
- Systematic problem-solving process
- Phase-based approach
- Documentation requirements
- Quality assurance steps

### 4. **From API Architect**
- Clear input requirements
- Structured deliverables
- Layer-based architecture
- No templates, full implementation

## 🚨 Common Pitfalls

### ❌ Avoid These Mistakes
1. **Vague instructions** - "Be helpful" thay vì specific actions
2. **Too complex** - Quá nhiều rules phức tạp
3. **Missing examples** - Không có minh họa cụ thể
4. **Poor structure** - Khó đọc và scan
5. **Ambiguous roles** - Không rõ ranh giới trách nhiệm
6. **No error handling** - Không handle edge cases
7. **Tool confusion** - Không rõ khi nào dùng tool nào

### ✅ Do These Instead
1. **Specific, actionable instructions**
2. **Clear, simple language**
3. **Concrete examples**
4. **Well-organized structure**
5. **Defined boundaries**
6. **Comprehensive error handling**
7. **Clear tool usage guidelines**

## 📊 Template Cơ Bản

```markdown
---
description: 'Mô tả ngắn gọn chức năng chatmode'
tools: ['tool1', 'tool2'] # nếu cần
---

# [Role Name] Mode Instructions

You are in [role] mode. Your primary objective is to [main goal].

## Primary Goals
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

## Guidelines
- **Do**: [Positive instruction]
- **Don't**: [What to avoid]
- **When**: [Conditional instruction]

## Workflow
1. **Phase 1**: [Description]
   - Step 1.1
   - Step 1.2
2. **Phase 2**: [Description]
   - Step 2.1
   - Step 2.2

## Output Format
[Describe expected output format]

## Examples
[Provide concrete examples if needed]

## Notes
[Additional considerations, edge cases, etc.]
```

---

*Tip: Hãy test chatmode với nhiều scenarios khác nhau để đảm bảo hoạt động đúng như mong muốn!*