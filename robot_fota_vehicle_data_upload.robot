*** Settings ***
Documentation   FOTA车辆数据上传测试用例
Resource    app_fota/importer.robot

Suite Setup       start    # 所有测试用例执行之前的操作
Suite Teardown    stop    # 所有测试用例执行完成的操作

Test Setup        setup    # 每条用例开始执行之前
Test Teardown     teardown    # 每条用例执行完成之后

*** Test Cases ***
case009
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件满足
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]

case010
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - FOTA使能功能未使能
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    fota_function_enable_configuration    False
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    False    ${status}[1]

case011
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - 设置系统电源模式为OFF
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    False    ${status}[1]

case012
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - 设置外网不可访问
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    network_access  False
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    False    ${status}[1]

case013     #疑问
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - 物流清单解析失败
	disconnect_ecu      IAM     ICC
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   simulation_message  ICC     IAM     logistic_mnf_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   simulation_message  IAM     ICC     logistic_mnf_resp_error_info
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    False    ${status}[1]

case014
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - 获取超时
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   simulation_message  ICC     IAM     logistic_mnf_req
    fota_assert     ${status}[0]    True    ${status}[1]
    disconnect_ecu      IAM     ICC
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    False    ${status}[1]

case015
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - 获取成功
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   simulation_message  ICC     IAM     logistic_mnf_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_check_version_resp
    fota_assert     ${status}[0]    True    ${status}[1]