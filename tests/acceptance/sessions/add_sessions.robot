*** Settings ***
Documentation     A test suite containing tests related to sessions.
Resource          __keywords.robot
Resource          ../auth.robot
Suite Setup       Clean    test    test
Suite Teardown    Close Browser


*** Test Cases ***
New Session Should Present In Table
    Add Session  New Session  Agenda
    Session Present In Table  New Session


Deleted Session Should Not Present In Table
    Add Session  New Session (two)  Agenda
    Delete Session  New Session (two)
    Session Not Present In Table  New Session (two)


Delete Action Should Delete Right Session
    Add Session  New Session (three)  Agenda
    Add Session  New Session (four)  Agenda
    Add Session  New Session (five)  Agenda
    Delete Session  New Session (four)
    Session Not Present In Table  New Session (four)

