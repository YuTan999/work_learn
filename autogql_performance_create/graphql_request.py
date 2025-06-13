import requests


def send_graphql_mutation(mutation, url):
    headers = {
        "content-type": "application/json",
        # 从浏览器复制来的，后面可以用Selenium去获取保存在本地
        # "cookie": "auth_session=205d5307-6d89-44c0-a6da-1a7fbf69e056"
        "cookie": "auth_session=1bd81c2b-42e8-4738-9d1c-8c4180a4cc45"
    }
    payload = {
        "query": mutation
    }

    try:
        response = requests.post(url, json=payload, headers=headers, verify=False)
        if response.ok:
            return response.json()
        else:
            print(f"Error: Server returned status code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error sending GraphQL mutation: {e}")
        return None
