*** Settings ***
Documentation  A resource file with reusable keywords for authentication.
Resource       resource.robot


*** Keywords ***
Authenticate With Valid Credentails
    Authenticate As  ${VALID USER}  ${VALID PASSWORD}

Authenticate As
    [Arguments]  ${login}  ${password}
    Open Browser To Login Page
    Login Page Should Be Open
    Input Username    ${login}
    Input Password    ${password}
    Submit Credentials


Open Browser To Login Page
    Open Browser  ${LOGIN URL}  ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed  ${DELAY}
    Login Page Should Be Open

Login Page Should Be Open
    Title Should Be  Login

Go To Login Page
    Go To  ${LOGIN URL}
    Login Page Should Be Open

Input Username
    [Arguments]  ${username}
    Input Text  jquery:#login.form-control  ${username}

Input Password
    [Arguments]  ${password}
    Input Text  jquery:#password.form-control  ${password}

Submit Credentials
    Click Button    signin

Welcome Page Should Be Open
    Location Should Be  ${WELCOME URL}
    Title Should Be  Dashboard

Clean
    [Arguments]    ${login}    ${password}
    prepare_database
    Authenticate With Valid Credentails
