*** Settings ***
Documentation    Suite description
Resource         ../resource.robot


*** Keywords ***
Go To Users Page
    Go To  http://${SERVER}/users


Add User
    [Arguments]  ${login}  ${password}  ${name}  ${permissions}
    Go To Users Page
    Click Link  new-user
    Title Should Be  New user
    Input Text  name  ${name}
    Input Text  login  ${login}
    Input Text  password  ${password}
    Input Text  permissions  ${permissions}
    Click Button  submit


User Present In Table
    [Arguments]  ${name}
    Table Should Contain  users-list  ${name}


User Not Present In Table
    [Arguments]  ${name}
    Page Should Not Contain  ${name}


Delete User
    [Arguments]  ${name}
    ${key}=  Get Element Attribute  jquery:a:contains('${name}')  data-key
    Click Link  jquery:a.delete[data-key='${key}']
    Wait Until Element Does Not Contain  users-list  ${name}
