# SVE-MDE-01-02: Session Management Service

## Cover
- **Document ID**: SVE-MDE-01-02
- **Document Name**: Session Management Service

## History

| No | Date       | Version | Account | Action     | Impacted Section | Description                           |
|----|------------|---------|---------|------------|------------------|---------------------------------------|
| 1  | 2024-Dec-27| v0.1    | system  | Initialize | Whole Document   | Initial creation of Session Management Service detailed design |

## Used DAOs

| No | DAO Document                          | DAO ID        | DAO Name               |
|----|---------------------------------------|---------------|------------------------|
| 1  | DAO-MDE-01-02_Session Management DAO_v0.1 | DAO-MDE-01-02-01 | Session Management DAO |

## Services

| No | ID             | Name                | Description                                    |
|----|----------------|---------------------|------------------------------------------------|
| 1  | SVE-MDE-01-02-01 | Session Management Service | Manages user sessions, token lifecycle, and security policies |

## Logic & Flow

### Service ID: SVE-MDE-01-02-01
### Service Name: Session Management Service

#### Arguments:
| No | Name        | Data Type | Constraint                    | Description                      |
|----|-------------|-----------|-------------------------------|----------------------------------|
| 1  | userId      | String    | Required when creating session| User identifier for session     |
| 2  | userProfile | Object    | Optional                      | User profile information         |
| 3  | accessToken | String    | Required for validation       | JWT access token                 |
| 4  | refreshToken| String    | Required for refresh          | JWT refresh token                |
| 5  | sessionId   | String    | Required for operations       | Session identifier               |
| 6  | rememberMe  | Boolean   | Optional, default false       | Session persistence preference   |
| 7  | operation   | String    | Required, Enum values         | Operation type (create, validate, refresh, terminate) |

#### Returns:
| No | Name         | Data Type | Description                        |
|----|--------------|-----------|------------------------------------| 
| 1  | success      | Boolean   | Operation success indicator        |
| 2  | sessionId    | String    | Session unique identifier          |
| 3  | accessToken  | String    | JWT access token                   |
| 4  | refreshToken | String    | JWT refresh token                  |
| 5  | expiresIn    | Integer   | Token expiration time in seconds   |
| 6  | sessionData  | Object    | Session information and user data  |
| 7  | message      | String    | Operation result message           |

#### Steps:
1. **Step 1:**
   - **Description**: Validate operation type and required parameters
   - **Data Validation**: Verify operation type and ensure required parameters are provided
   - **DAO Call**: None
   - **Callback**: Proceed to operation-specific logic based on operation type

2. **Step 2: Create Session Operation**
   - **Description**: Create new user session with JWT tokens
   - **Data Validation**: Verify userId and userProfile are provided
   - **DAO Call**: DAO-MDE-01-02-01 - Session Management DAO
     - **Arguments**:
       | Name        | Value               | Description                    |
       |-------------|---------------------|--------------------------------|
       | userId      | ARGUMENT.userId     | User for new session           |
       | userProfile | ARGUMENT.userProfile| User profile information       |
       | rememberMe  | ARGUMENT.rememberMe | Session persistence setting    |
       | operation   | createSession       | DAO operation type             |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | sessionId    | Generated session identifier       |
       | sessionData  | Created session information        |
       | expiryTime   | Session expiration time            |
     - **Callback**: Generate JWT tokens and return session information

3. **Step 3: Validate Session Operation**
   - **Description**: Validate existing session and access token
   - **Data Validation**: Verify access token format and signature
   - **DAO Call**: DAO-MDE-01-02-01 - Session Management DAO
     - **Arguments**:
       | Name        | Value                | Description                    |
       |-------------|----------------------|--------------------------------|
       | accessToken | ARGUMENT.accessToken | Token to validate              |
       | operation   | validateSession      | DAO operation type             |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | isValid      | Token validation result            |
       | sessionData  | Session information if valid       |
       | userId       | User ID from session               |
       | expiresIn    | Remaining token lifetime           |
     - **Callback**: Return session validation result with user information

4. **Step 4: Refresh Token Operation**
   - **Description**: Generate new access token using refresh token
   - **Data Validation**: Verify refresh token validity and expiration
   - **DAO Call**: DAO-MDE-01-02-01 - Session Management DAO
     - **Arguments**:
       | Name         | Value                 | Description                    |
       |--------------|----------------------|--------------------------------|
       | refreshToken | ARGUMENT.refreshToken | Refresh token to process       |
       | operation    | refreshSession       | DAO operation type             |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | isValid      | Refresh token validation result    |
       | sessionData  | Session information                |
       | newTokens    | Generated access and refresh tokens|
     - **Callback**: Return new tokens and updated session information

5. **Step 5: Terminate Session Operation**
   - **Description**: Invalidate session and all associated tokens
   - **Data Validation**: Verify session ownership and access rights
   - **DAO Call**: DAO-MDE-01-02-01 - Session Management DAO
     - **Arguments**:
       | Name        | Value                | Description                    |
       |-------------|----------------------|--------------------------------|
       | sessionId   | ARGUMENT.sessionId   | Session to terminate           |
       | accessToken | ARGUMENT.accessToken | Current access token           |
       | operation   | terminateSession     | DAO operation type             |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | success      | Termination operation result       |
       | message      | Termination confirmation           |
     - **Callback**: Return session termination confirmation

6. **Step 6: JWT Token Generation (for create and refresh operations)**
   - **Description**: Generate JWT access and refresh tokens with appropriate expiration
   - **Data Validation**: None
   - **DAO Call**: None
   - **Callback**: Return generated tokens with session information

7. **Final Step**: Return operation-specific result with session information, tokens, and appropriate confirmation messages
