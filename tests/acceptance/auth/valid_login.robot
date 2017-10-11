*** Settings ***
Documentation     A test suite with a single test for valid login.
Resource          ../resource.robot

*** Test Cases ***
Valid Login
    Open Browser To Login Page
    Login Page Should Be Open
    Input Username    akd
    Input Password    akd
    Submit Credentials
    Welcome Page Should Be Open
    [Teardown]    Close Browser
