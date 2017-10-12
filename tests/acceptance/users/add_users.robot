*** Settings ***
Documentation     A test suite containing tests related to users.
Resource          __keywords.robot
Resource          ../auth.robot
Suite Setup       Clean    test    test
Suite Teardown    Close Browser


*** Test Cases ***
New User Should Present In Table
    Add User  usr1  usr1  UserOne  proposals.read
    User Present In Table  UserOne


Deleted User Should Not Present In Table
    Add User  usr2  usr2  UserTwo  proposals.read
    Delete User  UserTwo
    User Not Present In Table  UserTwo


Delete Action Should Delete Right User
    Add User  usr3  usr3  UserThree  proposals.read
    Add User  usr4  usr4  UserFour  proposals.read
    Add User  usr5  usr5  UserFive  proposals.read
    Delete User  UserFour
    User Not Present In Table  UserFour

