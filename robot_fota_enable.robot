*** Settings ***
Documentation   FOTA使能测试用例
Resource    app_fota/resources.robot

Suite Setup       start    # 所有测试用例执行之前的操作
Suite Teardown    stop    # 所有测试用例执行完成的操作

Test Setup        setup    # 每条用例开始执行之前
Test Teardown     teardown    # 每条用例执行完成之后

*** Test Cases ***
case001
	[Documentation]  使能条件都满足 - 云端触发
	fota_enable_precondition
    ${status}   fota_triggersession
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]

case002
	[Documentation]  使能条件都满足 - 车端自动触发
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]

case003
	[Documentation]  使能条件都满足 - 云端触发 - 使能配置字无效
	fota_enable_precondition    True    False   True    True
    ${status}   fota_triggersession
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]

case004
	[Documentation]  使能条件都满足 - 云端触发 - VIN码不匹配
	fota_enable_precondition    True    True   False    True
    ${status}   fota_triggersession
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]

case005
	[Documentation]  使能条件都满足 - 云端触发 - 车辆身份证书状态为无效
	fota_enable_precondition    True    True   True    False
    ${status}   fota_triggersession
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]

case006
	[Documentation]  使能条件都满足 - 车端自动触发 - 使能配置字无效
	fota_enable_precondition    True    False   True    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]

case007
	[Documentation]  使能条件都满足 - 车端自动触发 - VIN码不匹配
	fota_enable_precondition    True    True   False    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]

case008
	[Documentation]  使能条件都满足 - 车端自动触发 - 车辆身份证书状态为无效
	fota_enable_precondition    True    True   True    False
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]