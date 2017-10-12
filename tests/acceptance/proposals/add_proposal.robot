*** Settings ***
Documentation     A test suite containing tests related to proposals.
Resource          __keywords.robot
Resource          ../auth.robot
Suite Setup       Clean    test    test
Suite Teardown    Close Browser


*** Test Cases ***
New Proposal Should Present In Table
    Add Proposal  New Proposal  With Some Content
    Proposal Present In Table  New Proposal


Deleted Proposal Should Not Present In Table
    Add Proposal  To Be Deleted Proposal  With Some Content
    Delete Proposal  To Be Deleted Proposal
    Proposal Not Present In Table  To Be Deleted Proposal


Delete Action Should Delete Right Proposal
    Add Proposal  To Be Deleted Proposal (One)  With Some Content
    Add Proposal  To Be Deleted Proposal (Two)  With Some Content
    Add Proposal  To Be Deleted Proposal (Three)  With Some Content
    Delete Proposal  To Be Deleted Proposal (Two)
    Proposal Not Present In Table  To Be Deleted Proposal (Two)

