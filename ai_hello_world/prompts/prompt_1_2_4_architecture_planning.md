# Prompt 1.2.4: Model Architecture Planning

## 🎯 Objective
Plan the Django application architecture, model organization, and integration with common abstractions to create a scalable and maintainable codebase structure.

## 🧠 Chain of Thought Process

### Step 1: App Structure Analysis
**Reasoning**: Based on database schema and DAO analysis, I need to organize models into logical Django apps that reflect business domains and maintain clean separation of concerns.

**Actions to take**:
1. Review database tables and group by business domain
2. Analyze DAO operations to understand functional boundaries
3. Plan Django app structure with clear responsibilities
4. Ensure proper dependency management between apps

### Step 2: Common Abstraction Integration
**Reasoning**: The IMPLEMENTATION_ROADMAP.md defines base models and common patterns. I need to integrate these abstractions to avoid code duplication and ensure consistency.

**Actions to take**:
1. Reference common app abstractions from IMPLEMENTATION_ROADMAP.md
2. Plan base model inheritance strategy
3. Design custom manager integration
4. Plan shared utility and mixin usage

### Step 3: Model Relationship Architecture
**Reasoning**: Django model relationships must be carefully planned to avoid circular imports, maintain referential integrity, and support efficient queries.

**Actions to take**:
1. Map foreign key relationships between apps
2. Plan cross-app relationships and imports
3. Design relationship field configurations
4. Plan reverse relationship naming strategies

## 📥 Input Variables

### Required Variables
- **`${input:common_app_strategy}`**: Common app integration approach
  - Options: `full_integration`, `selective_usage`, `custom_implementation`
  - Source: IMPLEMENTATION_ROADMAP.md recommendations

### Optional Variables
- **`${input:app_naming_convention}`**: Django app naming convention
  - Default: `snake_case`
  - Options: `snake_case`, `kebab_case`
- **`${input:model_inheritance_strategy}`**: Base model inheritance approach
  - Default: `abstract_base_models`
  - Options: `abstract_base_models`, `concrete_inheritance`, `mixins`

## 🔧 Execution Steps

### Step 1: Business Domain Analysis
```bash
echo "🔍 Step 1: Analyzing business domains and app structure..."

# Review previous analysis results
echo "📊 Database Schema Summary:"
echo "   - Total tables: 69"
echo "   - Business domains identified:"
echo "     * Authentication & User Management"
echo "     * Resource Management & Operations" 
echo "     * Configuration & Settings"
echo "     * Monitoring & Performance"
echo "     * Integration & External Systems"
echo "     * Notifications & Alerts"

echo ""
echo "📁 Proposed Django App Structure:"

# Authentication app
echo "🔐 authentication/"
echo "   Purpose: User management, roles, permissions, sessions"
echo "   Tables: users, profiles, departments, roles, permissions, user_roles, user_sessions"
echo "   DAO Sources: MDE-01 (DAO-MDE-01-01, DAO-MDE-01-02, DAO-MDE-01-03)"
echo "   Models: User, Profile, Department, Role, Permission, UserRole, UserSession"
echo "   Key Features: Authentication, authorization, session management"

# Resource Management app
echo ""
echo "📦 resource_management/"
echo "   Purpose: Idle resource tracking, import/export, audit"
echo "   Tables: idle_resources, import_sessions, export_sessions, audit_trail"
echo "   DAO Sources: MDE-03 (DAO-MDE-03-01, DAO-MDE-03-04, DAO-MDE-03-05)"
echo "   Models: IdleResource, ImportSession, ExportSession, AuditEntry"
echo "   Key Features: CRUD operations, data import/export, audit logging"

# Configuration app
echo ""
echo "⚙️ config/"
echo "   Purpose: System configuration, feature toggles, user preferences"
echo "   Tables: system_configurations, feature_toggles, user_preferences"
echo "   DAO Sources: MDE-03 (DAO-MDE-03-09)"
echo "   Models: SystemConfiguration, FeatureToggle, UserPreference"
echo "   Key Features: Dynamic configuration, A/B testing, personalization"

# Additional apps...
echo ""
echo "📈 monitoring/"
echo "📢 monitoring_alerts/"
echo "🔌 integration/"
```

