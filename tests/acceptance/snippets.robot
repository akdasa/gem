*** Keywords ***
Clean
    [Arguments]    ${login}    ${password}
    prepare_database
    User Authenticated  ${login}    ${password}

User Authenticated
    [Arguments]    ${login}    ${password}
    Open Browser To Login Page
    Login Page Should Be Open
    Input Username    ${login}
    Input Password    ${password}
    Submit Credentials
