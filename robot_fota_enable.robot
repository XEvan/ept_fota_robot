*** Settings ***
Documentation   FOTA使能测试用例
Library     app_fota/robot_manager.py   # 所有测试用例执行前后
Library     app_fota/hw_function.py     # 硬件
Library     app_fota/fota_enable/fota_enable.py    # FOTA使能
Library     app_fota/fota_vehicle_data_upload/vehicle_data_upload.py

Suite Setup       start    # 所有测试用例执行之前的操作
Suite Teardown    stop    # 所有测试用例执行完成的操作

Test Setup        setup    # 每条用例开始执行之前
Test Teardown     teardown    # 每条用例执行完成之后

*** Test Cases ***
case001
	[Documentation]  使能条件都满足 - 云端触发
    fota_function_enable_configuration    True
    vin_validate    True
    security_vehicle_identification_certificate_status    True
    fota_triggersession
    fota_get_logistics_manifest_req

case002
	[Documentation]  使能条件都满足 - 车端自动触发
    fota_function_enable_configuration    True
    vin_validate    True
    security_vehicle_identification_certificate_status    True
    sys_pwr_mode    no_off
    fota_get_logistics_manifest_req

case003
	[Documentation]  使能条件都满足 - 云端触发 - 使能配置字无效
    fota_function_enable_configuration    False
    vin_validate    True
    security_vehicle_identification_certificate_status    True
    fota_triggersession
    fota_get_logistics_manifest_req

case004
	[Documentation]  使能条件都满足 - 云端触发 - VIN码不匹配
    fota_function_enable_configuration    True
    vin_validate    False
    security_vehicle_identification_certificate_status    True
    fota_triggersession
    fota_get_logistics_manifest_req

case005
	[Documentation]  使能条件都满足 - 云端触发 - 车辆身份证书状态为无效
    fota_function_enable_configuration    True
    vin_validate    True
    security_vehicle_identification_certificate_status    False
    fota_triggersession
    fota_get_logistics_manifest_req

case006
	[Documentation]  使能条件都满足 - 车端自动触发 - 使能配置字无效
    fota_function_enable_configuration    False
    vin_validate    True
    security_vehicle_identification_certificate_status    True
    sys_pwr_mode    no_off
    fota_get_logistics_manifest_req

case007
	[Documentation]  使能条件都满足 - 车端自动触发 - VIN码不匹配
    fota_function_enable_configuration    True
    vin_validate    False
    security_vehicle_identification_certificate_status    True
    sys_pwr_mode    no_off
    fota_get_logistics_manifest_req

case008
	[Documentation]  使能条件都满足 - 车端自动触发 - 车辆身份证书状态为无效
    fota_function_enable_configuration    True
    vin_validate    True
    security_vehicle_identification_certificate_status    False
    sys_pwr_mode    no_off
    fota_get_logistics_manifest_req