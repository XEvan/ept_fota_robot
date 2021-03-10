*** Settings ***
Documentation   任务执行测试用例
Resource    app_fota/resources.robot

Suite Setup       start    # 所有测试用例执行之前的操作
Suite Teardown    stop    # 所有测试用例执行完成的操作

Test Setup        setup    # 每条用例开始执行之前
Test Teardown     teardown    # 每条用例执行完成之后

*** Test Cases ***
case0163
	[Documentation]  使能条件都满足 - 云端触发 - 静默升级 - 升级成功
	fota_enable_precondition    True    True   True    True     #使能条件满足
    ${status}   fota_triggersession     # 云端触发
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_check_version_resp
    fota_assert     ${status}[0]    True    ${status}[1]

	check_version_resp_update_mode_judge   ${status}[1]    0x04     # 解析是否是静默升级
    ${status}   fota_update_status_req
    fota_assert     ${status}[0]    True    ${status}[1]
    fota_update_status_req_update_state_judge  ${status}[1]    0x02     # 下载完成
    ${status}   fota_update_status_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_hmi_status
    fota_assert     ${status}[0]    True    ${status}[1]
    fota_hmi_status_update_mode_judge   ${status}[1]    0x01
    ${status}   fota_hmi_update_progress
    fota_assert     ${status}[0]    True    ${status}[1]
    fota_hmi_update_progress_update_status_judge   ${status}[1]    0x01    # download progressing
    ${status}   fota_update_status_req
    fota_assert     ${status}[0]    True    ${status}[1]
    fota_update_status_req_update_state_judge  ${status}[1]    0x05    # update progressing
    ${status}   fota_hmi_update_progress
    fota_assert     ${status}[0]    True    ${status}[1]
    fota_hmi_update_progress_update_status_judge   ${status}[1]    0x00
    ${status}   fota_update_status_req
    fota_assert     ${status}[0]    True    ${status}[1]
    fota_update_status_req_update_state_judge  ${status}[1]    0x07     # update successful
