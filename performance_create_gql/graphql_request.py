import requests


def get_cookie_from_login(url, mutation):
    headers = {
        "content-type": "application/json",
    }
    payload = {
        "query": mutation
    }
    try:
        response = requests.post(url, json=payload, headers=headers, verify=False)
        if response.ok:
            return response.json()["data"]["login"]["cookie"]["value"]
        else:
            print(f"Error: Server returned status code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error sending GraphQL mutation: {e}")
        return None


def get_interface_id(mutation, url, interface_name=None, cookie=None):
    headers = {
        "content-type": "application/json",
    }
    if cookie:
        headers["cookie"] = f"auth_session={cookie}"
    payload = {
        "query": mutation
    }
    try:
        response = requests.post(url, json=payload, headers=headers, verify=False)
        if response.ok:
            data = response.json()["data"]["device"]  # 修改2：先获取完整数据

            # 修改3：新增接口查找逻辑
            if interface_name:
                interfaces = data["networkInterfaces"]["edges"]
                for edge in interfaces:
                    if edge["node"]["label"] == interface_name:
                        return edge["node"]["id"]
                print(f"Error: Interface '{interface_name}' not found")
                return None
            else:
                # 默认返回网关id
                return data["networkDefaultGateway"]["id"]
        else:
            print(f"Error: Server returned status code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error sending GraphQL mutation: {e}")
        return None
    except KeyError as e:  # 修改4：新增异常处理
        print(f"Error parsing response data: {e}")
        return None


# def send_graphql_mutation(mutation, url, cookie=None):
#     headers = {
#         "content-type": "application/json",
#     }
#     if cookie:
#         headers["cookie"] = f"auth_session={cookie}"
#     payload = {
#         "query": mutation
#     }
#
#     try:
#         response = requests.post(url, json=payload, headers=headers, verify=False)
#
#         try:
#             response_data = response.json()
#             print(f"Response Data: {response_data}")  # 打印响应数据
#
#             if response.status_code == 200:
#                 return response_data  # 成功响应
#
#             elif response.status_code == 400:
#                 if 'errors' in response_data and response_data['errors']:
#                     error_message = response_data['errors'][0].get('message', 'Unknown error')
#                     print(f"GraphQL Validation Error: {error_message}")
#                 else:
#                     print(f"HTTP 400 Error: {response.text}")
#                 return None
#
#         except ValueError:
#             # JSON解析失败
#             print(f"Error: Invalid JSON response (Status {response.status_code})")
#             print(f"Response: {response.text}")
#             return None
#
#         # 其他状态码
#         print(f"Unexpected HTTP Status: {response.status_code}")
#         print(f"Response: {response.text}")
#         return None
#
#     except requests.RequestException as e:
#         print(f"Error sending GraphQL mutation: {e}")
#         return None


def send_graphql_mutation(mutation, url, cookie=None, operation_name=None):
    headers = {
        "content-type": "application/json",
    }
    if cookie:
        headers["cookie"] = f"auth_session={cookie}"
    payload = {
        "query": mutation
    }

    try:
        response = requests.post(url, json=payload, headers=headers, verify=False)

        # 基础结果结构
        result = {
            "success": False,
            "error": None,
            "data": None,
            "raw_response": None
        }

        try:
            response_data = response.json()
            result["raw_response"] = response_data
        except ValueError:
            result["error"] = f"Invalid JSON response (Status {response.status_code}): {response.text}"
            return result

        # ✅ 状态码200
        if response.status_code == 200:
            # GraphQL错误
            if 'errors' in response_data and response_data['errors']:
                result["error"] = f"GraphQL error: {response_data['errors'][0].get('message', 'Unknown error')}"
                result["data"] = response_data.get('data')
                return result

            # 业务逻辑检查
            if operation_name:
                data_key = f'create{operation_name}'
                if data_key in response_data.get('data', {}):
                    result_data = response_data['data'][data_key]
                    # 特殊处理 RouteFromTemplate 操作，其返回对象键名为 'route' 而不是 'routeFromTemplate'
                    if operation_name == "RouteFromTemplate":
                        object_key = "route"
                    else:
                        object_key = operation_name[0].lower() + operation_name[1:]

                    if object_key not in result_data or result_data[object_key] is None:
                        error_info = result_data.get('errorType', {})
                        error_code = error_info.get('code', 'UNKNOWN_ERROR')
                        error_message = error_info.get('message', 'Unknown creation error')
                        result["error"] = f"Creation failed: {error_code} - {error_message}"
                        result["data"] = response_data.get('data')
                        return result

            # 所有检查通过
            result["success"] = True
            result["data"] = response_data['data']
            return result

        # ✅ 状态码400
        elif response.status_code == 400:
            if 'errors' in response_data and response_data['errors']:
                error_message = response_data['errors'][0].get('message', 'Unknown error')
                result["error"] = f"GraphQL Validation Error: {error_message}"
            else:
                result["error"] = f"HTTP 400 Error: {response.text}"
            result["data"] = response_data.get('data')
            return result

        # ✅ 其他状态码
        else:
            result["error"] = f"Unexpected HTTP Status {response.status_code}: {response.text}"
            result["data"] = response_data.get('data')
            return result

    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"Network request error: {str(e)}",
            "data": None,
            "raw_response": None
        }
