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
	fota_enable_success    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]

case010
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - 配置字无效
	fota_enable_success    True    True   True    True
    sys_pwr_mode    no_off
    fota_function_enable_configuration    False
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    False    ${status}[1]

case011
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - 设置系统电源模式为OFF
	fota_enable_success    True    True   True    True
    sys_pwr_mode    off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    False    ${status}[1]

case012
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - 设置外网不可访问
	fota_enable_success    True    True   True    True
    sys_pwr_mode    no_off
    network_access  False
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    False    ${status}[1]

case013     #疑问：仿真报文方案？
	[Documentation]  使能条件都满足 - 车端自动触发 - 获取物流清单的前提条件不满足 - 物流清单解析失败
	disconnect_ecu      IAM     ICC
	fota_enable_success    True    True   True    True
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
	fota_enable_success    True    True   True    True
    sys_pwr_mode    no_off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]
    disconnect_ecu      IAM     ICC
    ${status}   fota_get_logistics_manifest_resp
    fota_assert     ${status}[0]    False    ${status}[1]

case015
	[Documentation]  车辆自动触发 - 获取车辆物流数据清单 - 获取物流数据清单：成功
	vehicle_data_list_obtain_success

case016
	[Documentation]  车辆自动触发 - 收集物流数据 - 物流数据收集失败 - 防火墙认证失败
	vehicle_data_list_obtain_success
    firewall_certificate_config     False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    logisticsDatainfo.ecuNum=0
    result_dict_judge     ${status}[1]    logisticsDatainfo.logisticsDataResult=1

case017
	[Documentation]  车辆自动触发 - 收集物流数据 - 物流数据收集失败 - FOTA使能功能未使能
	vehicle_data_list_obtain_success
    fota_function_enable_configuration     False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    logisticsDatainfo.ecuNum=0
    result_dict_judge     ${status}[1]    logisticsDatainfo.logisticsDataResult=3

case018
	[Documentation]  车辆自动触发 - 收集物流数据 - 物流数据收集失败 - VIN码不匹配
	vehicle_data_list_obtain_success
    vin_validate     False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    logisticsDatainfo.ecuNum=0
    result_dict_judge     ${status}[1]    logisticsDatainfo.logisticsDataResult=4

case019
	[Documentation]  车辆自动触发 - 收集物流数据 - 物流数据收集失败 - 车辆身份证书状态为无效
	vehicle_data_list_obtain_success
    security_vehicle_identification_certificate_status     False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    logisticsDatainfo.ecuNum=0
    result_dict_judge     ${status}[1]    logisticsDatainfo.logisticsDataResult=5

case020
	[Documentation]  车辆自动触发 - 收集物流数据 - 物流数据收集失败 - 诊断设备接入
	vehicle_data_list_obtain_success
	diagnosis_config    True    True
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    logisticsDatainfo.ecuNum=0
    result_dict_judge     ${status}[1]    logisticsDatainfo.logisticsDataResult=2

case027
	[Documentation]  车辆自动触发 - 物流数据的上传 - 物流数据上传前置条件不满足 - FOTA使能功能未使能
	ecu_data_gain_success
    fota_function_enable_configuration      False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    False    ${status}[1]

case028
	[Documentation]  车辆自动触发 - 物流数据的上传 - 物流数据上传前置条件不满足 - 车辆未上电
	ecu_data_gain_success
    sys_pwr_mode    off
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    False    ${status}[1]

case029     # 如何配置OTA后台
	[Documentation]  车辆自动触发 - 物流数据的上传 - 物流数据上传前置条件不满足 - 没到上传时间间隔
	ecu_data_gain_success
    # 配置OTA后台物流上传时间间隔小于预定时间
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    False    ${status}[1]

case030
	[Documentation]  车辆自动触发 - 物流数据的上传 - 物流数据上传前置条件不满足 - 外网不可访问
	ecu_data_gain_success
    network_access    False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    False    ${status}[1]

case031
	[Documentation]  使能条件都满足 - 车辆自动触发 - 物流数据的上传 - 物流数据上传前置条件不满足 - OTA后台不响应
	ecu_data_gain_success
    disconnect_ecu      IAM     ICC
    ${status}   fota_check_version_req      times=4
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_check_version_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    responseInfo.statusCode=0

case032
	[Documentation]  使能条件都满足 - 车端自动触发 - 物流数据的上传 - 物流数据上传成功
	ecu_data_gain_success
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_check_version_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    responseInfo.statusCode=0

case033
	[Documentation]  使能条件都满足 - 云端触发 - 获取物流清单的前提条件 - 条件满足
	fota_enable_success    True    True   True    True
    ${status}   fota_triggersession
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    True    ${status}[1]

