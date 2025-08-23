# API-MDE-01-01: User Authentication

## Cover
- **Document ID**: API-MDE-01-01
- **Document Name**: User Authentication

## History

| No | Date       | Version | Account | Action     | Impacted Section | Description                           |
|----|------------|---------|---------|------------|------------------|---------------------------------------|
| 1  | 2024-Dec-27| v0.1    | system  | Initialize | Whole Document   | Initial creation of User Authentication API detailed design |

## Used Services

| No | Service Document                           | Service ID     | Service Name            |
|----|-------------------------------------------|----------------|-------------------------|
| 1  | SVE-MDE-01-01_Authentication Service_v0.1 | SVE-MDE-01-01-01 | Authentication Service |
| 2  | SVE-MDE-01-02_Session Management Service_v0.1 | SVE-MDE-01-02-01 | Session Management Service |

## APIs

| No | ID             | Name                | Description                                    |
|----|----------------|---------------------|------------------------------------------------|
| 1  | API-MDE-01-01-01 | User Authentication | Validates user credentials and establishes secure session with JWT token generation |

## Logic & Flow

### API ID: API-MDE-01-01-01
### API Name: User Authentication
### HTTP Method: POST
### URI: /api/v1/auth/login

#### Arguments:
| No | Name       | Data Type | Constraint                    | Description                      |
|----|------------|-----------|-------------------------------|----------------------------------|
| 1  | username   | String    | Required, Max 100 characters  | Username or email address        |
| 2  | password   | String    | Required, Max 255 characters  | User password                    |
| 3  | language   | String    | Required, Enum values         | Preferred language code          |
| 4  | rememberMe | Boolean   | Optional                      | Remember user session preference |

#### Returns:
| No | Name         | Data Type | Description                        |
|----|--------------|-----------|------------------------------------| 
| 1  | success      | Boolean   | Authentication success indicator   |
| 2  | token        | String    | JWT authentication token           |
| 3  | refreshToken | String    | Token for session refresh          |
| 4  | userInfo     | Object    | User profile information           |
| 5  | sessionId    | String    | Unique session identifier          |
| 6  | expiresIn    | Integer   | Token expiration time in seconds   |
| 7  | message      | String    | Response message or error details  |

#### Steps:
1. **Step 1:**
   - **Description**: Validate input parameters and check required fields
   - **Data Validation**: Verify username and password are provided, validate language code format
   - **Service Call**: None
   - **Callback**: Return validation error if any required field is missing

2. **Step 2:**
   - **Description**: Authenticate user credentials using authentication service
   - **Data Validation**: None
   - **Service Call**: SVE-MDE-01-01-01 - Authentication Service
     - **Arguments**:
       | Name     | Value              | Description                    |
       |----------|--------------------|--------------------------------|
       | username | ARGUMENT.username  | Username from API request      |
       | password | ARGUMENT.password  | Password from API request      |
       | language | ARGUMENT.language  | Language preference            |
     - **Returns**:
       | Name         | Description                      |
       |--------------|----------------------------------|
       | isValid      | Credential validation result     |
       | userId       | Authenticated user identifier    |
       | userProfile  | User profile information         |
       | roleInfo     | User role and permissions        |
     - **Callback**: Proceed to session creation if valid, return authentication error if invalid

3. **Step 3:**
   - **Description**: Create user session and generate authentication tokens
   - **Data Validation**: None
   - **Service Call**: SVE-MDE-01-02-01 - Session Management Service
     - **Arguments**:
       | Name       | Value                | Description                      |
       |------------|----------------------|----------------------------------|
       | userId     | Previous Result      | User ID from authentication      |
       | userProfile| Previous Result      | User profile from authentication |
       | rememberMe | ARGUMENT.rememberMe  | Session persistence preference   |
       | language   | ARGUMENT.language    | User language preference         |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | sessionId    | Generated session identifier       |
       | accessToken  | JWT access token                   |
       | refreshToken | Refresh token for session renewal  |
       | expiresIn    | Token expiration duration          |
     - **Callback**: Return complete authentication response with tokens and user information

4. **Final Step**: Return authentication response containing JWT tokens, user information, and session details for successful login
