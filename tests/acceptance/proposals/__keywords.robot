*** Settings ***
Documentation    Suite description
Resource         ../resource.robot


*** Keywords ***
Go To Proposals Page
    Go To  http://${SERVER}/proposals


Add Proposal
    [Arguments]  ${title}  ${content}
    Go To Proposals Page
    Click Link  proposals-new
    Title Should Be  New proposal
    Input Text  title  ${title}
    Input Text  content  ${content}
    Click Button  submit


Proposal Present In Table
    [Arguments]  ${title}
    Table Should Contain  proposals-table  ${title}


Proposal Not Present In Table
    [Arguments]  ${title}
    Page Should Not Contain  ${title}


Delete Proposal
    [Arguments]  ${title}
    ${key}=  Get Element Attribute  jquery:a:contains('${title}')  data-key
    Click Link  jquery:a.delete[data-key='${key}']
    Wait Until Element Does Not Contain  proposals-table  ${title}
