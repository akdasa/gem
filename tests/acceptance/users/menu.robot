*** Settings ***
Documentation     A test suite containing tests related to proposals.
Resource          __keywords.robot
Resource          ../auth.robot
Resource          ../nav.robot
Suite Setup       Clean    test    test
Suite Teardown    Close Browser


*** Test Cases ***
Users Menu Should Be Highlighed
    Go To Users Page
    Navigation Bar Item Shoud Be Highlighted  Users


Users Menu Should Be Highlighed On New Page
    Go To  http://${SERVER}/users/new
    Navigation Bar Item Shoud Be Highlighted  Users


Users Menu Should Be Highlighed On Update Page
    Add User  menuHighlighTest  menuHighlighTest  Menu Highlight Test  Permissions
    Open User  Menu Highlight Test
    Navigation Bar Item Shoud Be Highlighted  Users
