*** Settings ***
Documentation    Suite description
Resource         ../resource.robot


*** Keywords ***
Go To Sessions Page
    Go To  http://${SERVER}/sessions


Add Session
    [Arguments]  ${title}  ${agenda}
    Go To Sessions Page
    Click Link  sessions-new
    Title Should Be  New session
    Input Text  title  ${title}
    Input Text  agenda  ${agenda}
    Click Button  submit

Open Session
    [Arguments]  ${title}
    Click Link  jquery:#sessions-table a:contains('${title}')


Session Present In Table
    [Arguments]  ${title}
    Table Should Contain  sessions-table  ${title}


Session Not Present In Table
    [Arguments]  ${title}
    Page Should Not Contain  ${title}


Delete Session
    [Arguments]  ${title}
    ${key}=  Get Element Attribute  jquery:a:contains('${title}')  data-key
    Click Link  jquery:a.delete[data-key='${key}']
    Wait Until Element Does Not Contain  sessions-table  ${title}
