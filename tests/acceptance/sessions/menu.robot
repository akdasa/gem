*** Settings ***
Documentation     A test suite containing tests related to proposals.
Resource          __keywords.robot
Resource          ../auth.robot
Resource          ../nav.robot
Suite Setup       Clean    test    test
Suite Teardown    Close Browser


*** Test Cases ***
Sessions Menu Should Be Highlighed
    Go To Sessions Page
    Navigation Bar Item Shoud Be Highlighted  Sessions


Sessions Menu Should Be Highlighed On New Page
    Go To  http://${SERVER}/sessions/new
    Navigation Bar Item Shoud Be Highlighted  Sessions


Sessions Menu Should Be Highlighed On Update Page
    Add Session  Menu Highlight Test  Agenda
    Open Session  Menu Highlight Test
    Navigation Bar Item Shoud Be Highlighted  Sessions
