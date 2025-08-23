# DAO-MDE-01-01: User Authentication DAO

## Cover
- **Document ID**: DAO-MDE-01-01
- **Document Name**: User Authentication DAO

## History

| No | Date       | Version | Account | Action     | Impacted Section | Description                           |
|----|------------|---------|---------|------------|------------------|---------------------------------------|
| 1  | 2024-Dec-27| v0.1    | system  | Initialize | Whole Document   | Initial creation of User Authentication DAO detailed design |

## DAOs

| No | ID             | Name                | Description                                    |
|----|----------------|---------------------|------------------------------------------------|
| 1  | DAO-MDE-01-01-01 | User Authentication DAO | Database operations for user credential validation and authentication data |

## Logic & Flow

### DAO ID: DAO-MDE-01-01-01
### DAO Name: User Authentication DAO

#### Arguments:
| No | Name       | Data Type | Constraint                    | Description                      |
|----|------------|-----------|-------------------------------|----------------------------------|
| 1  | username   | String    | Required, Max 100 characters  | Username or email for lookup     |
| 2  | userId     | String    | Required for user operations  | User unique identifier           |
| 3  | password   | String    | Required for updates          | New password hash                |
| 4  | loginTime  | DateTime  | Required for login updates    | Login timestamp                  |
| 5  | operation  | String    | Required, Enum values         | Database operation type          |

#### Returns:
| No | Name           | Data Type | Description                        |
|----|----------------|-----------|------------------------------------| 
| 1  | success        | Boolean   | Operation success indicator        |
| 2  | userExists     | Boolean   | User existence indicator           |
| 3  | userId         | String    | User unique identifier             |
| 4  | hashedPassword | String    | Stored password hash               |
| 5  | userProfile    | Object    | User profile information           |
| 6  | roles          | Array     | User assigned roles                |
| 7  | permissions    | Array     | User permissions list              |
| 8  | isActive       | Boolean   | Account active status              |
| 9  | lastLoginTime  | DateTime  | Previous login timestamp           |
| 10 | department     | Object    | User department information        |

#### Steps:
1. **Step 1: Get User Credentials Operation**
   - **Description**: Retrieve user credentials and basic profile information
   - **Data Validation**: Validate username format (email or username pattern)
   - **SQL Call**: 
     - **SQL**: 
       ```sql
       SELECT 
           u.user_id,
           u.username,
           u.email,
           u.password_hash,
           u.is_active,
           u.last_login_time,
           u.created_time,
           u.language_preference,
           p.first_name,
           p.last_name,
           p.phone_number,
           d.department_id,
           d.department_name
       FROM users u
       LEFT JOIN profiles p ON u.user_id = p.user_id
       LEFT JOIN departments d ON u.department_id = d.department_id
       WHERE (u.username = ? OR u.email = ?)
       AND u.is_deleted = false
       ```
     - **Arguments**:
       | Name     | Value              | Description                    |
       |----------|--------------------|--------------------------------|
       | username | ARGUMENT.username  | Username for lookup            |
       | email    | ARGUMENT.username  | Email for lookup (same value)  |
     - **Returns**:
       | Name           | Description                        |
       |----------------|------------------------------------| 
       | user_id        | User unique identifier             |
       | username       | Username                           |
       | email          | User email address                 |
       | password_hash  | Stored password hash               |
       | is_active      | Account active status              |
       | last_login_time| Previous login timestamp           |
       | first_name     | User first name                    |
       | last_name      | User last name                     |
       | department_id  | Department identifier              |
       | department_name| Department name                    |
     - **Callback**: Return user credentials and profile information if found

2. **Step 2: Get User Roles Operation**
   - **Description**: Retrieve user roles and permissions for authorization
   - **Data Validation**: Verify userId is provided
   - **SQL Call**:
     - **SQL**: 
       ```sql
       SELECT 
           r.role_id,
           r.role_name,
           r.role_description,
           ur.assigned_date,
           STRING_AGG(p.permission_name, ',') as permissions
       FROM user_roles ur
       INNER JOIN roles r ON ur.role_id = r.role_id
       LEFT JOIN role_permissions rp ON r.role_id = rp.role_id
       LEFT JOIN permissions p ON rp.permission_id = p.permission_id
       WHERE ur.user_id = ?
       AND ur.is_active = true
       AND r.is_active = true
       GROUP BY r.role_id, r.role_name, r.role_description, ur.assigned_date
       ORDER BY ur.assigned_date
       ```
     - **Arguments**:
       | Name   | Value            | Description                    |
       |--------|------------------|--------------------------------|
       | userId | ARGUMENT.userId  | User ID for role lookup        |
     - **Returns**:
       | Name            | Description                        |
       |-----------------|------------------------------------| 
       | role_id         | Role unique identifier             |
       | role_name       | Role name                          |
       | role_description| Role description                   |
       | assigned_date   | Role assignment date               |
       | permissions     | Comma-separated permissions        |
     - **Callback**: Return user roles and associated permissions

3. **Step 3: Update Last Login Operation**
   - **Description**: Update user's last login timestamp for audit purposes
   - **Data Validation**: Verify userId and loginTime are provided
   - **SQL Call**:
     - **SQL**: 
       ```sql
       UPDATE users 
       SET 
           last_login_time = ?,
           login_count = login_count + 1,
           updated_time = CURRENT_TIMESTAMP
       WHERE user_id = ?
       AND is_active = true
       ```
     - **Arguments**:
       | Name      | Value              | Description                    |
       |-----------|--------------------|--------------------------------|
       | loginTime | ARGUMENT.loginTime | Current login timestamp        |
       | userId    | ARGUMENT.userId    | User ID to update              |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | affected_rows| Number of rows updated             |
     - **Callback**: Return update success confirmation

4. **Step 4: Update Password Operation**
   - **Description**: Update user password hash in the database
   - **Data Validation**: Verify userId and password hash are provided
   - **SQL Call**:
     - **SQL**: 
       ```sql
       UPDATE users 
       SET 
           password_hash = ?,
           password_updated_time = CURRENT_TIMESTAMP,
           updated_time = CURRENT_TIMESTAMP
       WHERE user_id = ?
       AND is_active = true
       ```
     - **Arguments**:
       | Name     | Value             | Description                    |
       |----------|-------------------|--------------------------------|
       | password | ARGUMENT.password | New password hash              |
       | userId   | ARGUMENT.userId   | User ID to update              |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | affected_rows| Number of rows updated             |
     - **Callback**: Return password update confirmation

5. **Step 5: Validate User Existence Operation**
   - **Description**: Check if user exists without returning sensitive information
   - **Data Validation**: Validate username format
   - **SQL Call**:
     - **SQL**: 
       ```sql
       SELECT 
           user_id,
           username,
           email,
           is_active
       FROM users 
       WHERE (username = ? OR email = ?)
       AND is_deleted = false
       ```
     - **Arguments**:
       | Name     | Value              | Description                    |
       |----------|--------------------|--------------------------------|
       | username | ARGUMENT.username  | Username for existence check   |
       | email    | ARGUMENT.username  | Email for existence check      |
     - **Returns**:
       | Name      | Description                        |
       |-----------|------------------------------------| 
       | user_id   | User unique identifier             |
       | username  | Username                           |
       | email     | User email address                 |
       | is_active | Account active status              |
     - **Callback**: Return user existence and basic status information

6. **Final Step**: Return operation-specific database results with user authentication data, profile information, roles, or update confirmations based on the requested operation
