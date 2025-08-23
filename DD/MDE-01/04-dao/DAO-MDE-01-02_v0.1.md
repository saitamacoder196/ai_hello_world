# DAO-MDE-01-02: Session Management DAO

## Cover
- **Document ID**: DAO-MDE-01-02
- **Document Name**: Session Management DAO

## History

| No | Date       | Version | Account | Action     | Impacted Section | Description                           |
|----|------------|---------|---------|------------|------------------|---------------------------------------|
| 1  | 2024-Dec-27| v0.1    | system  | Initialize | Whole Document   | Initial creation of Session Management DAO detailed design |

## DAOs

| No | ID             | Name                | Description                                    |
|----|----------------|---------------------|------------------------------------------------|
| 1  | DAO-MDE-01-02-01 | Session Management DAO | Session data persistence and retrieval operations |

## Logic & Flow

### DAO ID: DAO-MDE-01-02-01
### DAO Name: Session Management DAO

#### Arguments:
| No | Name         | Data Type | Constraint                    | Description                      |
|----|--------------|-----------|-------------------------------|----------------------------------|
| 1  | userId       | String    | Required for session creation | User identifier                  |
| 2  | sessionId    | String    | Required for operations       | Session unique identifier        |
| 3  | accessToken  | String    | Required for validation       | JWT access token                 |
| 4  | refreshToken | String    | Required for refresh          | JWT refresh token                |
| 5  | userProfile  | Object    | Required for creation         | User profile information         |
| 6  | rememberMe   | Boolean   | Optional, default false       | Session persistence preference   |
| 7  | ipAddress    | String    | Optional                      | Client IP address                |
| 8  | userAgent    | String    | Optional                      | Client user agent string        |
| 9  | operation    | String    | Required, Enum values         | Database operation type          |

#### Returns:
| No | Name         | Data Type | Description                        |
|----|--------------|-----------|------------------------------------| 
| 1  | success      | Boolean   | Operation success indicator        |
| 2  | sessionId    | String    | Session unique identifier          |
| 3  | sessionData  | Object    | Session information                |
| 4  | isValid      | Boolean   | Session validation result          |
| 5  | userId       | String    | User identifier from session       |
| 6  | expiresIn    | Integer   | Session expiration time            |
| 7  | tokenHash    | String    | Token hash for storage             |
| 8  | createdTime  | DateTime  | Session creation timestamp         |
| 9  | lastActivity | DateTime  | Last session activity time         |

#### Steps:
1. **Step 1: Create Session Operation**
   - **Description**: Create new user session record in database
   - **Data Validation**: Verify userId and userProfile are provided, generate unique sessionId
   - **SQL Call**: 
     - **SQL**: 
       ```sql
       INSERT INTO user_sessions (
           session_id,
           user_id,
           access_token_hash,
           refresh_token_hash,
           ip_address,
           user_agent,
           remember_me,
           created_time,
           last_activity_time,
           expires_at,
           is_active
       ) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, true)
       ```
     - **Arguments**:
       | Name              | Value                    | Description                    |
       |-------------------|--------------------------|--------------------------------|
       | sessionId         | Generated UUID           | Unique session identifier      |
       | userId            | ARGUMENT.userId          | User creating session          |
       | accessTokenHash   | Hashed Access Token      | Secure token hash              |
       | refreshTokenHash  | Hashed Refresh Token     | Secure refresh token hash      |
       | ipAddress         | ARGUMENT.ipAddress       | Client IP address              |
       | userAgent         | ARGUMENT.userAgent       | Client user agent              |
       | rememberMe        | ARGUMENT.rememberMe      | Session persistence setting    |
       | expiresAt         | Calculated Expiry        | Session expiration time        |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | affected_rows| Number of rows inserted            |
     - **Callback**: Return session creation confirmation with session details

2. **Step 2: Validate Session Operation**
   - **Description**: Validate existing session using access token
   - **Data Validation**: Verify access token format and extract session information
   - **SQL Call**:
     - **SQL**: 
       ```sql
       SELECT 
           s.session_id,
           s.user_id,
           s.created_time,
           s.last_activity_time,
           s.expires_at,
           s.remember_me,
           s.ip_address,
           u.username,
           u.email,
           u.is_active as user_active
       FROM user_sessions s
       INNER JOIN users u ON s.user_id = u.user_id
       WHERE s.access_token_hash = ?
       AND s.is_active = true
       AND s.expires_at > CURRENT_TIMESTAMP
       AND u.is_active = true
       ```
     - **Arguments**:
       | Name            | Value                     | Description                    |
       |-----------------|---------------------------|--------------------------------|
       | accessTokenHash | Hash of access token      | Hashed token for lookup        |
     - **Returns**:
       | Name              | Description                        |
       |-------------------|------------------------------------| 
       | session_id        | Session identifier                 |
       | user_id           | User identifier                    |
       | created_time      | Session creation time              |
       | last_activity_time| Last activity timestamp            |
       | expires_at        | Session expiration time            |
       | remember_me       | Session persistence setting       |
       | username          | Username from session              |
       | email             | User email                         |
       | user_active       | User account status                |
     - **Callback**: Return session validation result with user information

