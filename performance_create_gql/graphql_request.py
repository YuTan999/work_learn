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


def send_graphql_mutation(mutation, url, cookie=None):
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

        try:
            response_data = response.json()

            if response.status_code == 200:
                return response_data  # 成功响应

            elif response.status_code == 400:
                if 'errors' in response_data and response_data['errors']:
                    error_message = response_data['errors'][0].get('message', 'Unknown error')
                    print(f"GraphQL Validation Error: {error_message}")
                else:
                    print(f"HTTP 400 Error: {response.text}")
                return None

        except ValueError:
            # JSON解析失败
            print(f"Error: Invalid JSON response (Status {response.status_code})")
            print(f"Response: {response.text}")
            return None

        # 其他状态码
        print(f"Unexpected HTTP Status: {response.status_code}")
        print(f"Response: {response.text}")
        return None

    except requests.RequestException as e:
        print(f"Error sending GraphQL mutation: {e}")
        return None