### Step 2: Common Abstractions Integration Planning
```bash
echo "🔍 Step 2: Planning common abstractions integration..."

COMMON_STRATEGY="${input:common_app_strategy}"
echo "📋 Common app strategy: $COMMON_STRATEGY"

echo ""
echo "🏗️ Base Model Architecture Plan:"

# Reference IMPLEMENTATION_ROADMAP.md structure
echo "📄 Base Model Classes (from common app):"
echo "   ✅ TimestampedModel: created_at, updated_at"
echo "   ✅ UUIDBaseModel: UUID primary keys"
echo "   ✅ AuditableModel: created_by, updated_by, audit fields"
echo "   ✅ SoftDeleteModel: is_deleted, deleted_at, deleted_by"
echo "   ✅ VersionedModel: version field for optimistic locking"
echo "   ✅ BaseModel: Combined all above features"

echo ""
echo "🔧 Model Inheritance Strategy:"
case $COMMON_STRATEGY in
    "full_integration")
        echo "   Strategy: Full integration with common app"
        echo "   ✅ All models inherit from BaseModel"
        echo "   ✅ Use common managers (SoftDeleteManager, ActiveManager)"
        echo "   ✅ Apply common mixins and utilities"
        ;;
    "selective_usage")
        echo "   Strategy: Selective usage of common abstractions"
        echo "   ✅ Core models inherit from BaseModel"
        echo "   ✅ Simple models use specific base classes"
        echo "   ✅ Custom implementations where needed"
        ;;
    "custom_implementation")
        echo "   Strategy: Custom implementation with common patterns"
        echo "   ✅ Custom base models following common patterns"
        echo "   ✅ Minimal dependency on common app"
        echo "   ✅ Tailored abstractions for specific needs"
        ;;
esac

echo ""
echo "📱 App Dependencies Plan:"
echo "   common → (base abstractions)"
echo "   authentication → common"
echo "   resource_management → common, authentication"  
echo "   config → common, authentication"
echo "   monitoring → common, authentication"
echo "   integration → common, authentication, config"
echo "   monitoring_alerts → common, authentication, monitoring"
```

### Step 3: Model Relationship Architecture
```bash
echo "🔍 Step 3: Planning model relationships and cross-app references..."

echo "🔗 Cross-App Relationship Mapping:"

echo ""
echo "📊 Core Relationships:"
echo "   authentication.User → config.UserPreference (One-to-Many)"
echo "   authentication.User → resource_management.IdleResource (via created_by)"
echo "   authentication.Department → resource_management.IdleResource (One-to-Many)"
echo "   authentication.User → monitoring.PerformanceAlert (via assigned_to)"

echo ""
echo "🔧 Relationship Implementation Strategy:"
echo "   ✅ Use string references for cross-app ForeignKeys"
echo "   ✅ Implement related_name consistently"
echo "   ✅ Plan reverse relationship access patterns"
echo "   ✅ Avoid circular import issues"

echo ""
echo "📝 Example Relationship Implementations:"
cat << 'EOF'
# In resource_management/models.py
class IdleResource(BaseModel):
    # String reference to avoid circular imports
    created_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.PROTECT,
        related_name='created_resources'
    )
    department = models.ForeignKey(
        'authentication.Department', 
        on_delete=models.PROTECT,
        related_name='idle_resources'
    )

# In authentication/models.py  
class User(BaseModel):
    # Reverse relationships accessible as:
    # user.created_resources.all()
    # user.preferences.all()
    pass
EOF

echo ""
echo "⚡ Query Optimization Plan:"
echo "   ✅ select_related() for ForeignKey relationships"
echo "   ✅ prefetch_related() for reverse ForeignKey and ManyToMany"
echo "   ✅ Custom QuerySets for common query patterns"
echo "   ✅ Database indexes on frequently queried fields"
```

## 📤 Expected Output

