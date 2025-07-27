# Chain of Thought Guidelines

## 🧠 Overview
This document provides guidelines for implementing chain of thought reasoning in the modular prompt system.

## 🎯 Chain of Thought Principles

### 1. Explicit Reasoning Steps
Each prompt must clearly articulate the reasoning behind each action:

**Example Structure:**
```
### Step X: [Action Name]
**Reasoning**: [Why this step is necessary and how it fits into the overall goal]

**Actions to take**:
1. [Specific action with clear rationale]
2. [Next action with logical connection]
3. [Follow-up action with expected outcome]
```

### 2. Progressive Complexity
Start with simple validations and build up to complex operations:

1. **Foundation**: Environment validation and basic checks
2. **Analysis**: Document parsing and content extraction  
3. **Planning**: Architecture design and relationship mapping
4. **Generation**: Code creation with business logic
5. **Implementation**: Deployment and comprehensive testing

### 3. Decision Points and Alternatives
Explicitly state decision points and reasoning for choices:

```
**Decision Point**: How to handle cross-app relationships?
**Options Considered**:
- Option A: Direct imports (Risk: circular dependencies)
- Option B: String references (Benefit: loose coupling)
- Option C: Signals/events (Complexity: high)

**Selected**: Option B - String references
**Reasoning**: Provides loose coupling while maintaining Django best practices
```

## 🔄 Human Review Integration

### Review Checkpoints
Each prompt must include explicit human review requirements:

```
## 🔄 Human Review Required

**Please review the [results] above and confirm:**

1. **✅ [Category] is [criteria]**
   - [ ] Specific checklist item
   - [ ] Another verification point
   - [ ] Final validation requirement

2. **✅ [Next category] meets [standards]**
   - [ ] Related checklist items
```

### Decision Documentation
Capture human decisions for future reference:

```
**Human Decision Log:**
- Database engine: PostgreSQL (instead of SQLite for production)
- Inheritance strategy: Abstract base models (approved)
- Documentation level: Comprehensive (confirmed)
```

## 📊 Validation Patterns

### Pre-Step Validation
Before executing any step, validate prerequisites:

```bash
echo "🔍 Step X: [Step Name]..."

# Validate inputs
if [ -z "${input:required_variable}" ]; then
    echo "❌ ERROR: Required variable not provided"
    exit 1
fi

echo "✅ Prerequisites validated"
```

### Post-Step Verification
After each step, verify expected outcomes:

```bash
# Verify step completion
if [ $? -eq 0 ]; then
    echo "✅ Step X completed successfully"
else
    echo "❌ Step X failed with exit code: $?"
    exit 1
fi
```

### Success Criteria
Define clear success criteria for each step:

```
📊 Step Success Criteria:
- [ ] All expected files found
- [ ] No parsing errors encountered
- [ ] Output format matches specification
- [ ] All validations passed
```

## 🎯 Error Handling Patterns

### Graceful Degradation
Handle missing or invalid inputs gracefully:

```bash
# Graceful handling of missing files
if [ ! -f "$REQUIRED_FILE" ]; then
    echo "⚠️ Warning: Required file not found: $REQUIRED_FILE"
    echo "🔍 Searching for alternatives..."
    # Alternative search logic
fi
```

### Error Recovery
Provide recovery options when possible:

```bash
# Error recovery example
if ! command_that_might_fail; then
    echo "❌ Primary method failed, trying alternative..."
    alternative_method || {
        echo "❌ All methods failed. Manual intervention required."
        exit 1
    }
fi
```

## 📝 Output Formatting Standards

### Consistent Status Indicators
Use consistent visual indicators:

- ✅ Success/Completed
- ❌ Error/Failed  
- ⚠️ Warning/Attention needed
- ℹ️ Information/Note
- 🔍 Processing/Analyzing
- 📊 Summary/Statistics
- 🎯 Goals/Objectives

### Structured Results
Format results consistently across prompts:

```
🔍 [OPERATION] REPORT
===================

📊 Summary:
   - Metric 1: Value
   - Metric 2: Value

✅ Successes:
   - Achievement 1
   - Achievement 2

⚠️ Warnings:
   - Warning 1 with context
   - Warning 2 with recommendation

❌ Errors:
   - Error 1 with resolution steps
```

## 🔗 Cross-Prompt Consistency

### Variable Naming
Maintain consistent variable naming across prompts:

- `${input:project_root}` (not `${input:projectRoot}`)
- `${input:db_design_file}` (not `${input:database_file}`)
- `${input:generation_strategy}` (not `${input:gen_strategy}`)

### Output Format Consistency
Ensure output variables are consistently formatted:

```javascript
// Standard output format
{
  "status": "completed|failed|pending",
  "data": {...},
  "errors": [...],
  "warnings": [...],
  "next_inputs": {...}
}
```

### Progress Tracking
Use consistent progress indicators:

```
📈 Progress: Step 3/6 (50% complete)
⏱️ Estimated time remaining: 10 minutes
🎯 Next milestone: Model generation
```