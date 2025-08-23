# API-MDE-01-02: Session Management

## Cover
- **Document ID**: API-MDE-01-02
- **Document Name**: Session Management

## History

| No | Date       | Version | Account | Action     | Impacted Section | Description                           |
|----|------------|---------|---------|------------|------------------|---------------------------------------|
| 1  | 2024-Dec-27| v0.1    | system  | Initialize | Whole Document   | Initial creation of Session Management API detailed design |

## Used Services

| No | Service Document                           | Service ID     | Service Name            |
|----|-------------------------------------------|----------------|-------------------------|
| 1  | SVE-MDE-01-02_Session Management Service_v0.1 | SVE-MDE-01-02-01 | Session Management Service |

## APIs

| No | ID             | Name                | Description                                    |
|----|----------------|---------------------|------------------------------------------------|
| 1  | API-MDE-01-02-01 | Session Validation | Validates current session and returns session status |
| 2  | API-MDE-01-02-02 | Token Refresh      | Refreshes expired access token using refresh token |
| 3  | API-MDE-01-02-03 | Session Termination| Terminates user session and invalidates tokens |

## Logic & Flow

### API ID: API-MDE-01-02-01
### API Name: Session Validation
### HTTP Method: GET
### URI: /api/v1/auth/session

#### Arguments:
| No | Name         | Data Type | Constraint                    | Description                      |
|----|--------------|-----------|-------------------------------|----------------------------------|
| 1  | accessToken  | String    | Required, JWT format          | Current access token             |

#### Returns:
| No | Name         | Data Type | Description                        |
|----|--------------|-----------|------------------------------------| 
| 1  | isValid      | Boolean   | Session validity indicator         |
| 2  | userId       | String    | Current user identifier            |
| 3  | sessionId    | String    | Current session identifier         |
| 4  | expiresIn    | Integer   | Token remaining time in seconds    |
| 5  | userInfo     | Object    | Current user profile information   |
| 6  | permissions  | Array     | User permissions and roles         |

#### Steps:
1. **Step 1:**
   - **Description**: Validate access token format and extract session information
   - **Data Validation**: Verify JWT token format and signature
   - **Service Call**: SVE-MDE-01-02-01 - Session Management Service
     - **Arguments**:
       | Name        | Value                 | Description                    |
       |-------------|-----------------------|--------------------------------|
       | accessToken | ARGUMENT.accessToken  | Access token to validate       |
       | operation   | validate              | Operation type                 |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | isValid      | Token validation result            |
       | sessionData  | Session information if valid       |
       | userProfile  | User profile from session          |
       | permissions  | User permissions and roles         |
     - **Callback**: Return session information if valid, return invalid session error if not

2. **Final Step**: Return session validation response with user information and session status

### API ID: API-MDE-01-02-02
### API Name: Token Refresh
### HTTP Method: POST
### URI: /api/v1/auth/refresh

#### Arguments:
| No | Name         | Data Type | Constraint                    | Description                      |
|----|--------------|-----------|-------------------------------|----------------------------------|
| 1  | refreshToken | String    | Required, JWT format          | Refresh token for renewal        |

#### Returns:
| No | Name         | Data Type | Description                        |
|----|--------------|-----------|------------------------------------| 
| 1  | success      | Boolean   | Token refresh success indicator    |
| 2  | accessToken  | String    | New access token                   |
| 3  | refreshToken | String    | New refresh token                  |
| 4  | expiresIn    | Integer   | New token expiration time          |
| 5  | message      | String    | Response message or error details  |

#### Steps:
1. **Step 1:**
   - **Description**: Validate refresh token and generate new access token
   - **Data Validation**: Verify refresh token format and expiration
   - **Service Call**: SVE-MDE-01-02-01 - Session Management Service
     - **Arguments**:
       | Name         | Value                  | Description                    |
       |--------------|------------------------|--------------------------------|
       | refreshToken | ARGUMENT.refreshToken  | Refresh token to process       |
       | operation    | refresh                | Operation type                 |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | success      | Token refresh result               |
       | newTokens    | New access and refresh tokens      |
       | expiresIn    | Token expiration duration          |
     - **Callback**: Return new tokens if successful, return refresh error if failed

2. **Final Step**: Return token refresh response with new authentication tokens

### API ID: API-MDE-01-02-03
### API Name: Session Termination
### HTTP Method: POST
### URI: /api/v1/auth/logout

#### Arguments:
| No | Name         | Data Type | Constraint                    | Description                      |
|----|--------------|-----------|-------------------------------|----------------------------------|
| 1  | accessToken  | String    | Required, JWT format          | Current access token             |
| 2  | sessionId    | String    | Required                      | Session identifier to terminate  |

#### Returns:
| No | Name         | Data Type | Description                        |
|----|--------------|-----------|------------------------------------| 
| 1  | success      | Boolean   | Session termination success        |
| 2  | message      | String    | Confirmation or error message      |

#### Steps:
1. **Step 1:**
   - **Description**: Terminate user session and invalidate all tokens
   - **Data Validation**: Verify access token and session ownership
   - **Service Call**: SVE-MDE-01-02-01 - Session Management Service
     - **Arguments**:
       | Name        | Value                | Description                    |
       |-------------|----------------------|--------------------------------|
       | accessToken | ARGUMENT.accessToken | Access token to invalidate     |
       | sessionId   | ARGUMENT.sessionId   | Session to terminate           |
       | operation   | terminate            | Operation type                 |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | success      | Session termination result         |
       | message      | Termination confirmation message   |
     - **Callback**: Return termination confirmation

2. **Final Step**: Return session termination confirmation and clear all authentication tokens
