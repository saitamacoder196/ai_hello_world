# Prompt 1.2.2: Database Design Analysis

## 🎯 Objective
Parse and analyze the database design document to extract comprehensive schema information, relationships, and constraints for Django model generation.

## 🧠 Chain of Thought Process

### Step 1: Document Structure Analysis
**Reasoning**: Database design documents contain table definitions, but I need to understand the format and extract structured data systematically.

**Actions to take**:
1. Read and parse database design document structure
2. Identify table definitions and field specifications
3. Extract data types, constraints, and relationships
4. Validate document completeness

### Step 2: Schema Information Extraction
**Reasoning**: Django models require specific field types, relationships, and constraints that must be mapped from database specifications.

**Actions to take**:
1. Map database types to Django field types
2. Extract primary key and foreign key relationships
3. Identify indexes, constraints, and business rules
4. Document table-to-model mappings

### Step 3: Relationship Analysis
**Reasoning**: Proper Django model relationships (ForeignKey, ManyToMany, OneToOne) must be inferred from database foreign keys and junction tables.

**Actions to take**:
1. Analyze foreign key relationships
2. Identify many-to-many relationships via junction tables
3. Determine relationship cardinalities
4. Plan Django relationship field implementations

## 📥 Input Variables

### Required Variables
- **`${input:db_design_file}`**: Path to database design document
  - Example: `../DD/database_v0.1.md`
  - Source: Output from Prompt 1.2.1

### Optional Variables
- **`${input:target_db_engine}`**: Target database engine for Django
  - Default: `sqlite3`
  - Options: `postgresql`, `mysql`, `sqlite3`

## 🔧 Execution Steps

### Step 1: Database Document Analysis
```bash
echo "🔍 Step 1: Analyzing database design document..."

DB_DESIGN_FILE="${input:db_design_file}"

# Verify file exists and is readable
if [ ! -f "$DB_DESIGN_FILE" ]; then
    echo "❌ ERROR: Database design file not found: $DB_DESIGN_FILE"
    exit 1
fi

echo "✅ Database design file found: $DB_DESIGN_FILE"
echo "📄 File size: $(stat -c%s "$DB_DESIGN_FILE") bytes"

# Extract document metadata
echo "📋 Document metadata:"
head -20 "$DB_DESIGN_FILE" | grep -E "(Document ID|Document Name|Version|Date)"

# Extract table list
echo "🗃️ Tables defined in document:"
grep -E "^\|.*\|.*\|.*\|" "$DB_DESIGN_FILE" | grep -v "No.*ID.*Name" | head -20
```

### Step 2: Table Schema Extraction
```bash
echo "🔍 Step 2: Extracting table schema information..."

# Extract table definitions
echo "📊 Analyzing table structures..."

# Find table sections in document
grep -n "^###" "$DB_DESIGN_FILE" | head -10

# Extract field definitions for each table
echo "🔍 Field analysis for key tables:"

# Look for table field definitions (pipe-separated format)
awk '/^### [a-z_]+$/ {
    table = $2
    print "Table: " table
    getline
    while (getline && /^\|/) {
        if (!/^---/ && !/ID.*Name.*Data Type/) {
            print "  " $0
        }
    }
}' "$DB_DESIGN_FILE" | head -50
```

### Step 3: Relationship Mapping
```bash
echo "🔍 Step 3: Analyzing relationships and constraints..."

# Extract foreign key relationships
echo "🔗 Foreign key relationships:"
grep -i "foreign key\|references\|FK" "$DB_DESIGN_FILE" | head -20

# Look for relationship patterns in field definitions
echo "📋 Relationship analysis:"
grep -E "_id.*VARCHAR.*FK|Foreign Key.*references" "$DB_DESIGN_FILE"

# Extract primary keys
echo "🔑 Primary key analysis:"
grep -E "Primary Key.*Yes|primary_key|PK" "$DB_DESIGN_FILE" | head -10
```

## 📤 Expected Output

