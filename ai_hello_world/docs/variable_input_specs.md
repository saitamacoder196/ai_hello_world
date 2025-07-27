# Variable Input Specifications

## 📋 Overview
This document defines all input variables used across the modular prompt system for Django model implementation.

## 🔧 Variable Categories

### Environment Variables
- **`${input:project_root}`**
  - Type: String (absolute path)
  - Required: Yes
  - Description: Absolute path to Django project root directory
  - Example: `/mnt/d/00. Workshop/ai_hello_world`
  - Validation: Must contain `manage.py` file

- **`${input:virtual_env_path}`**
  - Type: String (absolute path)
  - Required: No
  - Description: Path to Python virtual environment
  - Default: Auto-detect from environment
  - Example: `/path/to/venv`

### Document Discovery Variables
- **`${input:db_design_file}`**
  - Type: String (file path)
  - Required: Yes
  - Source: Output from Prompt 1.2.1
  - Description: Path to database design document
  - Example: `../DD/database_v0.1.md`

- **`${input:dao_directories}`**
  - Type: String (comma-separated paths)
  - Required: Yes
  - Source: Output from Prompt 1.2.1
  - Description: Paths to DAO specification directories
  - Example: `/DD/MDE-01/04-dao,/DD/MDE-03/04-dao`

### Architecture Variables
- **`${input:common_app_strategy}`**
  - Type: String (enum)
  - Required: Yes
  - Options: `full_integration`, `selective_usage`, `custom_implementation`
  - Default: `full_integration`
  - Description: Strategy for integrating common app abstractions

- **`${input:app_naming_convention}`**
  - Type: String (enum)
  - Required: No
  - Options: `snake_case`, `kebab_case`
  - Default: `snake_case`
  - Description: Naming convention for Django apps

### Generation Variables
- **`${input:generation_strategy}`**
  - Type: String (enum)
  - Required: Yes
  - Options: `full_featured`, `minimal_viable`, `incremental`
  - Default: `full_featured`
  - Description: Approach for model generation

- **`${input:documentation_level}`**
  - Type: String (enum)
  - Required: No
  - Options: `minimal`, `standard`, `comprehensive`
  - Default: `comprehensive`
  - Description: Level of code documentation to generate

### Implementation Variables
- **`${input:deployment_settings}`**
  - Type: String (enum)
  - Required: Yes
  - Options: `development`, `staging`, `production`
  - Default: `development`
  - Description: Target deployment environment

- **`${input:run_full_tests}`**
  - Type: Boolean
  - Required: No
  - Default: `true`
  - Description: Whether to run comprehensive test suite

## 📝 Variable Usage Matrix

| Prompt | Required Variables | Optional Variables |
|--------|-------------------|-------------------|
| 1.2.1 | `project_root` | `virtual_env_path`, `search_paths` |
| 1.2.2 | `db_design_file` | `target_db_engine` |
| 1.2.3 | `dao_directories` | `dao_file_pattern`, `business_logic_extraction` |
| 1.2.4 | `common_app_strategy` | `app_naming_convention`, `model_inheritance_strategy` |
| 1.2.5 | `generation_strategy` | `include_test_models`, `documentation_level` |
| 1.2.6 | `deployment_settings` | `run_full_tests`, `create_sample_data` |

## 🔄 Variable Flow Between Prompts

```
Prompt 1.2.1 → Prompt 1.2.2:
  db_design_file, dao_directories

Prompt 1.2.2 → Prompt 1.2.3:
  schema_analysis_result

Prompt 1.2.3 → Prompt 1.2.4:
  dao_analysis_result

Prompt 1.2.4 → Prompt 1.2.5:
  architecture_plan

Prompt 1.2.5 → Prompt 1.2.6:
  generated_models
```