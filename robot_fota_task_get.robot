*** Settings ***
Documentation   任务获取测试用例
Resource    app_fota/resources.robot

Suite Setup       start    # 所有测试用例执行之前的操作
Suite Teardown    stop    # 所有测试用例执行完成的操作

Test Setup        setup    # 每条用例开始执行之前
Test Teardown     teardown    # 每条用例执行完成之后

*** Test Cases ***
case065
	[Documentation]  使能条件都满足 - 云端触发 - 判断任务是否可执行 - 无升级任务
	vehicle_data_upload_success    OTA
	disconnect_ecu      IAM     ICC
	${status}   simulation_message  IAM     ICC     check_version_resp_none
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_update_status_req
    fota_assert     ${status}[0]    False    ${status}[1]

case066
	[Documentation]  使能条件都满足 - 云端触发 - 判断任务是否可执行 - 有升级任务 - 配置字无效
	vehicle_data_upload_success    OTA
    fota_function_enable_configuration      False
    ${status}   fota_check_version_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_update_status_req
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    fotaTaskStatus.updateState=0x0F

case066
	[Documentation]  判断任务是否可执行 - 有升级任务：FOTA功能未使能
	vehicle_data_upload_success    OTA
    fota_function_enable_configuration      False
    ${status}   fota_check_version_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_update_status_req
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge   ${status}[1]     fotaTaskStatus.updateState=0x0F

case069
	[Documentation]  使能条件都满足 - 云端触发 - 判断任务是否可执行 - 有升级任务 - 任务可用
	fota_enable_success    True    True   True    True
    ${status}   fota_triggersession
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_check_version_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_update_status_req
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    fotaTaskStatus.updateState=0x00

case070
	[Documentation]  判断任务是否可执行 - 有升级任务：ICC没有收到应答响应
	vehicle_data_upload_success    OTA
    ${status}   fota_check_version_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    disconnect_ecu  IAM     ICC
    ${status}   fota_update_status_req      4
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge   ${status}[1]     fotaTaskStatus.updateState=0x00

case071
	[Documentation]  判断任务是否可执行 - 有升级任务：ICC重发消息过程中收到应答响应
	vehicle_data_upload_success    OTA
    ${status}   fota_check_version_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    disconnect_ecu  IAM     ICC
    ${status}   fota_update_status_req
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge   ${status}[1]     fotaTaskStatus.updateState=0x00
    simulation_message      IAM     ICC     FOTA_UpdateStatusResp
    ${status}   fota_hmi_status
    fota_assert     ${status}[0]    True    ${status}[1]
