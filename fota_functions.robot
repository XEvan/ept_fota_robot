*** Settings ***
Library           app_fota/robot_manager.py     # 所有测试用例执行前后
Library           app_fota/hw_function.py       # 硬件
Library           app_fota/fota_enable/function_fota_enable.py      #

Suite Setup       start    # 所有测试用例执行之前的操作
Suite Teardown    stop    # 所有测试用例执行完成的操作

Test Setup        hw_setup    # 每条用例开始执行之前
Test Teardown     hw_teardown    # 每条用例执行完成之后

*** Test Cases ***
case001
    fota_function_enable_configuration    True
    vin_validate    True
    security_vehicle_identification_certificate_status    True
    fota_triggersession    IAM    ICC
    fota_get_logistics_manifest_req    ICC    IAM

case002
    fota_function_enable_configuration    True
    vin_validate    True
    security_vehicle_identification_certificate_status    True
    sys_pwr_mode    no_off
    fota_get_logistics_manifest_req    ICC    IAM

case003
    fota_function_enable_configuration    False
    vin_validate    True
    security_vehicle_identification_certificate_status    True
    fota_triggersession    IAM    ICC
    fota_get_logistics_manifest_req    ICC    IAM

case004
    fota_function_enable_configuration    True
    vin_validate    False
    security_vehicle_identification_certificate_status    True
    fota_triggersession    IAM    ICC
    fota_get_logistics_manifest_req    ICC    IAM

case005
    fota_function_enable_configuration    True
    vin_validate    True
    security_vehicle_identification_certificate_status    False
    fota_triggersession    IAM    ICC
    fota_get_logistics_manifest_req    ICC    IAM

case006
    fota_function_enable_configuration    False
    vin_validate    True
    security_vehicle_identification_certificate_status    True
    sys_pwr_mode    no_off
    fota_get_logistics_manifest_req    ICC    IAM

case007
    fota_function_enable_configuration    True
    vin_validate    False
    security_vehicle_identification_certificate_status    True
    sys_pwr_mode    no_off
    fota_get_logistics_manifest_req    ICC    IAM

case008
    fota_function_enable_configuration    True
    vin_validate    True
    security_vehicle_identification_certificate_status    False
    sys_pwr_mode    no_off
    fota_get_logistics_manifest_req    ICC    IAM