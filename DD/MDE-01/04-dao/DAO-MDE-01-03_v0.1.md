# DAO-MDE-01-03: Security Policy DAO

## Cover
- **Document ID**: DAO-MDE-01-03
- **Document Name**: Security Policy DAO

## History

| No | Date       | Version | Account | Action     | Impacted Section | Description                           |
|----|------------|---------|---------|------------|------------------|---------------------------------------|
| 1  | 2024-Dec-27| v0.1    | system  | Initialize | Whole Document   | Initial creation of Security Policy DAO detailed design |

## DAOs

| No | ID             | Name                | Description                                    |
|----|----------------|---------------------|------------------------------------------------|
| 1  | DAO-MDE-01-03-01 | Security Policy DAO | Security policy data and login attempt tracking operations |

## Logic & Flow

### DAO ID: DAO-MDE-01-03-01
### DAO Name: Security Policy DAO

#### Arguments:
| No | Name         | Data Type | Constraint                    | Description                      |
|----|--------------|-----------|-------------------------------|----------------------------------|
| 1  | username     | String    | Required for most operations  | Username for security operations |
| 2  | userId       | String    | Required for user operations  | User unique identifier           |
| 3  | password     | String    | Required for validation       | Password to validate             |
| 4  | ipAddress    | String    | Required for monitoring       | Client IP address                |
| 5  | userAgent    | String    | Optional                      | Client user agent string        |
| 6  | resetToken   | String    | Required for reset operations | Password reset token             |
| 7  | email        | String    | Required for notifications    | User email address               |
| 8  | action       | String    | Required for enforcement      | Security action to take          |
| 9  | reason       | String    | Optional                      | Reason for security action       |
| 10 | duration     | Integer   | Optional                      | Action duration in seconds       |
| 11 | operation    | String    | Required, Enum values         | Database operation type          |

#### Returns:
| No | Name              | Data Type | Description                        |
|----|-------------------|-----------|------------------------------------| 
| 1  | success           | Boolean   | Operation success indicator        |
| 2  | isValid           | Boolean   | Validation result                  |
| 3  | violations        | Array     | Policy violations                  |
| 4  | strength          | Integer   | Password strength score            |
| 5  | isLocked          | Boolean   | Account lockout status             |
| 6  | failedAttempts    | Integer   | Failed login attempt count         |
| 7  | remainingAttempts | Integer   | Attempts remaining                 |
| 8  | lockoutExpiry     | DateTime  | Lockout expiration time            |
| 9  | riskLevel         | String    | Security risk assessment           |
| 10 | resetToken        | String    | Generated reset token              |
| 11 | expiresIn         | Integer   | Token expiration time              |
| 12 | auditId           | String    | Audit trail identifier             |

#### Steps:
1. **Step 1: Password Policy Validation Operation**
   - **Description**: Validate password against defined security policies
   - **Data Validation**: Check password is provided and not empty
   - **SQL Call**: 
     - **SQL**: 
       ```sql
       SELECT 
           policy_name,
           policy_value,
           is_required
       FROM security_policies 
       WHERE policy_category = 'PASSWORD'
       AND is_active = true
       ORDER BY policy_priority
       ```
     - **Arguments**: None
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | policy_name  | Security policy name               |
       | policy_value | Policy value or rule               |
       | is_required  | Whether policy is mandatory        |
     - **Callback**: Apply policies to password and return validation result

2. **Step 2: Login Attempt Tracking Operation**
   - **Description**: Record and track failed login attempts
   - **Data Validation**: Verify username and IP address are provided
   - **SQL Call**:
     - **SQL**: 
       ```sql
       INSERT INTO login_attempts (
           username,
           ip_address,
           user_agent,
           attempt_time,
           is_successful,
           failure_reason
       ) VALUES (?, ?, ?, CURRENT_TIMESTAMP, false, 'Authentication Failed')
       ```
     - **Arguments**:
       | Name      | Value              | Description                    |
       |-----------|--------------------|--------------------------------|
       | username  | ARGUMENT.username  | Username for failed attempt    |
       | ipAddress | ARGUMENT.ipAddress | Client IP address              |
       | userAgent | ARGUMENT.userAgent | Client user agent              |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | affected_rows| Number of rows inserted            |
     - **Callback**: Record failed attempt and check lockout threshold

