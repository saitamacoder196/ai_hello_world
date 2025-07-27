# Prompt 1.2.3: DAO Content Discovery & Parsing

## 🎯 Objective
Dynamically discover all DAO specification files and parse their content to extract database operations, business logic, and method specifications for Django model enhancement.

## 🧠 Chain of Thought Process

### Step 1: Dynamic DAO File Discovery
**Reasoning**: DAO files contain business logic and database operations that must be converted to Django model methods. I need to find all files regardless of quantity or structure.

**Actions to take**:
1. Scan all DAO directories found in previous step
2. Catalog DAO files with their module assignments
3. Extract DAO operation IDs and descriptions
4. Validate file accessibility and format

### Step 2: DAO Content Structure Analysis
**Reasoning**: Each DAO file contains multiple operations with specific formats. I need to parse the structured content to extract meaningful information.

**Actions to take**:
1. Parse DAO operation sections
2. Extract arguments, returns, and steps
3. Identify SQL queries and business logic
4. Map operations to database tables

### Step 3: Business Logic Extraction
**Reasoning**: DAO specifications contain validation rules, workflow logic, and method implementations that should be preserved in Django models.

**Actions to take**:
1. Extract validation rules and constraints
2. Parse SQL queries for Django ORM conversion
3. Identify custom method requirements
4. Document business rule dependencies

## 📥 Input Variables

### Required Variables
- **`${input:dao_directories}`**: Comma-separated DAO directory paths
  - Example: `/DD/MDE-01/04-dao,/DD/MDE-03/04-dao`
  - Source: Output from Prompt 1.2.1

### Optional Variables
- **`${input:dao_file_pattern}`**: Pattern for DAO file matching
  - Default: `DAO-MDE-*-*_v*.md`
- **`${input:business_logic_extraction}`**: Level of business logic to extract
  - Default: `full`
  - Options: `minimal`, `standard`, `full`

## 🔧 Execution Steps

### Step 1: DAO File Discovery
```bash
echo "🔍 Step 1: Dynamic DAO file discovery..."

DAO_DIRS="${input:dao_directories}"
IFS=',' read -ra DAO_DIR_ARRAY <<< "$DAO_DIRS"

echo "📁 Processing DAO directories:"
for dao_dir in "${DAO_DIR_ARRAY[@]}"; do
    echo "  - $dao_dir"
done

# Discover all DAO files
echo "📄 DAO files discovered:"
DAO_FILES=""
for dao_dir in "${DAO_DIR_ARRAY[@]}"; do
    if [ -d "$dao_dir" ]; then
        echo "🗂️ Directory: $dao_dir"
        current_files=$(find "$dao_dir" -name "DAO-MDE-*-*_v*.md" -type f 2>/dev/null)
        for file in $current_files; do
            dao_id=$(basename "$file" .md)
            module_id=$(echo "$dao_id" | grep -o "MDE-[0-9]\+")
            sequence_id=$(echo "$dao_id" | grep -o "DAO-MDE-[0-9]\+-[0-9]\+")
            echo "  ✅ $dao_id (Module: $module_id)"
            DAO_FILES="$DAO_FILES $file"
        done
    else
        echo "  ❌ Directory not found: $dao_dir"
    fi
done

echo "📊 Total DAO files found: $(echo $DAO_FILES | wc -w)"
```

### Step 2: DAO Content Parsing
```bash
echo "🔍 Step 2: Parsing DAO content structure..."

# Parse each DAO file
for dao_file in $DAO_FILES; do
    echo "📋 Processing: $(basename "$dao_file")"
    
    # Extract document metadata
    echo "  📄 Document info:"
    grep -E "Document ID|Document Name|Module" "$dao_file" | head -3
    
    # Extract DAO operations list
    echo "  🔧 DAO operations:"
    awk '/^## DAOs/,/^## Logic & Flow/ {
        if (/^\|.*\|.*DAO.*\|/) {
            gsub(/^\| *| *\|$/, "");
            print "    - " $0
        }
    }' "$dao_file"
    
    # Extract table references from SQL
    echo "  🗃️ Table references:"
    grep -o "FROM [a-z_]\+\|JOIN [a-z_]\+\|INTO [a-z_]\+\|UPDATE [a-z_]\+" "$dao_file" | \
    awk '{print $2}' | sort | uniq | head -10 | while read table; do
        echo "    - $table"
    done
    
    echo ""
done
```

### Step 3: Business Logic Analysis
```bash
echo "🔍 Step 3: Extracting business logic and operations..."

# Create comprehensive DAO operation catalog
echo "📚 DAO Operations Catalog:"
echo "========================="

for dao_file in $DAO_FILES; do
    dao_basename=$(basename "$dao_file" .md)
    module_name=$(echo "$dao_basename" | grep -o "MDE-[0-9]\+")
    
    echo "📁 Module: $module_name"
    echo "📄 File: $dao_basename"
    
    # Extract individual DAO operations
    awk '/^### DAO ID:/ {
        dao_id = $3
        getline; dao_name = substr($0, 16)  # Remove "### DAO Name: "
        
        print "  🔧 Operation: " dao_id
        print "     Name: " dao_name
        
        # Extract arguments
        while (getline && !/^### Steps:/) {
            if (/^\| [0-9]+ \|.*\| String \|/ || /^\| [0-9]+ \|.*\| Object \|/ || /^\| [0-9]+ \|.*\| Boolean \|/) {
                gsub(/^\| *[0-9]+ *\| */, "");
                gsub(/ *\|.*/, "");
                print "     Arg: " $0
            }
        }
        
        # Extract steps and SQL
        step_count = 0
        while (getline && !/^---/ && !/^### DAO ID:/) {
            if (/^\*\*Step [0-9]+:/) {
                step_count++
                gsub(/^\*\*Step [0-9]+: */, "");
                gsub(/\*\*$/, "");
                print "     Step " step_count ": " $0
            }
            if (/SELECT|INSERT|UPDATE|DELETE/) {
                print "     SQL: " substr($0, 1, 80) "..."
            }
        }
        print ""
    }' "$dao_file"
done
```

