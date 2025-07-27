# DAO Parsing Techniques

## 📋 Overview
This document provides detailed techniques for parsing DAO specification files and extracting business logic for Django model implementation.

## 🔍 DAO File Structure Understanding

### Standard DAO Document Format
```markdown
# DAO-MDE-XX-YY: [DAO Name]

## Cover
- Document ID, Name, Version, etc.

## History
- Change tracking table

## DAOs
- List of DAO operations in this file

## Logic & Flow
### DAO ID: DAO-MDE-XX-YY-ZZ
### DAO Name: [Operation Name]

#### Arguments:
| No | Name | Data Type | Constraint | Description |

#### Returns:
| No | Name | Data Type | Description |

#### Steps:
1. **Step 1: [Step Name]**
   - **Description**: [What this step does]
   - **Data Validation**: [Validation rules]
   - **SQL Call**: 
     - **SQL**: [Actual SQL query]
     - **Arguments**: [Parameter mapping]
     - **Returns**: [Return value mapping]
     - **Callback**: [Next action]
```

## ⚙️ Parsing Techniques

### 1. Extract DAO Operations List
```bash
# Extract all DAO operations from the DAOs table
awk '/^## DAOs/,/^## Logic & Flow/ {
    if (/^\|.*\|.*DAO.*\|/) {
        gsub(/^\| *| *\|$/, "");
        split($0, fields, " *\\| *");
        if (fields[2] != "ID" && fields[2] != "---") {
            print "DAO_ID: " fields[2];
            print "DAO_NAME: " fields[3];
            print "DESCRIPTION: " fields[4];
            print "---";
        }
    }
}' "$dao_file"
```

### 2. Extract Individual DAO Operation Details
```bash
# Parse each DAO operation section
awk '/^### DAO ID:/ {
    dao_id = $3
    getline; dao_name = substr($0, 16)  # Remove "### DAO Name: "
    
    print "=== DAO OPERATION ==="
    print "ID: " dao_id
    print "Name: " dao_name
    
    # Extract arguments
    while (getline && !/^#### Returns:/) {
        if (/^\| [0-9]+ \|.*\|.*\|.*\|/) {
            gsub(/^\| *[0-9]+ *\| */, "");
            gsub(/ *\|$/, "");
            split($0, fields, " *\\| *");
            if (fields[1] != "Name" && fields[1] != "---") {
                print "ARG: " fields[1] " (" fields[2] ") - " fields[4];
            }
        }
    }
    
    # Extract returns
    while (getline && !/^#### Steps:/) {
        if (/^\| [0-9]+ \|.*\|.*\|/) {
            gsub(/^\| *[0-9]+ *\| */, "");
            gsub(/ *\|$/, "");
            split($0, fields, " *\\| *");
            if (fields[1] != "Name" && fields[1] != "---") {
                print "RETURN: " fields[1] " (" fields[2] ") - " fields[3];
            }
        }
    }
    
    # Extract steps
    step_count = 0
    while (getline && !/^---/ && !/^### DAO ID:/) {
        if (/^\*\*Step [0-9]+:/) {
            step_count++
            gsub(/^\*\*Step [0-9]+: */, "");
            gsub(/\*\*$/, "");
            print "STEP_" step_count ": " $0
        }
    }
    print ""
}' "$dao_file"
```

### 3. Extract SQL Queries and Business Logic
```bash
# Extract SQL queries with context
grep -A 10 -B 2 "SQL.*:" "$dao_file" | while IFS= read -r line; do
    if [[ "$line" =~ "SQL".*":" ]]; then
        echo "SQL_CONTEXT: $line"
    elif [[ "$line" =~ "SELECT|INSERT|UPDATE|DELETE" ]]; then
        echo "SQL_QUERY: $line"
    elif [[ "$line" =~ "Arguments:" ]]; then
        echo "SQL_ARGS_SECTION: $line"
    elif [[ "$line" =~ "Returns:" ]]; then
        echo "SQL_RETURNS_SECTION: $line"
    fi
done
```

### 4. Extract Business Rules and Validation
```bash
# Extract validation rules and business logic
grep -E "Data Validation|Business Rules|Constraint" "$dao_file" | while IFS= read -r line; do
    echo "BUSINESS_RULE: $line"
done

# Extract constraint information from arguments table
awk '/#### Arguments:/,/#### Returns:/ {
    if (/^\|.*\|.*\|.*Required.*\|/ || /^\|.*\|.*\|.*Optional.*\|/) {
        print "CONSTRAINT: " $0
    }
}' "$dao_file"
```

## 🔄 SQL to Django ORM Conversion

### Common SQL Pattern Conversions

#### 1. Simple SELECT with WHERE
```sql
-- DAO SQL
SELECT user_id, username, email FROM users WHERE username = ? AND is_active = true

-- Django ORM Equivalent
User.objects.filter(username=username, is_active=True).values('user_id', 'username', 'email')
```

#### 2. JOIN Operations
```sql
-- DAO SQL
SELECT u.user_id, u.username, p.first_name, p.last_name 
FROM users u 
LEFT JOIN profiles p ON u.user_id = p.user_id 
WHERE u.username = ?

-- Django ORM Equivalent
User.objects.select_related('profile').filter(username=username)
```

#### 3. Complex Aggregations
```sql
-- DAO SQL
SELECT COUNT(*) as total_count, AVG(hourly_rate) as avg_rate 
FROM idle_resources 
WHERE status = 'available'

-- Django ORM Equivalent
IdleResource.objects.filter(status='available').aggregate(
    total_count=Count('*'),
    avg_rate=Avg('hourly_rate')
)
```