3. **Step 3: Account Lockout Check Operation**
   - **Description**: Check if account should be locked based on failed attempts
   - **Data Validation**: Verify username is provided
   - **SQL Call**:
     - **SQL**: 
       ```sql
       SELECT 
           COUNT(*) as failed_count,
           MAX(attempt_time) as last_attempt,
           (SELECT policy_value::integer FROM security_policies 
            WHERE policy_name = 'MAX_LOGIN_ATTEMPTS' AND is_active = true) as max_attempts,
           (SELECT policy_value::integer FROM security_policies 
            WHERE policy_name = 'LOCKOUT_DURATION' AND is_active = true) as lockout_duration
       FROM login_attempts 
       WHERE username = ?
       AND is_successful = false
       AND attempt_time > CURRENT_TIMESTAMP - INTERVAL '1 hour'
       ```
     - **Arguments**:
       | Name     | Value              | Description                    |
       |----------|--------------------|--------------------------------|
       | username | ARGUMENT.username  | Username to check              |
     - **Returns**:
       | Name           | Description                        |
       |----------------|------------------------------------| 
       | failed_count   | Number of recent failed attempts   |
       | last_attempt   | Most recent attempt time           |
       | max_attempts   | Maximum allowed attempts           |
       | lockout_duration| Lockout duration in minutes       |
     - **Callback**: Determine if account should be locked and apply lockout if necessary

4. **Step 4: Account Lockout Application Operation**
   - **Description**: Apply account lockout with specified duration
   - **Data Validation**: Verify username and lockout duration are provided
   - **SQL Call**:
     - **SQL**: 
       ```sql
       INSERT INTO account_lockouts (
           username,
           locked_time,
           unlock_time,
           lockout_reason,
           locked_by_ip
       ) VALUES (?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '? minutes', 'Excessive Failed Attempts', ?)
       ON CONFLICT (username) 
       DO UPDATE SET 
           locked_time = CURRENT_TIMESTAMP,
           unlock_time = CURRENT_TIMESTAMP + INTERVAL '? minutes',
           lockout_reason = 'Excessive Failed Attempts'
       ```
     - **Arguments**:
       | Name     | Value              | Description                    |
       |----------|--------------------|--------------------------------|
       | username | ARGUMENT.username  | Username to lock               |
       | duration | Lockout Duration   | Lockout period in minutes      |
       | ipAddress| ARGUMENT.ipAddress | IP that triggered lockout      |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | affected_rows| Number of rows affected            |
     - **Callback**: Return lockout application confirmation

5. **Step 5: Risk Assessment Operation**
   - **Description**: Assess login attempt risk based on patterns and history
   - **Data Validation**: Verify username and IP address are provided
   - **SQL Call**:
     - **SQL**: 
       ```sql
       WITH risk_factors AS (
           SELECT 
               CASE WHEN COUNT(DISTINCT ip_address) > 5 THEN 'HIGH' 
                    WHEN COUNT(DISTINCT ip_address) > 2 THEN 'MEDIUM' 
                    ELSE 'LOW' END as ip_diversity_risk,
               CASE WHEN COUNT(*) > 10 THEN 'HIGH'
                    WHEN COUNT(*) > 5 THEN 'MEDIUM'
                    ELSE 'LOW' END as frequency_risk,
               COUNT(*) as recent_attempts,
               COUNT(DISTINCT ip_address) as unique_ips
           FROM login_attempts 
           WHERE username = ?
           AND attempt_time > CURRENT_TIMESTAMP - INTERVAL '24 hours'
       )
       SELECT * FROM risk_factors
       ```
     - **Arguments**:
       | Name     | Value              | Description                    |
       |----------|--------------------|--------------------------------|
       | username | ARGUMENT.username  | Username for risk assessment   |
     - **Returns**:
       | Name               | Description                        |
       |--------------------|------------------------------------| 
       | ip_diversity_risk  | Risk level based on IP diversity   |
       | frequency_risk     | Risk level based on attempt frequency|
       | recent_attempts    | Number of recent attempts          |
       | unique_ips         | Number of unique IP addresses      |
     - **Callback**: Calculate overall risk level and return assessment

