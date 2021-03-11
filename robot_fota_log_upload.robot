*** Settings ***
Documentation   任务执行测试用例
Resource    app_fota/resources.robot

Suite Setup       start    # 所有测试用例执行之前的操作
Suite Teardown    stop    # 所有测试用例执行完成的操作

Test Setup        setup    # 每条用例开始执行之前
Test Teardown     teardown    # 每条用例执行完成之后

*** Test Cases ***
case0259
	[Documentation]  使能条件都满足 - 云端触发 - 上传成功
	fota_enable_precondition    True    True   True    True     #使能条件满足
    ${status}   fota_triggersession     # 云端触发
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_update_status_req
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    fotaTaskStatus.updateState=0x07     # update successful

    ${status}   fota_triggersession     GetLog
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_log_upload_url_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_log_upload_url_resp
    fota_assert     ${status}[0]    True    ${status}[1]

    ${status}   fota_report_upload_log_result_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_report_upload_log_result_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    fota_report_upload_log_result_resp_status_code_judge    ${status}[1]    0
