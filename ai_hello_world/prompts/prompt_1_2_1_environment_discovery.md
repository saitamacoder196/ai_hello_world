# Prompt 1.2.1: Environment Discovery & Validation

## 🎯 Objective
Discover and validate the Django project environment, locate DAO files, database design documents, and verify system readiness for model generation.

## 🧠 Chain of Thought Process

### Step 1: Initial Environment Assessment
**Reasoning**: Before any code generation, I need to understand the project structure and locate all necessary files.

**Actions to take**:
1. Verify Django project structure exists
2. Check for virtual environment activation
3. Validate Django version compatibility
4. Locate project root and key directories

### Step 2: Document Discovery
**Reasoning**: I need to find the database design and DAO specification files to understand what models to generate.

**Actions to take**:
1. Search for database design document (`database_v*.md`)
2. Discover all DAO directories (`*/04-dao/`)
3. Catalog DAO specification files
4. Verify file accessibility and readability

### Step 3: Dependency Analysis
**Reasoning**: Ensure all required packages and tools are available for Django model generation.

**Actions to take**:
1. Check Django installation and version
2. Verify required Python packages
3. Assess database connectivity options
4. Check for existing models that might conflict

## 📥 Input Variables

### Required Variables
- **`${input:project_root}`**: Absolute path to Django project root directory
  - Example: `/mnt/d/00. Workshop/ai_hello_world`
  - Validation: Must contain `manage.py` file

### Optional Variables  
- **`${input:virtual_env_path}`**: Path to virtual environment (if using)
  - Default: Auto-detect from project
- **`${input:search_paths}`**: Additional paths to search for documents
  - Default: Current directory and parent directories

## 🔧 Execution Steps

### Step 1: Project Structure Validation
```bash
echo "🔍 Step 1: Validating Django project structure..."

# Verify project root
PROJECT_ROOT="${input:project_root}"
if [ ! -f "$PROJECT_ROOT/manage.py" ]; then
    echo "❌ ERROR: manage.py not found at $PROJECT_ROOT"
    echo "Please verify PROJECT_ROOT path"
    exit 1
fi

echo "✅ Django project found at: $PROJECT_ROOT"

# Check project structure
echo "📁 Project structure:"
ls -la "$PROJECT_ROOT" | head -20

# Check for existing apps
echo "📱 Existing Django apps:"
find "$PROJECT_ROOT" -name "models.py" -not -path "*/venv/*" | while read model_file; do
    app_dir=$(dirname "$model_file")
    app_name=$(basename "$app_dir")
    echo "  - $app_name ($(dirname "$model_file"))"
done
```

### Step 2: Document Discovery
```bash
echo "🔍 Step 2: Discovering documentation files..."

# Find database design document
echo "🗃️ Searching for database design document..."
DB_DESIGN_FILES=$(find . -name "database_v*.md" -o -name "database*.md" 2>/dev/null | head -5)

if [ -z "$DB_DESIGN_FILES" ]; then
    echo "⚠️ Warning: No database design document found"
    echo "Searching in parent directories..."
    DB_DESIGN_FILES=$(find .. -name "database_v*.md" -o -name "database*.md" 2>/dev/null | head -5)
fi

echo "📄 Database design files found:"
echo "$DB_DESIGN_FILES"

# Find DAO directories
echo "🗂️ Searching for DAO directories..."
DAO_DIRS=$(find . -name "04-dao" -type d 2>/dev/null)

if [ -z "$DAO_DIRS" ]; then
    echo "⚠️ No DAO directories found in current location"
    echo "Searching in parent directories..."
    DAO_DIRS=$(find .. -name "04-dao" -type d 2>/dev/null)
fi

echo "📁 DAO directories found:"
echo "$DAO_DIRS"

# Catalog DAO files
echo "📋 DAO files catalog:"
for dao_dir in $DAO_DIRS; do
    echo "Directory: $dao_dir"
    find "$dao_dir" -name "DAO-MDE-*-*_v*.md" -type f | while read dao_file; do
        dao_id=$(basename "$dao_file" .md)
        echo "  - $dao_id: $dao_file"
    done
done
```

### Step 3: Technical Environment Check
```bash
echo "🔍 Step 3: Technical environment assessment..."

# Check Python and Django
echo "🐍 Python environment:"
python --version
python -c "import django; print(f'Django version: {django.get_version()}')" 2>/dev/null || echo "❌ Django not installed"

# Check virtual environment
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Virtual environment active: $VIRTUAL_ENV"
else
    echo "⚠️ No virtual environment detected"
fi

# Check database file
echo "🗃️ Database check:"
if [ -f "$PROJECT_ROOT/db.sqlite3" ]; then
    echo "✅ SQLite database found"
    echo "📊 Database size: $(stat -c%s "$PROJECT_ROOT/db.sqlite3") bytes"
else
    echo "ℹ️ No database file found (will be created)"
fi

# Check existing migrations
echo "📦 Existing migrations:"
find "$PROJECT_ROOT" -name "migrations" -type d | while read migrations_dir; do
    app_name=$(dirname "$migrations_dir" | xargs basename)
    migration_count=$(find "$migrations_dir" -name "*.py" ! -name "__init__.py" | wc -l)
    echo "  - $app_name: $migration_count migrations"
done
```

## 📤 Expected Output

### Environment Discovery Report
```
🔍 ENVIRONMENT DISCOVERY REPORT
=====================================

✅ Project Validation:
   - Django project root: ${input:project_root}
   - manage.py found: ✅ Yes
   - Virtual environment: ✅ Active / ⚠️ Not detected
   - Django version: 5.2.x
   - Python version: 3.x.x

📄 Documentation Files:
   - Database design: database_v0.1.md (found at: ../DD/database_v0.1.md)
   - DAO directories: 2 found
     * /DD/MDE-01/04-dao (3 DAO files)
     * /DD/MDE-03/04-dao (10 DAO files)

🎯 Ready for Next Steps:
   - Database schema parsing: ✅ Ready
   - DAO content analysis: ✅ Ready 
   - Model generation: ✅ Ready

⚠️ Warnings/Issues:
   - [List any warnings or issues found]

💾 Variables for Next Prompt:
   - db_design_file: ../DD/database_v0.1.md
   - dao_directories: /DD/MDE-01/04-dao,/DD/MDE-03/04-dao
   - project_root: ${input:project_root}
   - django_version: 5.2.x
```

## 🔄 Human Review Required

**Please review the environment discovery report above and confirm:**

1. **✅ Project structure is correct**
   - [ ] Django project root path is accurate
   - [ ] manage.py file is accessible
   - [ ] No conflicting existing models

2. **✅ Documentation files located**
   - [ ] Database design file is readable
   - [ ] DAO directories contain expected files
   - [ ] File paths are accessible

3. **✅ Technical environment ready**
   - [ ] Django version is compatible (5.0+)
   - [ ] Python environment is properly configured
   - [ ] No blocking technical issues

## 🚀 Next Actions

**If review is successful:**
- Proceed to [Prompt 1.2.2: Database Design Analysis](./prompt_1_2_2_database_analysis.md)
- Use the discovered file paths as input variables

**If review fails:**
- Address identified issues
- Re-run this prompt with corrected inputs
- Update project structure if necessary

## 🔗 Related Documentation
- [Variable Input Specifications](../docs/variable_input_specs.md)
- [Django Project Structure Guide](../docs/django_project_structure.md)