### Database Schema Analysis Report
```
🗃️ DATABASE SCHEMA ANALYSIS REPORT
====================================

📄 Document Information:
   - File: ${input:db_design_file}
   - Document ID: database_v0.1
   - Tables defined: 69 tables
   - Document status: ✅ Valid and complete

📊 Table Summary:
   1. idle_resources (12 fields)
      - PK: resource_id (VARCHAR 36, UUID)
      - FK: employee_id → employees(employee_id)
      - FK: department_id → departments(department_id)
      - Fields: resource_type, status, availability_start, availability_end, skills, experience_years, hourly_rate, created_by, created_at, updated_by, updated_at

   2. employees (8 fields)
      - PK: employee_id (VARCHAR 36, UUID)
      - Fields: first_name, last_name, email, department_id, hire_date, status, created_at, updated_at

   3. departments (6 fields)
      - PK: department_id (VARCHAR 36, UUID)
      - FK: parent_department → departments(department_id)
      - FK: manager → users(user_id)
      - Fields: department_name, parent_department, manager, is_active

   [Continue for all tables...]

🔗 Relationship Mapping:
   One-to-Many Relationships:
   - departments → idle_resources (department_id)
   - employees → idle_resources (employee_id)
   - users → user_sessions (user_id)
   - roles → user_roles (role_id)
   
   Many-to-Many Relationships:
   - users ↔ roles (via user_roles)
   - roles ↔ permissions (via role_permissions)
   
   One-to-One Relationships:
   - users → profiles (user_id)

🎯 Django Field Type Mapping:
   VARCHAR(36) → UUIDField (for IDs)
   VARCHAR(n) → CharField(max_length=n)
   TEXT → TextField
   BOOLEAN → BooleanField
   DATETIME → DateTimeField
   INTEGER → IntegerField
   DECIMAL → DecimalField
   JSON → JSONField

📱 Proposed Django App Structure:
   authentication/
   - User, Department, Profile, Role, Permission, UserRole, UserSession
   
   resource_management/
   - IdleResource, ImportSession, ExportSession, AuditEntry
   
   config/
   - SystemConfiguration, FeatureToggle, UserPreference
   
   monitoring/
   - PerformanceMetric, HealthCheck, DiagnosticSession
   
   integration/
   - ExternalIntegration, SyncJob, APIOperation, Webhook
   
   monitoring_alerts/
   - Notification, Alert, AlertRule
```

## 🧩 Schema Validation Checklist

**Table Analysis:**
- [ ] All tables have primary keys defined
- [ ] Foreign key relationships are clear and valid
- [ ] Data types are supported by Django
- [ ] Constraints are properly documented

**Relationship Validation:**
- [ ] One-to-many relationships identified correctly
- [ ] Many-to-many relationships have junction tables
- [ ] Circular dependencies are resolved
- [ ] Cascade behaviors are specified

**Django Compatibility:**
- [ ] Field types map to Django fields
- [ ] Relationship types are Django-compatible
- [ ] Naming conventions follow Django standards
- [ ] Index requirements are noted

## 🔄 Human Review Required

**Please review the database schema analysis above and confirm:**

1. **✅ Table structure is complete**
   - [ ] All required tables are identified
   - [ ] Field definitions are accurate
   - [ ] Primary keys are properly defined

2. **✅ Relationships are correct**
   - [ ] Foreign key mappings are accurate
   - [ ] Many-to-many relationships identified
   - [ ] Relationship cardinalities are correct

3. **✅ Django mapping is appropriate**
   - [ ] Field type mappings are suitable
   - [ ] App organization makes business sense
   - [ ] No naming conflicts exist

## 🚀 Next Actions

**If review is successful:**
- Proceed to [Prompt 1.2.3: DAO Content Discovery & Parsing](./prompt_1_2_3_dao_discovery.md)
- Use the schema analysis as input for model generation

**If review requires changes:**
- Address identified schema issues
- Update field type mappings if needed
- Reorganize app structure if necessary

## 📝 Output Variables for Next Prompt
```
schema_analysis_result={
  "tables": {...},
  "relationships": {...},
  "django_apps": {...},
  "field_mappings": {...}
}
```

## 🔗 Related Documentation
- [Django Field Type Reference](../docs/django_field_types.md)
- [Database Relationship Patterns](../docs/db_relationship_patterns.md)