*** Settings ***
Documentation   FOTA使能测试用例
Library     app_fota/hw_function.py

*** Test Cases ***
case001
	[Documentation]  使能条件都满足 - 云端触发
    hello   0x100   0x100