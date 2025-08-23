# API-MDE-01-03: Password Management

## Cover
- **Document ID**: API-MDE-01-03
- **Document Name**: Password Management

## History

| No | Date       | Version | Account | Action     | Impacted Section | Description                           |
|----|------------|---------|---------|------------|------------------|---------------------------------------|
| 1  | 2024-Dec-27| v0.1    | system  | Initialize | Whole Document   | Initial creation of Password Management API detailed design |

## Used Services

| No | Service Document                           | Service ID     | Service Name            |
|----|-------------------------------------------|----------------|-------------------------|
| 1  | SVE-MDE-01-01_Authentication Service_v0.1 | SVE-MDE-01-01-01 | Authentication Service |
| 2  | SVE-MDE-01-03_Security Policy Service_v0.1 | SVE-MDE-01-03-01 | Security Policy Service |

## APIs

| No | ID             | Name                | Description                                    |
|----|----------------|---------------------|------------------------------------------------|
| 1  | API-MDE-01-03-01 | Password Change    | Changes user password with current password verification |
| 2  | API-MDE-01-03-02 | Password Reset     | Initiates password reset process with email verification |
| 3  | API-MDE-01-03-03 | Password Reset Confirm | Confirms password reset with verification token |

## Logic & Flow

### API ID: API-MDE-01-03-01
### API Name: Password Change
### HTTP Method: POST
### URI: /api/v1/auth/password/change

#### Arguments:
| No | Name            | Data Type | Constraint                      | Description                      |
|----|-----------------|-----------|--------------------------------|----------------------------------|
| 1  | userId          | String    | Required                       | User identifier                  |
| 2  | currentPassword | String    | Required, Max 255 characters   | Current password for verification|
| 3  | newPassword     | String    | Required, Min 8 Max 255 chars  | New password                     |
| 4  | confirmPassword | String    | Required, Must match newPassword| Password confirmation            |

#### Returns:
| No | Name         | Data Type | Description                        |
|----|--------------|-----------|------------------------------------| 
| 1  | success      | Boolean   | Password change success indicator  |
| 2  | message      | String    | Success or error message           |
| 3  | policyCheck  | Object    | Password policy validation results |

#### Steps:
1. **Step 1:**
   - **Description**: Validate password change requirements and policy compliance
   - **Data Validation**: Verify new password matches confirmation, check password policy
   - **Service Call**: SVE-MDE-01-03-01 - Security Policy Service
     - **Arguments**:
       | Name        | Value                  | Description                    |
       |-------------|------------------------|--------------------------------|
       | newPassword | ARGUMENT.newPassword   | New password to validate       |
       | userId      | ARGUMENT.userId        | User requesting change         |
       | operation   | validatePassword       | Operation type                 |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | isValid      | Password policy compliance         |
       | violations   | Policy violations if any           |
       | strength     | Password strength assessment       |
     - **Callback**: Proceed if policy compliant, return policy error if not

2. **Step 2:**
   - **Description**: Verify current password before allowing change
   - **Data Validation**: None
   - **Service Call**: SVE-MDE-01-01-01 - Authentication Service
     - **Arguments**:
       | Name            | Value                      | Description                    |
       |-----------------|----------------------------|--------------------------------|
       | userId          | ARGUMENT.userId            | User requesting change         |
       | currentPassword | ARGUMENT.currentPassword   | Current password to verify     |
       | operation       | verifyPassword             | Operation type                 |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | isValid      | Current password verification      |
       | message      | Verification result message        |
     - **Callback**: Proceed to password update if verified, return verification error if not

3. **Step 3:**
   - **Description**: Update user password in the system
   - **Data Validation**: None
   - **Service Call**: SVE-MDE-01-01-01 - Authentication Service
     - **Arguments**:
       | Name        | Value                  | Description                    |
       |-------------|------------------------|--------------------------------|
       | userId      | ARGUMENT.userId        | User to update password        |
       | newPassword | ARGUMENT.newPassword   | New password to set            |
       | operation   | updatePassword         | Operation type                 |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | success      | Password update result             |
       | message      | Update confirmation message        |
     - **Callback**: Return password change confirmation

4. **Final Step**: Return password change result with success confirmation and policy compliance details

