# API-MDE-01-04: Security Validation

## Cover
- **Document ID**: API-MDE-01-04
- **Document Name**: Security Validation

## History

| No | Date       | Version | Account | Action     | Impacted Section | Description                           |
|----|------------|---------|---------|------------|------------------|---------------------------------------|
| 1  | 2024-Dec-27| v0.1    | system  | Initialize | Whole Document   | Initial creation of Security Validation API detailed design |

## Used Services

| No | Service Document                           | Service ID     | Service Name            |
|----|-------------------------------------------|----------------|-------------------------|
| 1  | SVE-MDE-01-03_Security Policy Service_v0.1 | SVE-MDE-01-03-01 | Security Policy Service |

## APIs

| No | ID             | Name                | Description                                    |
|----|----------------|---------------------|------------------------------------------------|
| 1  | API-MDE-01-04-01 | Login Attempt Validation | Validates security policies and monitors login attempts |
| 2  | API-MDE-01-04-02 | Account Status Check | Checks account lockout status and security restrictions |
| 3  | API-MDE-01-04-03 | Security Policy Enforcement | Enforces password policies and security rules |

## Logic & Flow

### API ID: API-MDE-01-04-01
### API Name: Login Attempt Validation
### HTTP Method: POST
### URI: /api/v1/auth/security/validate-attempt

#### Arguments:
| No | Name      | Data Type | Constraint                    | Description                      |
|----|-----------|-----------|-------------------------------|----------------------------------|
| 1  | username  | String    | Required, Max 100 characters  | Username attempting login        |
| 2  | ipAddress | String    | Required, IP format           | Client IP address                |
| 3  | userAgent | String    | Optional, Max 500 characters  | Client user agent string        |

#### Returns:
| No | Name              | Data Type | Description                        |
|----|-------------------|-----------|------------------------------------| 
| 1  | isAllowed         | Boolean   | Whether login attempt is allowed   |
| 2  | remainingAttempts | Integer   | Remaining login attempts           |
| 3  | lockoutTime       | Integer   | Account lockout duration in seconds|
| 4  | riskLevel         | String    | Security risk assessment level     |
| 5  | message           | String    | Security validation message        |

#### Steps:
1. **Step 1:**
   - **Description**: Check account lockout status and failed attempt history
   - **Data Validation**: Validate IP address format and username
   - **Service Call**: SVE-MDE-01-03-01 - Security Policy Service
     - **Arguments**:
       | Name      | Value              | Description                    |
       |-----------|--------------------|--------------------------------|
       | username  | ARGUMENT.username  | Username to check              |
       | ipAddress | ARGUMENT.ipAddress | Client IP address              |
       | operation | checkLockout       | Operation type                 |
     - **Returns**:
       | Name              | Description                        |
       |-------------------|------------------------------------| 
       | isLocked          | Account lockout status             |
       | failedAttempts    | Number of recent failed attempts   |
       | lockoutExpiry     | Lockout expiration time            |
       | remainingAttempts | Attempts remaining before lockout  |
     - **Callback**: Return lockout information if account is locked, proceed to risk assessment if not

2. **Step 2:**
   - **Description**: Assess login attempt risk based on patterns and history
   - **Data Validation**: None
   - **Service Call**: SVE-MDE-01-03-01 - Security Policy Service
     - **Arguments**:
       | Name      | Value               | Description                    |
       |-----------|---------------------|--------------------------------|
       | username  | ARGUMENT.username   | Username attempting login      |
       | ipAddress | ARGUMENT.ipAddress  | Client IP address              |
       | userAgent | ARGUMENT.userAgent  | Client user agent              |
       | operation | assessRisk          | Operation type                 |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | riskLevel    | Calculated risk level              |
       | isAllowed    | Whether attempt should be allowed  |
       | riskFactors  | Identified risk factors            |
     - **Callback**: Return risk assessment and validation decision

3. **Final Step**: Return login attempt validation result with security status and remaining attempts

### API ID: API-MDE-01-04-02
### API Name: Account Status Check
### HTTP Method: GET
### URI: /api/v1/auth/security/account-status

#### Arguments:
| No | Name     | Data Type | Constraint                    | Description                      |
|----|----------|-----------|-------------------------------|----------------------------------|
| 1  | username | String    | Required, Max 100 characters  | Username to check status         |

#### Returns:
| No | Name           | Data Type | Description                        |
|----|----------------|-----------|------------------------------------| 
| 1  | isActive       | Boolean   | Account active status              |
| 2  | isLocked       | Boolean   | Account lockout status             |
| 3  | lockoutExpiry  | DateTime  | Lockout expiration time            |
| 4  | failedAttempts | Integer   | Recent failed login attempts       |
| 5  | lastLoginTime  | DateTime  | Last successful login time         |
| 6  | securityLevel  | String    | Account security level             |

#### Steps:
1. **Step 1:**
   - **Description**: Retrieve comprehensive account security status
   - **Data Validation**: Validate username format
   - **Service Call**: SVE-MDE-01-03-01 - Security Policy Service
     - **Arguments**:
       | Name      | Value              | Description                    |
       |-----------|--------------------|--------------------------------|
       | username  | ARGUMENT.username  | Username to check              |
       | operation | getAccountStatus   | Operation type                 |
     - **Returns**:
       | Name           | Description                        |
       |----------------|------------------------------------| 
       | accountStatus  | Comprehensive account status       |
       | securityInfo   | Security-related information       |
       | lockoutInfo    | Lockout details if applicable      |
     - **Callback**: Return complete account security status

2. **Final Step**: Return comprehensive account status with security and lockout information

### API ID: API-MDE-01-04-03
### API Name: Security Policy Enforcement
### HTTP Method: POST
### URI: /api/v1/auth/security/enforce-policy

#### Arguments:
| No | Name       | Data Type | Constraint                    | Description                      |
|----|------------|-----------|-------------------------------|----------------------------------|
| 1  | username   | String    | Required, Max 100 characters  | Username for policy enforcement  |
| 2  | action     | String    | Required, Enum values         | Security action to enforce       |
| 3  | reason     | String    | Optional, Max 255 characters  | Reason for enforcement action    |
| 4  | duration   | Integer   | Optional                      | Enforcement duration in seconds  |

#### Returns:
| No | Name         | Data Type | Description                        |
|----|--------------|-----------|------------------------------------| 
| 1  | success      | Boolean   | Policy enforcement success         |
| 2  | actionTaken  | String    | Specific action that was taken     |
| 3  | expiryTime   | DateTime  | When enforcement expires           |
| 4  | message      | String    | Enforcement confirmation message   |

#### Steps:
1. **Step 1:**
   - **Description**: Validate enforcement action and apply security policy
   - **Data Validation**: Verify action type is valid and duration is appropriate
   - **Service Call**: SVE-MDE-01-03-01 - Security Policy Service
     - **Arguments**:
       | Name      | Value              | Description                    |
       |-----------|--------------------|--------------------------------|
       | username  | ARGUMENT.username  | Target username                |
       | action    | ARGUMENT.action    | Security action to take        |
       | reason    | ARGUMENT.reason    | Enforcement reason             |
       | duration  | ARGUMENT.duration  | Enforcement duration           |
       | operation | enforcePolicy      | Operation type                 |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | success      | Enforcement operation result       |
       | actionTaken  | Specific action implemented        |
       | expiryTime   | When enforcement expires           |
       | auditTrail   | Audit information for action       |
     - **Callback**: Return policy enforcement confirmation

2. **Final Step**: Return security policy enforcement result with action confirmation and expiry details
