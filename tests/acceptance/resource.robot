*** Settings ***
Documentation     A resource file with reusable keywords and variables.
Library           SeleniumLibrary
Library           aux.py

*** Variables ***
${SERVER}           localhost:5000
${BROWSER}          Chrome
${DELAY}            0
${VALID USER}       test
${VALID PASSWORD}   test
${LOGIN URL}        http://${SERVER}/account/login
${WELCOME URL}      http://${SERVER}/account/
${ERROR URL}        http://${SERVER}/error.html

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Login Page Should Be Open

Login Page Should Be Open
    Title Should Be    Login

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open

Go To Proposals Page
    Go To   http://${SERVER}/proposals

Input Username
    [Arguments]    ${username}
    Input Text    jquery:#login.form-control    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    jquery:#password.form-control    ${password}

Submit Credentials
    Click Button    signin

Welcome Page Should Be Open
    Location Should Be    ${WELCOME URL}
    Title Should Be    Dashboard