### API ID: API-MDE-01-03-02
### API Name: Password Reset
### HTTP Method: POST
### URI: /api/v1/auth/password/reset

#### Arguments:
| No | Name     | Data Type | Constraint                    | Description                      |
|----|----------|-----------|-------------------------------|----------------------------------|
| 1  | username | String    | Required, Max 100 characters  | Username or email for reset      |

#### Returns:
| No | Name         | Data Type | Description                        |
|----|--------------|-----------|------------------------------------| 
| 1  | success      | Boolean   | Reset initiation success indicator |
| 2  | message      | String    | Confirmation or error message      |
| 3  | resetToken   | String    | Password reset verification token  |

#### Steps:
1. **Step 1:**
   - **Description**: Validate user exists and initiate password reset process
   - **Data Validation**: Verify username format and existence
   - **Service Call**: SVE-MDE-01-01-01 - Authentication Service
     - **Arguments**:
       | Name     | Value              | Description                    |
       |----------|--------------------|--------------------------------|
       | username | ARGUMENT.username  | Username to reset password     |
       | operation| initiateReset      | Operation type                 |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | userExists   | User existence verification        |
       | userId       | User identifier if found           |
       | email        | User email for reset notification  |
     - **Callback**: Proceed to reset token generation if user exists

2. **Step 2:**
   - **Description**: Generate password reset token and send notification
   - **Data Validation**: None
   - **Service Call**: SVE-MDE-01-03-01 - Security Policy Service
     - **Arguments**:
       | Name      | Value              | Description                    |
       |-----------|--------------------|--------------------------------|
       | userId    | Previous Result    | User ID from previous step     |
       | email     | Previous Result    | User email for notification    |
       | operation | generateResetToken | Operation type                 |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | resetToken   | Generated reset verification token |
       | expiresIn    | Token expiration time              |
       | message      | Reset initiation confirmation      |
     - **Callback**: Return reset token and confirmation message

3. **Final Step**: Return password reset initiation confirmation with verification token

### API ID: API-MDE-01-03-03
### API Name: Password Reset Confirm
### HTTP Method: POST
### URI: /api/v1/auth/password/reset/confirm

#### Arguments:
| No | Name            | Data Type | Constraint                      | Description                      |
|----|-----------------|-----------|--------------------------------|----------------------------------|
| 1  | resetToken      | String    | Required                       | Password reset verification token|
| 2  | newPassword     | String    | Required, Min 8 Max 255 chars  | New password                     |
| 3  | confirmPassword | String    | Required, Must match newPassword| Password confirmation            |

#### Returns:
| No | Name         | Data Type | Description                        |
|----|--------------|-----------|------------------------------------| 
| 1  | success      | Boolean   | Password reset success indicator   |
| 2  | message      | String    | Success or error message           |

#### Steps:
1. **Step 1:**
   - **Description**: Validate reset token and password policy compliance
   - **Data Validation**: Verify reset token validity and password confirmation match
   - **Service Call**: SVE-MDE-01-03-01 - Security Policy Service
     - **Arguments**:
       | Name        | Value                  | Description                    |
       |-------------|------------------------|--------------------------------|
       | resetToken  | ARGUMENT.resetToken    | Reset token to validate        |
       | newPassword | ARGUMENT.newPassword   | New password to validate       |
       | operation   | validateResetToken     | Operation type                 |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | isValid      | Token and password validation      |
       | userId       | User ID from token                 |
       | violations   | Policy violations if any           |
     - **Callback**: Proceed to password reset if valid, return validation error if not

2. **Step 2:**
   - **Description**: Complete password reset with new password
   - **Data Validation**: None
   - **Service Call**: SVE-MDE-01-01-01 - Authentication Service
     - **Arguments**:
       | Name        | Value                  | Description                    |
       |-------------|------------------------|--------------------------------|
       | userId      | Previous Result        | User ID from token validation  |
       | newPassword | ARGUMENT.newPassword   | New password to set            |
       | operation   | completeReset          | Operation type                 |
     - **Returns**:
       | Name         | Description                        |
       |--------------|------------------------------------| 
       | success      | Password reset completion result   |
       | message      | Reset confirmation message         |
     - **Callback**: Return password reset completion confirmation

3. **Final Step**: Return password reset completion confirmation and invalidate reset token