case034
	[Documentation]  使能条件都满足 - 云端触发 - 获取物流清单的前提条件 - 条件不满足 - 配置字无效
	fota_enable_success    True    True   True    True
    ${status}   fota_triggersession
    fota_assert     ${status}[0]    True    ${status}[1]
    fota_function_enable_configuration    False
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    False    ${status}[1]

case035
	[Documentation]  使能条件都满足 - 云端触发 - 获取物流清单的前提条件 - 条件不满足 - 设置系统电源模式为OFF
	fota_enable_success    True    True   True    True
    ${status}   fota_triggersession
    fota_assert     ${status}[0]    True    ${status}[1]
    sys_pwr_mode    off
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    False    ${status}[1]

case036
	[Documentation]  使能条件都满足 - 云端触发 - 获取物流清单的前提条件 - 条件不满足 - 外网不可访问
	fota_enable_success    True    True   True    True
    ${status}   fota_triggersession
    fota_assert     ${status}[0]    True    ${status}[1]
    network_access      False
    ${status}   fota_get_logistics_manifest_req
    fota_assert     ${status}[0]    False    ${status}[1]



case041
	[Documentation]  OTA管理平台下发命令触发 - 收集物流数据 - 物流数据收集失败 - FOTA使能功能未使能
	vehicle_data_list_obtain_success    OTA
    fota_function_enable_configuration      False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
	result_dict_judge   ${status}[1]    logisticsDatainfo.ecuNum=0
	result_dict_judge   ${status}[1]    logisticsDatainfo.logisticsDataResult=3

case042
	[Documentation]  OTA管理平台下发命令触发 - 收集物流数据 - 物流数据收集失败 - VIN码不匹配
	vehicle_data_list_obtain_success    OTA
    vin_validate     False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
	result_dict_judge   ${status}[1]    logisticsDatainfo.ecuNum=0
	result_dict_judge   ${status}[1]    logisticsDatainfo.logisticsDataResult=4

case043
	[Documentation]  OTA管理平台下发命令触发 - 收集物流数据 - 物流数据收集失败 - 车辆身份证书状态为无效
	vehicle_data_list_obtain_success    OTA
    security_vehicle_identification_certificate_status  False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
	result_dict_judge   ${status}[1]    logisticsDatainfo.ecuNum=0
	result_dict_judge   ${status}[1]    logisticsDatainfo.logisticsDataResult=5

case044
	[Documentation]  OTA管理平台下发命令触发 - 收集物流数据 - 物流数据收集失败 - 诊断设备接入
	vehicle_data_list_obtain_success    OTA
	diagnosis_config    True    True
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
	result_dict_judge   ${status}[1]    logisticsDatainfo.ecuNum=0
	result_dict_judge   ${status}[1]    logisticsDatainfo.logisticsDataResult=2



case047
	[Documentation]  OTA管理平台下发命令触发 - 收集物流数据 - 物流数据收集失败 - 物流数据收集超时：车辆休眠
	vehicle_data_list_obtain_success    OTA
	vehicle_sleep    True
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]

case050
	[Documentation]  OTA管理平台下发命令触发 - 物流数据的上传 - 物流数据上传前置条件不满足 - FOTA使能功能未使能
	ecu_data_gain_success    OTA
    fota_function_enable_configuration      False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    False    ${status}[1]

case051
	[Documentation]  OTA管理平台下发命令触发 - 物流数据的上传 - 物流数据上传前置条件不满足 - 车辆未上电
	ecu_data_gain_success    OTA
    sys_pwr_mode  False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    False    ${status}[1]

case053
	[Documentation]  OTA管理平台下发命令触发 - 物流数据的上传 - 物流数据上传前置条件不满足 - 外网不可访问
	ecu_data_gain_success    OTA
    network_access  False
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    False    ${status}[1]

case055
	[Documentation]  OTA管理平台下发命令触发 - 物流数据的上传 - 物流数据上传失败
	ecu_data_gain_success    OTA
	disconnect_ecu  IAM     ICC
    # 断开IAM与ICC
    ${status}   fota_check_version_req      4
    fota_assert     ${status}[0]    False    ${status}[1]

case056
	[Documentation]  OTA管理平台下发命令触发 - 物流数据的上传 - 物流数据上传成功：前置条件满足
	ecu_data_gain_success    OTA
    ${status}   fota_check_version_req
    fota_assert     ${status}[0]    True    ${status}[1]
    ${status}   fota_check_version_resp
    fota_assert     ${status}[0]    True    ${status}[1]
    result_dict_judge     ${status}[1]    responseInfo.statusCode=0