3. **Step 3: Refresh Session Operation**
   - **Description**: Validate refresh token and generate new session tokens
   - **Data Validation**: Verify refresh token validity and expiration
   - **SQL Call**:
     - **SQL**: 
       ```sql
       SELECT 
           session_id,
           user_id,
           expires_at,
           remember_me
       FROM user_sessions 
       WHERE refresh_token_hash = ?
       AND is_active = true
       AND expires_at > CURRENT_TIMESTAMP
       ```
     - **Arguments**:
       | Name             | Value                     | Description                    |
       |------------------|---------------------------|--------------------------------|
       | refreshTokenHash | Hash of refresh token     | Hashed refresh token for lookup|
     - **Returns**:
       | Name       | Description                        |
       |------------|------------------------------------|
       | session_id | Session identifier                 |
       | user_id    | User identifier                    |
       | expires_at | Current session expiration         |
       | remember_me| Session persistence setting       |
     - **Callback**: Proceed to update session with new tokens if valid

4. **Step 4: Update Session Tokens Operation**
   - **Description**: Update session with new access and refresh tokens
   - **Data Validation**: Verify sessionId and new token hashes are provided
   - **SQL Call**:
     - **SQL**: 
       ```sql
       UPDATE user_sessions 
       SET 
           access_token_hash = ?,
           refresh_token_hash = ?,
           last_activity_time = CURRENT_TIMESTAMP,
           expires_at = ?
       WHERE session_id = ?
       AND is_active = true
       ```
     - **Arguments**:
       | Name              | Value                     | Description                    |
       |-------------------|---------------------------|--------------------------------|
       | newAccessHash     | New access token hash     | Updated access token hash      |
       | newRefreshHash    | New refresh token hash    | Updated refresh token hash     |
       | newExpiresAt      | Updated expiration time   | New session expiration         |
       | sessionId         | ARGUMENT.sessionId        | Session to update              |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | affected_rows| Number of rows updated             |
     - **Callback**: Return token update confirmation

5. **Step 5: Terminate Session Operation**
   - **Description**: Invalidate session and mark as inactive
   - **Data Validation**: Verify sessionId is provided
   - **SQL Call**:
     - **SQL**: 
       ```sql
       UPDATE user_sessions 
       SET 
           is_active = false,
           terminated_time = CURRENT_TIMESTAMP,
           termination_reason = 'User Logout'
       WHERE session_id = ?
       AND is_active = true
       ```
     - **Arguments**:
       | Name      | Value               | Description                    |
       |-----------|---------------------|--------------------------------|
       | sessionId | ARGUMENT.sessionId  | Session to terminate           |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | affected_rows| Number of rows updated             |
     - **Callback**: Return session termination confirmation

6. **Step 6: Update Session Activity Operation**
   - **Description**: Update last activity time for active sessions
   - **Data Validation**: Verify sessionId is provided
   - **SQL Call**:
     - **SQL**: 
       ```sql
       UPDATE user_sessions 
       SET last_activity_time = CURRENT_TIMESTAMP
       WHERE session_id = ?
       AND is_active = true
       ```
     - **Arguments**:
       | Name      | Value               | Description                    |
       |-----------|---------------------|--------------------------------|
       | sessionId | ARGUMENT.sessionId  | Session to update activity     |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | affected_rows| Number of rows updated             |
     - **Callback**: Return activity update confirmation

7. **Step 7: Clean Expired Sessions Operation**
   - **Description**: Remove expired and inactive sessions for maintenance
   - **Data Validation**: None
   - **SQL Call**:
     - **SQL**: 
       ```sql
       DELETE FROM user_sessions 
       WHERE (expires_at < CURRENT_TIMESTAMP 
              OR (is_active = false AND terminated_time < CURRENT_TIMESTAMP - INTERVAL '7 days'))
       ```
     - **Arguments**: None
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | affected_rows| Number of sessions cleaned         |
     - **Callback**: Return cleanup operation result

8. **Final Step**: Return operation-specific database results with session management data, validation results, or update confirmations based on the requested operation
