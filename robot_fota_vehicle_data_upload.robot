*** Settings ***
Documentation   FOTA车辆数据上传测试用例
Resource    app_fota/resources.robot

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
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - 配置字无效
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

case013     #疑问：仿真报文方案？
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
    result_dict_judge     ${status}[1]    logisticsDatainfo.ecuNum=0
    result_dict_judge     ${status}[1]    logisticsDatainfo.logisticsDataResult=7

case014
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - 获取超时
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]
    disconnect_ecu      IAM     ICC
    ${status}   fota_get_logistics_manifest_resp
    fota_assert     ${status}[0]    False    ${status}[1]

case015
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - 获取成功
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    responseInfo.statusCode=0

case016
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - 配置ICC防火墙认证失败
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    firewall_certificate_config     False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    logisticsDatainfo.ecuNum=0
    result_dict_judge     ${status}[1]    logisticsDatainfo.logisticsDataResult=1

case017
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - 配置字无效
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    fota_function_enable_configuration     False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    logisticsDatainfo.ecuNum=0
    result_dict_judge     ${status}[1]    logisticsDatainfo.logisticsDataResult=3

case018
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - 配置VIN不一致
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    vin_validate     False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    logisticsDatainfo.ecuNum=0
    result_dict_judge     ${status}[1]    logisticsDatainfo.logisticsDataResult=4

case019
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - 配置身份证书状态无效
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    security_vehicle_identification_certificate_status     False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    logisticsDatainfo.ecuNum=0
    result_dict_judge     ${status}[1]    logisticsDatainfo.logisticsDataResult=1

case027
	[Documentation]  使能条件都满足 - 车辆自动触发 - 物流数据的上传 - 物流数据上传前置条件不满足 - 配置字无效
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    fota_function_enable_configuration      False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    False    ${status}[1]

case028
	[Documentation]  使能条件都满足 - 车辆自动触发 - 物流数据的上传 - 物流数据上传前置条件不满足 - 车辆未上电
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    sys_pwr_mode    off
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    False    ${status}[1]

case030
	[Documentation]  使能条件都满足 - 车辆自动触发 - 物流数据的上传 - 物流数据上传前置条件不满足 - 外网不可访问
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    network_access    False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    False    ${status}[1]

case031
	[Documentation]  使能条件都满足 - 车辆自动触发 - 物流数据的上传 - 物流数据上传前置条件不满足 - OTA后台不响应
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    disconnect_ecu      IAM     ICC
    ${status}   fota_check_version_req      times=4
    fota_assert     ${status}[0]    True    ${status}[1]

case032
	[Documentation]  使能条件都满足 - 车端自动触发 - 物流数据的上传 - 物流数据上传成功
	fota_enable_precondition    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_check_version_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    responseInfo.statusCode=0

case033
	[Documentation]  使能条件都满足 - 云端触发 - 获取物流清单的前提条件 - 条件满足
	fota_enable_precondition    True    True   True    True
    ${status}   fota_triggersession
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]

case034
	[Documentation]  使能条件都满足 - 云端触发 - 获取物流清单的前提条件 - 条件不满足 - 配置字无效
	fota_enable_precondition    True    True   True    True
    ${status}   fota_triggersession
    fota_assert     ${status}[0]    True    ${status}[1]
    fota_function_enable_configuration    False
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    False    ${status}[1]

case035
	[Documentation]  使能条件都满足 - 云端触发 - 获取物流清单的前提条件 - 条件不满足 - 设置系统电源模式为OFF
	fota_enable_precondition    True    True   True    True
    ${status}   fota_triggersession
    fota_assert     ${status}[0]    True    ${status}[1]
    sys_pwr_mode    off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    False    ${status}[1]

case036
	[Documentation]  使能条件都满足 - 云端触发 - 获取物流清单的前提条件 - 条件不满足 - 外网不可访问
	fota_enable_precondition    True    True   True    True
    ${status}   fota_triggersession
    fota_assert     ${status}[0]    True    ${status}[1]
    network_access      False
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    False    ${status}[1]

case056
	[Documentation]  使能条件都满足 - 云端触发 - 获取物流清单的前提条件 - 物流数据的上传 - 物流数据上传成功
	fota_enable_precondition    True    True   True    True
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
    result_dict_judge     ${status}[1]    responseInfo.statusCode=0