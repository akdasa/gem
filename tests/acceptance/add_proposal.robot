*** Settings ***
Documentation     A test suite containing tests related to proposals.
Resource          resource.robot
Resource          snippets.robot
Suite Setup       User Authenticated    akd    akd
Suite Teardown    Close Browser
Test Setup        Go To Proposals Page


*** Test Cases ***
Add Proposal
    Click Link              jquery:.btn
    Title Should Be         New proposal
    Input Text              name:title          New proposal
    Input Text              name:content        Some content
    Click Button            id:submit
    Table Should Contain    id:proposals-list   New proposal
