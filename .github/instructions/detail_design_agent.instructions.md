---
applyTo: "**"
---
# Hướng dẫn Tài liệu Thiết kế Hệ thống (DD - Design Document)

## Tổng quan về cấu trúc DD

Tài liệu DD (Design Document) được tổ chức theo kiến trúc phân lớp, mỗi module/chức năng có cấu trúc thư mục riêng với 4 tầng chính:

```
DD/
├── database.md                    # Thiết kế cơ sở dữ liệu chung
├── [Template].csv                 # File mẫu import/export
└── MDE-XX/                       # Module chức năng (XX = số thứ tự)
    ├── 01-screen/                # Tầng giao diện người dùng
    ├── 02-api/                   # Tầng API/Controller
    ├── 03-service/               # Tầng logic nghiệp vụ
    └── 04-dao/                   # Tầng truy cập dữ liệu
```

## Chi tiết từng loại file

### 1. Database Design (`database.md`)

**Mục đích**: Định nghĩa cấu trúc cơ sở dữ liệu toàn hệ thống

**Nội dung chính**:
- **Tables**: Danh sách các bảng trong hệ thống
- **Columns & Constraints**: Chi tiết cột, kiểu dữ liệu, ràng buộc
- **Foreign Key Relationships**: Mối quan hệ giữa các bảng

**Ví dụ cấu trúc**:
```markdown
## Tables
| No | ID | Name | Description |
|----|----|----- |-------------|
| 1  | idle_resources | Idle Resources | Stores idle personnel info |

## Columns & Constraints
### Table: idle_resources
| No | ID | Name | Data Type | Length | Primary Key | Nullable | Default | Foreign Key | References |
```

### 2. Template Files (`.csv`)

**Mục đích**: Định nghĩa format file import/export dữ liệu

**Nội dung**: Header columns của file Excel/CSV được sử dụng trong chức năng import/export

### 3. Screen Design (`01-screen/SCR-MDE-XX-YY.md`)

**Mục đích**: Thiết kế chi tiết giao diện người dùng

**Cấu trúc document**:
- **Used APIs**: Danh sách API được screen sử dụng
- **Screen Layout**: Chi tiết các thành phần UI (button, table, dropdown...)
- **Events**: Các sự kiện người dùng có thể thực hiện
- **Steps & Details**: Flow chi tiết của từng event

**Ví dụ Screen Layout**:
```markdown
| No | ID | Name | Type | Status | Description |
|----|----|----- |------|--------|-------------|
| 1  | ITEM-01 | Search Bar | Text Field | Enabled | Search by name/email |
| 2  | ITEM-02 | Import Button | Button | Enabled | Import from Excel |
```

### 4. API Design (`02-api/API-MDE-XX-YY.md`)

**Mục đích**: Định nghĩa interface API và luồng xử lý

**Cấu trúc document**:
- **Used Services**: Danh sách Service layer được gọi
- **APIs**: Danh sách các endpoint API
- **Logic & Flow**: Chi tiết từng API (HTTP method, URI, arguments, returns, steps)

**Ví dụ API Definition**:
```markdown
### API ID: API-MDE-01-01-01
#### API Name: Get Idle Resource List
- HTTP Method: GET
- URI: /api/idle-resources
- Arguments: query, department, status
- Returns: resourceList
```

### 5. Service Design (`03-service/SVE-MDE-XX-YY.md`)

**Mục đích**: Thiết kế logic nghiệp vụ, xử lý business rules

**Cấu trúc document**:
- **Used DAOs**: Danh sách DAO được service gọi
- **Services**: Danh sách các service methods
- **Logic & Flow**: Chi tiết logic xử lý của từng service

**Đặc điểm**: 
- Chứa business logic validation
- Orchestrate việc gọi nhiều DAO
- Transform data giữa API và DAO layer

### 6. DAO Design (`04-dao/DAO-MDE-XX-YY.md`)

**Mục đích**: Thiết kế tầng truy cập dữ liệu, thao tác trực tiếp với database

**Cấu trúc document**:
- **DAOs**: Danh sách các DAO methods
- **Logic & Flow**: Chi tiết SQL queries và database operations

**Ví dụ DAO Method**:
```markdown
### DAO ID: DAO-MDE-01-01-01
#### DAO Name: Get Idle Resource List DAO
- SQL: SELECT * FROM idle_resources WHERE (name LIKE ? OR email LIKE ?)
- Arguments: query, department, status
- Returns: resourceList
```

## Quy tắc đặt tên

### Module Naming
- **MDE-XX**: Module Design (XX = số thứ tự module)
- Ví dụ: MDE-01 (Resource Management), MDE-02 (User Management)

### File Naming Convention
- **Screen**: `SCR-MDE-XX-YY.md`
- **API**: `API-MDE-XX-YY.md` 
- **Service**: `SVE-MDE-XX-YY.md`
- **DAO**: `DAO-MDE-XX-YY.md`

Trong đó:
- XX = Module number
- YY = Component number trong module

### ID Naming trong documents
- **Screen Items**: `ITEM-01`, `ITEM-02`...
- **Events**: `EVT-01`, `EVT-02`...
- **APIs**: `API-MDE-XX-YY-ZZ`
- **Services**: `SVE-MDE-XX-YY-ZZ`
- **DAOs**: `DAO-MDE-XX-YY-ZZ`

## Luồng dữ liệu giữa các tầng

```
Screen (UI) 
    ↓ User Action/Event
API (Controller)
    ↓ Business Request
Service (Business Logic)
    ↓ Data Request
DAO (Data Access)
    ↓ SQL Query
Database
```

### Mối quan hệ Dependencies:
- **Screen** → **API**: Screen gọi API thông qua HTTP requests
- **API** → **Service**: API gọi Service methods để xử lý business logic
- **Service** → **DAO**: Service gọi DAO methods để truy cập dữ liệu
- **DAO** → **Database**: DAO thực thi SQL queries

## Mẫu document structure chung

Mỗi file DD đều có cấu trúc:

```markdown
# Cover
- Document ID: [ID]
- Document Name: [Name]

## History
| No | Date | Account | Action | Impacted Section | Description |

## [Specific Sections based on layer]
- Used APIs/Services/DAOs
- Main Content (Screen Layout/APIs/Services/DAOs)
- Logic & Flow details
```

## Best Practices

1. **Consistency**: Giữ nhất quán format và naming convention
2. **Traceability**: Mỗi component phải reference đến component phụ thuộc
3. **Completeness**: Mỗi method/API phải có đầy đủ arguments, returns, validation
4. **Maintainability**: History section để track changes theo thời gian
5. **Clarity**: Description rõ ràng cho từng component và business logic

Cấu trúc này đảm bảo hệ thống có thể scale, maintain và các developer có thể hiểu rõ architecture tổng thể cũng như chi tiết implementation.