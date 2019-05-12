*** Settings ***
Resource  ../../Common.robot

Force Tags  SP0030_v3.2.0  930

Test Setup     <Your Setup here>
Test Teardown  <Your Teardown Here>

Variables  ../../System.yaml

*** Test Cases ***
DR_6.11.3_DR_5.1.1_DR_2.3.3 - <test_description>
    [Documentation]  <urs_id>: <urs_description - as in Confluence>
    [Tags]  DR_6.11.3  DR_5.1.1  DR_2.3.3

    Given Open Web Browser  ${ICOTRIAL_GTM.
    Then

    Take Screenshot  SP0030_<module>_<urs>_SS_01_<description>.png
    Log  Requirement <> is verified successfully
