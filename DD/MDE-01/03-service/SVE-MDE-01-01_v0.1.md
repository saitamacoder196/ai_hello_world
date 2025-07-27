# SVE-MDE-01-01: Authentication Service

## Cover
- **Document ID**: SVE-MDE-01-01
- **Document Name**: Authentication Service

## History

| No | Date       | Version | Account | Action     | Impacted Section | Description                           |
|----|------------|---------|---------|------------|------------------|---------------------------------------|
| 1  | 2024-Dec-27| v0.1    | system  | Initialize | Whole Document   | Initial creation of Authentication Service detailed design |

## Used DAOs

| No | DAO Document                          | DAO ID        | DAO Name               |
|----|---------------------------------------|---------------|------------------------|
| 1  | DAO-MDE-01-01_User Authentication DAO_v0.1 | DAO-MDE-01-01-01 | User Authentication DAO |

## Services

| No | ID             | Name                | Description                                    |
|----|----------------|---------------------|------------------------------------------------|
| 1  | SVE-MDE-01-01-01 | Authentication Service | Core authentication logic with credential validation and security enforcement |

## Logic & Flow

### Service ID: SVE-MDE-01-01-01
### Service Name: Authentication Service

#### Arguments:
| No | Name       | Data Type | Constraint                    | Description                      |
|----|------------|-----------|-------------------------------|----------------------------------|
| 1  | username   | String    | Required, Max 100 characters  | Username or email address        |
| 2  | password   | String    | Required, Max 255 characters  | User password for verification   |
| 3  | language   | String    | Required, Enum values         | User language preference         |
| 4  | operation  | String    | Required, Enum values         | Operation type (authenticate, verify, update) |

#### Returns:
| No | Name         | Data Type | Description                        |
|----|--------------|-----------|------------------------------------| 
| 1  | isValid      | Boolean   | Authentication result              |
| 2  | userId       | String    | Authenticated user identifier      |
| 3  | userProfile  | Object    | User profile information           |
| 4  | roleInfo     | Object    | User roles and permissions         |
| 5  | message      | String    | Authentication result message      |
| 6  | lastLoginTime| DateTime  | Previous login timestamp           |

#### Steps:
1. **Step 1:**
   - **Description**: Validate input parameters and prepare authentication request
   - **Data Validation**: Verify username and password are provided, validate operation type
   - **DAO Call**: None
   - **Callback**: Proceed to credential validation if inputs are valid

2. **Step 2:**
   - **Description**: Retrieve user credentials and profile information
   - **Data Validation**: None
   - **DAO Call**: DAO-MDE-01-01-01 - User Authentication DAO
     - **Arguments**:
       | Name      | Value              | Description                    |
       |-----------|--------------------|--------------------------------|
       | username  | ARGUMENT.username  | Username to lookup             |
       | operation | getUserCredentials | DAO operation type             |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | userExists   | Whether user exists in system      |
       | hashedPassword| Stored password hash              |
       | userId       | User unique identifier             |
       | userProfile  | User profile information           |
       | isActive     | Account active status              |
     - **Callback**: Proceed to password verification if user exists and is active

3. **Step 3:**
   - **Description**: Verify provided password against stored hash
   - **Data Validation**: Hash password using same algorithm and compare
   - **DAO Call**: None
   - **Callback**: Proceed to role retrieval if password matches, return authentication failure if not

4. **Step 4:**
   - **Description**: Retrieve user roles and permissions for session establishment
   - **Data Validation**: None
   - **DAO Call**: DAO-MDE-01-01-01 - User Authentication DAO
     - **Arguments**:
       | Name      | Value              | Description                    |
       |-----------|--------------------|--------------------------------|
       | userId    | Previous Result    | User ID from step 2            |
       | operation | getUserRoles       | DAO operation type             |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | roles        | User assigned roles                |
       | permissions  | User permissions list              |
       | department   | User department information        |
     - **Callback**: Compile authentication result with user information and roles

5. **Step 5:**
   - **Description**: Update last login time and authentication audit trail
   - **Data Validation**: None
   - **DAO Call**: DAO-MDE-01-01-01 - User Authentication DAO
     - **Arguments**:
       | Name      | Value              | Description                    |
       |-----------|--------------------|--------------------------------|
       | userId    | Previous Result    | User ID from authentication    |
       | loginTime | Current Timestamp  | Current login time             |
       | operation | updateLastLogin    | DAO operation type             |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | success      | Update operation result            |
       | previousLogin| Previous login timestamp           |
     - **Callback**: Return complete authentication result

6. **Final Step**: Return comprehensive authentication result with user profile, roles, and session information for successful credential validation