6. **Step 6: Password Reset Token Generation Operation**
   - **Description**: Generate and store password reset token
   - **Data Validation**: Verify userId and email are provided
   - **SQL Call**:
     - **SQL**: 
       ```sql
       INSERT INTO password_reset_tokens (
           user_id,
           token_hash,
           created_time,
           expires_time,
           is_used,
           email_sent_to
       ) VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '24 hours', false, ?)
       ```
     - **Arguments**:
       | Name      | Value             | Description                    |
       |-----------|-------------------|--------------------------------|
       | userId    | ARGUMENT.userId   | User requesting reset          |
       | tokenHash | Generated Hash    | Secure token hash              |
       | email     | ARGUMENT.email    | Email for notification         |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | affected_rows| Number of rows inserted            |
     - **Callback**: Return reset token generation confirmation

7. **Step 7: Reset Token Validation Operation**
   - **Description**: Validate password reset token for password reset
   - **Data Validation**: Verify reset token is provided
   - **SQL Call**:
     - **SQL**: 
       ```sql
       SELECT 
           user_id,
           created_time,
           expires_time,
           is_used
       FROM password_reset_tokens 
       WHERE token_hash = ?
       AND expires_time > CURRENT_TIMESTAMP
       AND is_used = false
       ```
     - **Arguments**:
       | Name      | Value               | Description                    |
       |-----------|---------------------|--------------------------------|
       | tokenHash | ARGUMENT.resetToken | Reset token hash to validate   |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | user_id      | User ID from token                 |
       | created_time | Token creation time                |
       | expires_time | Token expiration time              |
       | is_used      | Whether token was already used     |
     - **Callback**: Return token validation result

8. **Step 8: Security Policy Enforcement Operation**
   - **Description**: Apply security enforcement actions with audit trail
   - **Data Validation**: Verify username and action are provided
   - **SQL Call**:
     - **SQL**: 
       ```sql
       INSERT INTO security_enforcement_log (
           username,
           action_type,
           enforcement_reason,
           enforced_time,
           expires_time,
           enforced_by_system,
           audit_id
       ) VALUES (?, ?, ?, CURRENT_TIMESTAMP, 
                CASE WHEN ? > 0 THEN CURRENT_TIMESTAMP + INTERVAL '? seconds' 
                     ELSE NULL END, 
                true, ?)
       ```
     - **Arguments**:
       | Name      | Value              | Description                    |
       |-----------|--------------------|--------------------------------|
       | username  | ARGUMENT.username  | Target username                |
       | action    | ARGUMENT.action    | Security action type           |
       | reason    | ARGUMENT.reason    | Enforcement reason             |
       | duration  | ARGUMENT.duration  | Enforcement duration           |
       | auditId   | Generated UUID     | Unique audit identifier        |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | affected_rows| Number of rows inserted            |
     - **Callback**: Return enforcement action confirmation with audit ID

9. **Step 9: Account Status Retrieval Operation**
   - **Description**: Get comprehensive account security status
   - **Data Validation**: Verify username is provided
   - **SQL Call**:
     - **SQL**: 
       ```sql
       SELECT 
           u.username,
           u.is_active,
           al.locked_time,
           al.unlock_time,
           al.lockout_reason,
           COUNT(la.id) as recent_failed_attempts,
           MAX(la.attempt_time) as last_attempt_time,
           COUNT(DISTINCT la.ip_address) as unique_attempt_ips
       FROM users u
       LEFT JOIN account_lockouts al ON u.username = al.username 
           AND al.unlock_time > CURRENT_TIMESTAMP
       LEFT JOIN login_attempts la ON u.username = la.username 
           AND la.attempt_time > CURRENT_TIMESTAMP - INTERVAL '24 hours'
           AND la.is_successful = false
       WHERE u.username = ?
       GROUP BY u.username, u.is_active, al.locked_time, al.unlock_time, al.lockout_reason
       ```
     - **Arguments**:
       | Name     | Value              | Description                    |
       |----------|--------------------|--------------------------------|
       | username | ARGUMENT.username  | Username for status check      |
     - **Returns**:
       | Name                  | Description                        |
       |-----------------------|------------------------------------| 
       | username              | Username                           |
       | is_active             | Account active status              |
       | locked_time           | Current lockout start time         |
       | unlock_time           | Lockout expiration time            |
       | lockout_reason        | Reason for current lockout         |
       | recent_failed_attempts| Failed attempts in last 24 hours  |
       | last_attempt_time     | Most recent attempt time           |
       | unique_attempt_ips    | Number of unique IPs attempting    |
     - **Callback**: Return comprehensive account security status

10. **Final Step**: Return operation-specific database results with security policy validation, login attempt tracking, risk assessment, or enforcement actions based on the requested operation