### Architecture Planning Report
```
🏗️ DJANGO MODEL ARCHITECTURE PLAN
===================================

📱 Django Application Structure:
   1. common/ (Base abstractions and utilities)
      - Base models, managers, mixins, utilities
      - No database tables (abstract models only)
      
   2. authentication/ (User management and security)
      - Models: User, Profile, Department, Role, Permission, UserRole, UserSession
      - Tables: 7 tables
      - Features: Authentication, authorization, RBAC, session management
      
   3. resource_management/ (Core business logic)
      - Models: IdleResource, ImportSession, ExportSession, AuditEntry
      - Tables: 4 primary tables + related
      - Features: Resource CRUD, data import/export, audit logging
      
   4. config/ (Configuration and settings)
      - Models: SystemConfiguration, FeatureToggle, UserPreference
      - Tables: 12 configuration-related tables
      - Features: Dynamic config, feature flags, user preferences
      
   5. monitoring/ (Performance and health)
      - Models: PerformanceMetric, HealthCheck, DiagnosticSession
      - Tables: 20 monitoring-related tables
      - Features: System monitoring, health checks, diagnostics
      
   6. integration/ (External systems)
      - Models: ExternalIntegration, SyncJob, APIOperation, Webhook
      - Tables: 9 integration tables
      - Features: API management, sync jobs, webhook handling
      
   7. monitoring_alerts/ (Notifications and alerts)
      - Models: Notification, Alert, AlertRule, NotificationSubscription
      - Tables: 10 alert/notification tables
      - Features: Alert management, notifications, subscriptions

🏗️ Base Model Integration:
   Strategy: ${input:common_app_strategy}
   
   ✅ BaseModel inheritance for all primary models
   ✅ Custom managers: SoftDeleteManager, ActiveManager
   ✅ Common mixins: AuditMixin, ValidationMixin
   ✅ Shared utilities: pagination, filtering, search

🔗 Relationship Architecture:
   Cross-App Dependencies:
   authentication ← resource_management (User, Department references)
   authentication ← config (User preferences)
   authentication ← monitoring (User assignments)
   common ← all apps (base abstractions)
   
   Key Relationships:
   - User (1) → IdleResources (N) via created_by
   - Department (1) → IdleResources (N) via department
   - User (1) → UserPreferences (N) via user_id
   - User (1) → UserSessions (N) via user_id
   - Role (N) ↔ Users (N) via UserRole junction table

📊 Implementation Priorities:
   Phase 1: common app + authentication app (core foundation)
   Phase 2: resource_management app (primary business logic)
   Phase 3: config app (system configuration)
   Phase 4: monitoring + integration + monitoring_alerts (extended features)

🎯 Code Organization Standards:
   ✅ Abstract base models in common/models.py
   ✅ App-specific models in {app}/models.py
   ✅ Custom managers in {app}/managers.py
   ✅ Model mixins in common/mixins.py
   ✅ Utilities in common/utils.py

⚙️ Custom Method Integration Plan:
   From DAO Analysis:
   - User.authenticate_user() from DAO-MDE-01-01-01
   - User.update_last_login() from DAO-MDE-01-01-01
   - IdleResource.create_with_validation() from DAO-MDE-03-01-01
   - IdleResource.list_with_filters() from DAO-MDE-03-01-05
   [30+ additional methods mapped...]

🔧 Technical Implementation Notes:
   ✅ Use string references for cross-app ForeignKeys
   ✅ Implement consistent related_name patterns  
   ✅ Plan database indexes for performance
   ✅ Design for Django admin integration
   ✅ Prepare for API serialization
```

## 🧩 Architecture Validation Checklist

**App Structure:**
- [ ] Business domain separation is logical
- [ ] App dependencies are minimal and clear
- [ ] No circular dependencies between apps
- [ ] Each app has focused responsibility

**Model Organization:**
- [ ] Base model inheritance strategy is consistent
- [ ] Common abstractions are properly utilized
- [ ] Custom managers and mixins are planned
- [ ] Relationship patterns are standardized

**Scalability Considerations:**
- [ ] Architecture supports future growth
- [ ] Performance implications are considered
- [ ] Database design is optimized
- [ ] Code reusability is maximized

## 🔄 Human Review Required

**Please review the architecture plan above and confirm:**

1. **✅ App structure is appropriate**
   - [ ] Business domain boundaries make sense
   - [ ] App responsibilities are clear and focused
   - [ ] Dependencies are minimal and logical

2. **✅ Common abstractions integration is sound**
   - [ ] Base model strategy is appropriate
   - [ ] Common app usage aligns with project needs
   - [ ] Code reusability is maximized

3. **✅ Relationship architecture is robust**
   - [ ] Cross-app relationships are well-planned
   - [ ] Performance implications are considered
   - [ ] Circular dependency issues are avoided

## 🚀 Next Actions

**If review is successful:**
- Proceed to [Prompt 1.2.5: Smart Model Generation](./prompt_1_2_5_model_generation.md)
- Use architecture plan for model code generation

**If review requires changes:**
- Adjust app structure based on feedback
- Revise relationship architecture
- Update common abstraction integration strategy

## 📝 Output Variables for Next Prompt
```
architecture_plan={
  "apps": {...},
  "relationships": {...},
  "base_models": {...},
  "implementation_order": [...]
}
```

## 🔗 Related Documentation
- [Common Model Abstractions Guide](../docs/common_model_abstractions.md)
- [Django App Architecture Best Practices](../docs/django_app_architecture.md)