## 📤 Expected Output

### DAO Discovery & Parsing Report
```
🔍 DAO CONTENT DISCOVERY & PARSING REPORT
==========================================

📊 Discovery Summary:
   - DAO directories processed: 2
   - Total DAO files found: 13
   - DAO operations cataloged: 35
   - Modules covered: MDE-01, MDE-03

📁 Module Breakdown:
   MDE-01 (Authentication Module): 3 files, 8 operations
   ├── DAO-MDE-01-01_v0.1.md: User Authentication DAO
   │   ├── DAO-MDE-01-01-01: User Authentication DAO (5 steps)
   │   └── Tables: users, profiles, departments, user_roles, roles, permissions
   ├── DAO-MDE-01-02_v0.1.md: Session Management DAO  
   │   ├── DAO-MDE-01-02-01: Session Management DAO (8 steps)
   │   └── Tables: user_sessions, users
   └── DAO-MDE-01-03_v0.1.md: Security Policy DAO
       ├── DAO-MDE-01-03-01: Security Policy DAO (6 steps)
       └── Tables: security_policy, login_attempts, password_reset_tokens

   MDE-03 (Resource Management Module): 10 files, 27 operations
   ├── DAO-MDE-03-01_v0.1.md: Idle Resource CRUD DAO
   │   ├── DAO-MDE-03-01-01: Create Idle Resource (5 steps)
   │   ├── DAO-MDE-03-01-02: Read Idle Resource (5 steps)
   │   ├── DAO-MDE-03-01-03: Update Idle Resource (5 steps)
   │   ├── DAO-MDE-03-01-04: Delete Idle Resource (5 steps)
   │   ├── DAO-MDE-03-01-05: List Idle Resources (6 steps)
   │   └── Tables: idle_resources, employees, departments
   └── [Additional MDE-03 files...]

🔧 Business Logic Extraction:
   Authentication Operations:
   - User credential validation with profile joins
   - Role and permission management
   - Session creation and token management
   - Password reset and security policies
   
   Resource Management Operations:
   - CRUD operations with audit trails
   - Dynamic filtering and pagination
   - Import/export with validation
   - Business rule enforcement

🗃️ Table-to-Model Mapping:
   users → User model (authentication app)
   profiles → Profile model (authentication app)
   departments → Department model (authentication app)
   idle_resources → IdleResource model (resource_management app)
   import_sessions → ImportSession model (resource_management app)
   [Continue mapping...]

⚙️ Custom Method Requirements:
   User model methods:
   - authenticate_user(username, password) from DAO-MDE-01-01-01
   - update_last_login(login_time) from DAO-MDE-01-01-01
   - get_user_with_roles(username) from DAO-MDE-01-01-01
   
   IdleResource model methods:
   - create_with_validation(resource_data, user_context) from DAO-MDE-03-01-01
   - update_with_version_check(update_data, version_check) from DAO-MDE-03-01-03
   - list_with_filters(filter_criteria, pagination) from DAO-MDE-03-01-05

🎯 SQL-to-ORM Conversion Requirements:
   - Complex joins need select_related() and prefetch_related()
   - Dynamic WHERE clauses require Q objects
   - Pagination needs Django pagination classes
   - Aggregate queries need Django aggregation functions
```

## 🧩 DAO Operation Analysis

**Operation Type Distribution:**
- [ ] CRUD operations: 45% (Create, Read, Update, Delete)
- [ ] Authentication operations: 20% (Login, session, security)
- [ ] Business logic operations: 25% (Validation, workflow)
- [ ] Utility operations: 10% (Search, export, reporting)

**Complexity Assessment:**
- [ ] Simple operations (direct SQL): 60%
- [ ] Medium operations (joins, validation): 30%
- [ ] Complex operations (multi-step, transactions): 10%

## 🔄 Human Review Required

**Please review the DAO discovery and parsing results above and confirm:**

1. **✅ DAO Discovery Complete**
   - [ ] All expected DAO files found
   - [ ] Module assignments are correct
   - [ ] File accessibility verified

2. **✅ Content Parsing Accurate**
   - [ ] DAO operations extracted correctly
   - [ ] Business logic properly identified
   - [ ] Table mappings are accurate

3. **✅ Method Requirements Clear**
   - [ ] Custom method specifications understood
   - [ ] SQL-to-ORM conversion requirements noted
   - [ ] Business rule dependencies identified

## 🚀 Next Actions

**If review is successful:**
- Proceed to [Prompt 1.2.4: Model Architecture Planning](./prompt_1_2_4_architecture_planning.md)
- Use DAO analysis for Django model method generation

**If review requires adjustments:**
- Re-examine specific DAO files
- Clarify business logic extraction requirements
- Update table-to-model mappings

## 📝 Output Variables for Next Prompt
```
dao_analysis_result={
  "operations": {...},
  "business_logic": {...},
  "table_mappings": {...},
  "custom_methods": {...}
}
```

## 🔗 Related Documentation
- [DAO Parsing Techniques](../docs/dao_parsing_techniques.md)
- [Business Logic Extraction Guide](../docs/business_logic_extraction.md)