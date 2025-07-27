# SCR-MDE-01-01: Login Screen

## Cover
- **Document ID**: SCR-MDE-01-01
- **Document Name**: Login Screen

## History

| No | Date       | Version | Account | Action     | Impacted Sections | Description                    |
|----|------------|---------|---------|------------|-------------------|--------------------------------|
| 1  | 2024-Dec-27| v0.1    | system  | Initialize | Whole Document    | Initial creation of Login Screen detailed design |

## Used APIs

| No | API Document                              | API ID        | API Name              |
|----|-------------------------------------------|---------------|-----------------------|
| 1  | API-MDE-01-01_User Authentication_v0.1   | API-MDE-01-01-01 | User Authentication |
| 2  | API-MDE-01-04_Security Validation_v0.1   | API-MDE-01-04-01 | Security Validation |

## Screen Layout

| No | ID        | Name               | Type          | Status  | Value | Default Value | Data Source | Validations        | Description                           |
|----|-----------|--------------------|--------------|---------|---------|-----------|-----------|--------------------|---------------------------------------|
| 1  | ITEM-01   | Username Field     | Text Field   | Enabled |         |           |           | Required           | Input field for username/email       |
| 2  | ITEM-02   | Password Field     | Password Field| Enabled |         |           |           | Required           | Input field for password              |
| 3  | ITEM-03   | Language Selector  | Dropdown     | Enabled |         | EN        | Language Options | Required        | Language preference selection         |
| 4  | ITEM-04   | Remember Me        | Checkbox     | Enabled |         | false     |           |                    | Option to remember user credentials   |
| 5  | ITEM-05   | Login Button       | Button       | Enabled |         |           |           |                    | Submit authentication request         |
| 6  | ITEM-06   | Forgot Password    | Link         | Enabled |         |           |           |                    | Link to password recovery             |
| 7  | ITEM-07   | Error Message      | Label        | Hidden  |         |           |           |                    | Display authentication errors         |
| 8  | ITEM-08   | Loading Indicator  | Label        | Hidden  |         |           |           |                    | Show loading status during auth       |
| 9  | ITEM-09   | Company Logo       | Label        | Visible |         |           |           |                    | Display company branding              |
| 10 | ITEM-10   | Version Info       | Label        | Visible |         | v1.0      |           |                    | System version information            |

## Events

| No | ID     | Name                    | Description                                    |
|----|--------|-------------------------|------------------------------------------------|
| 1  | EVT-01 | Page Initialization     | Initialize login screen and set default values|
| 2  | EVT-02 | User Authentication     | Process user login with credentials           |
| 3  | EVT-03 | Language Change         | Update interface language preference          |
| 4  | EVT-04 | Password Recovery       | Navigate to password reset functionality      |
| 5  | EVT-05 | Form Validation         | Validate input fields before submission      |

## Steps & Details

### Event ID: EVT-01
### Event Name: Page Initialization

#### Steps:
1. **Step 1:**
   - **Trigger**: Initialization
   - **Description**: Load default language and initialize form components
   - **Data Validation**: None
   - **API Call**: None
   - **Callback**: Set focus on username field, display default language

2. **Step 2:**
   - **Trigger**: Initialization
   - **Description**: Check for saved language preference
   - **Data Validation**: None
   - **API Call**: None
   - **Callback**: Update language selector if preference found

3. **Final Step**: Display login form with default values, focus on username field, and show appropriate language interface

### Event ID: EVT-02
### Event Name: User Authentication

#### Steps:
1. **Step 1:**
   - **Trigger**: User Action
   - **Description**: Validate form inputs before submission
   - **Data Validation**: Check username and password are not empty
   - **API Call**: None
   - **Callback**: Show error message if validation fails

2. **Step 2:**
   - **Trigger**: User Action
   - **Description**: Perform security validation check
   - **Data Validation**: None
   - **API Call**: API-MDE-01-04-01 - Security Validation
     - **Arguments**:
       | Name     | Value           | Description                  |
       |----------|-----------------|------------------------------|
       | username | SCREEN.ITEM-01  | Username from input field    |
       | ipAddress| Client IP       | User's IP address           |
     - **Response**:
       | Name           | Description                    |
       |----------------|--------------------------------|
       | isAllowed      | Whether login attempt allowed  |
       | remainingAttempts| Remaining login attempts    |
       | lockoutTime    | Account lockout duration       |
     - **Callback**: Proceed to authentication if allowed, show lockout message if blocked

3. **Step 3:**
   - **Trigger**: API Call
   - **Description**: Authenticate user credentials
   - **Data Validation**: None
   - **API Call**: API-MDE-01-01-01 - User Authentication
     - **Arguments**:
       | Name       | Value           | Description                    |
       |------------|-----------------|--------------------------------|
       | username   | SCREEN.ITEM-01  | Username from input field      |
       | password   | SCREEN.ITEM-02  | Password from input field      |
       | language   | SCREEN.ITEM-03  | Selected language preference   |
       | rememberMe | SCREEN.ITEM-04  | Remember user preference       |
     - **Response**:
       | Name         | Description                      |
       |--------------|----------------------------------|
       | success      | Authentication result            |
       | token        | JWT authentication token         |
       | refreshToken | Token for session refresh        |
       | userInfo     | User profile information         |
       | sessionId    | Session identifier               |
     - **Callback**: Redirect to dashboard on success, show error message on failure

4. **Final Step**: Complete authentication process, establish user session, and redirect to main application dashboard

### Event ID: EVT-03
### Event Name: Language Change

#### Steps:
1. **Step 1:**
   - **Trigger**: User Action
   - **Description**: Update interface language based on user selection
   - **Data Validation**: Validate selected language is supported
   - **API Call**: None
   - **Callback**: Update all interface labels and messages to selected language

2. **Final Step**: Interface displays in selected language, language preference saved for future sessions

### Event ID: EVT-04
### Event Name: Password Recovery

#### Steps:
1. **Step 1:**
   - **Trigger**: User Action
   - **Description**: Navigate to password recovery screen
   - **Data Validation**: None
   - **API Call**: None
   - **Callback**: Redirect to password recovery page with current username pre-filled

2. **Final Step**: User is directed to password recovery interface

### Event ID: EVT-05
### Event Name: Form Validation

#### Steps:
1. **Step 1:**
   - **Trigger**: Data Change
   - **Description**: Real-time validation of username field
   - **Data Validation**: Check username format (email or username pattern)
   - **API Call**: None
   - **Callback**: Show validation indicator, enable/disable login button

2. **Step 2:**
   - **Trigger**: Data Change
   - **Description**: Real-time validation of password field
   - **Data Validation**: Check password length and complexity
   - **API Call**: None
   - **Callback**: Show password strength indicator

3. **Final Step**: Form validation complete, login button enabled when all validations pass
