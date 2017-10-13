*** Settings ***
Documentation     A test suite containing tests related to proposals.
Resource          __keywords.robot
Resource          ../auth.robot
Resource          ../nav.robot
Suite Setup       Clean    test    test
Suite Teardown    Close Browser


*** Test Cases ***
Proposals Menu Should Be Highlighed
    Go To Proposals Page
    Navigation Bar Item Shoud Be Highlighted  Proposals


Proposals Menu Should Be Highlighed On New Page
    Go To  http://${SERVER}/proposals/new
    Navigation Bar Item Shoud Be Highlighted  Proposals


Proposals Menu Should Be Highlighed On Update Page
    Add Proposal  Menu Highlight Test  Some Content
    Open Proposal  Menu Highlight Test
    Navigation Bar Item Shoud Be Highlighted  Proposals
