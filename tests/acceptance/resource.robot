*** Settings ***
Documentation     A resource file with reusable keywords and variables.
Library           SeleniumLibrary
Library           aux.py

*** Variables ***
${SERVER}           localhost:5000
${BROWSER}          Chrome
${DELAY}            0
${VALID USER}       test
${VALID PASSWORD}   test
${LOGIN URL}        http://${SERVER}/account/login
${WELCOME URL}      http://${SERVER}/account/
${ERROR URL}        http://${SERVER}/error.html