### Advanced Conversion Patterns

#### 1. Dynamic WHERE Clauses
```python
# DAO Pattern: Dynamic filtering based on criteria
def build_dynamic_filter(filter_criteria):
    queryset = IdleResource.objects.all()
    
    if 'status' in filter_criteria:
        queryset = queryset.filter(status=filter_criteria['status'])
    
    if 'department_id' in filter_criteria:
        queryset = queryset.filter(department_id=filter_criteria['department_id'])
    
    if 'resource_type' in filter_criteria:
        queryset = queryset.filter(resource_type=filter_criteria['resource_type'])
    
    return queryset
```

#### 2. Pagination Implementation
```python
# DAO Pattern: LIMIT and OFFSET conversion
def apply_pagination(queryset, pagination_info):
    limit = pagination_info.get('limit', 20)
    offset = pagination_info.get('offset', 0)
    
    total_count = queryset.count()
    results = list(queryset[offset:offset + limit])
    
    return {
        'results': results,
        'total_count': total_count,
        'has_next': total_count > (offset + limit)
    }
```

## 🎯 Business Logic Extraction

### 1. Validation Rule Extraction
```python
def extract_validation_rules(dao_arguments):
    """Extract validation rules from DAO argument specifications."""
    rules = {}
    
    for arg in dao_arguments:
        if 'Required' in arg['constraint']:
            rules[arg['name']] = {'required': True}
        
        if 'Max' in arg['constraint']:
            max_length = re.search(r'Max (\d+)', arg['constraint'])
            if max_length:
                rules[arg['name']]['max_length'] = int(max_length.group(1))
    
    return rules
```

### 2. Method Generation from DAO Steps
```python
def generate_method_from_dao_steps(dao_operation):
    """Generate Django model method from DAO operation steps."""
    
    method_name = dao_operation['name'].lower().replace(' ', '_')
    arguments = dao_operation['arguments']
    steps = dao_operation['steps']
    
    # Generate method signature
    args_signature = ', '.join([f"{arg['name']}" for arg in arguments])
    
    # Generate method body from steps
    method_body = []
    for step in steps:
        if 'SQL' in step:
            orm_code = convert_sql_to_orm(step['sql'])
            method_body.append(orm_code)
        
        if 'Validation' in step:
            validation_code = generate_validation(step['validation'])
            method_body.append(validation_code)
    
    return f"""
def {method_name}(self, {args_signature}):
    \"\"\"
    {dao_operation['description']}
    
    Source: {dao_operation['dao_id']}
    \"\"\"
    {chr(10).join(method_body)}
"""
```

## 📊 Table Reference Extraction

### 1. Extract Table Names from SQL
```bash
# Extract all table references from DAO files
extract_table_references() {
    local dao_file="$1"
    
    # Extract FROM clauses
    grep -o "FROM [a-z_][a-z0-9_]*" "$dao_file" | cut -d' ' -f2
    
    # Extract JOIN clauses
    grep -o "JOIN [a-z_][a-z0-9_]*" "$dao_file" | cut -d' ' -f2
    
    # Extract INSERT INTO
    grep -o "INTO [a-z_][a-z0-9_]*" "$dao_file" | cut -d' ' -f2
    
    # Extract UPDATE tables
    grep -o "UPDATE [a-z_][a-z0-9_]*" "$dao_file" | cut -d' ' -f2
}
```

### 2. Map Tables to Django Apps
```python
def map_tables_to_apps(table_references, app_mapping):
    """Map database tables to Django apps based on business logic."""
    
    table_app_map = {}
    
    for table in table_references:
        # Authentication tables
        if table in ['users', 'profiles', 'departments', 'roles', 'permissions']:
            table_app_map[table] = 'authentication'
        
        # Resource management tables
        elif table in ['idle_resources', 'import_sessions', 'export_sessions']:
            table_app_map[table] = 'resource_management'
        
        # Configuration tables
        elif 'config' in table or 'preference' in table or 'setting' in table:
            table_app_map[table] = 'config'
        
        # Default assignment
        else:
            table_app_map[table] = 'core'
    
    return table_app_map
```

## 🔧 Automated Parsing Pipeline

### Complete DAO Processing Script
```bash
#!/bin/bash
# Complete DAO parsing pipeline

process_dao_files() {
    local dao_directories="$1"
    local output_dir="$2"
    
    mkdir -p "$output_dir"
    
    # Process each DAO directory
    IFS=',' read -ra DAO_DIRS <<< "$dao_directories"
    
    for dao_dir in "${DAO_DIRS[@]}"; do
        echo "Processing DAO directory: $dao_dir"
        
        # Find all DAO files in directory
        find "$dao_dir" -name "DAO-MDE-*-*_v*.md" | while read dao_file; do
            echo "  Processing file: $dao_file"
            
            # Extract operations
            extract_dao_operations "$dao_file" > "$output_dir/operations_$(basename "$dao_file" .md).txt"
            
            # Extract SQL queries
            extract_sql_queries "$dao_file" > "$output_dir/sql_$(basename "$dao_file" .md).txt"
            
            # Extract business rules
            extract_business_rules "$dao_file" > "$output_dir/rules_$(basename "$dao_file" .md).txt"
        done
    done
    
    echo "DAO processing completed. Results in: $output_dir"
}
```

This comprehensive parsing system enables automatic extraction of all necessary information from DAO files for Django model generation.