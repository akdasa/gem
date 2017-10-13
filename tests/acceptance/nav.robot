
*** Keywords ***
Navigation Bar Item Shoud Be Highlighted
    [Arguments]  ${title}
    ${key}=  Get Element Attribute  jquery:ul.nav > li:contains('${title}')  class
    Should Contain  ${key}  active

