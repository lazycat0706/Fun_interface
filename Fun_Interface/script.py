from Fun_Interface.common import *
import json
import threading


def check_save(loc_num, api_name, expect_result, response):
    check(response, expect_result, loc_num, case_path)
    save_variable(api_name, response, loc_num, case_path)
    print(response, expect_result)


def run_interface(env, qsxq_type):
    token = ""
    if qsxq_type == "comm" or qsxq_type == "erp":
        token = get_login_token(qsxq_type)
    loc_num = 2
    base_url = get_env_url(env, qsxq_type)
    for interface_info in data_list:
        api_name = interface_info[0]
        url = base_url + interface_info[2].strip()
        headers = get_headers(qsxq_type, token)
        someting = interface_info[3]
        post_data = str(interface_info[4])
        method = interface_info[1]
        title = interface_info[7]
        expect_result = json.loads(interface_info[5])
        print(title + '-' + method + '请求参数: ' + post_data)
        if someting == 'skip':
            print('跳过执行')
            loc_num += 1
            continue
        elif someting == "normal":
            post_data = json.loads(post_data)
            response = json.loads(send_post_json_request(url, headers, post_data))
            check_save(loc_num, api_name, expect_result, response)
            loc_num += 1
        else:
            if post_data != "nan":
                post_data = json.loads(post_data)
            else:
                post_data = ""
            if method.lower() == "get":
                response = json.loads(send_get_request(url, headers, post_data))
                check_save(loc_num, api_name, expect_result, response)
                loc_num += 1
            elif method.lower() == "post":
                response = json.loads(send_post_params_request(url, headers, post_data))
                check_save(loc_num, api_name, expect_result, response)
                loc_num += 1


if __name__ == '__main__':
    qsxq_type = "applet"
    env = "sit"
    case_path_dict = {
        "app": "D:/Python development/Fun_Interface/app_interface.xlsx",
        "erp": "D:/Python development/Fun_Interface/erp_interface.xlsx",
        "applet": "D:/Python development/Fun_Interface/applet_interface.xlsx"
    }
    case_path = case_path_dict[qsxq_type]
    data_list = get_excel(case_path)
    run_interface(env, qsxq_type)
