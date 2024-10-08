import requests

url = 'http://10.200.8.104/graphql'
mutation = '''
mutation {
     login(
          passwd: "proav101",
          user: "admin"
        ) {
          errorType {
            code
            message
          }
          user
          sid
        }
    }

'''


response = requests.post(url, json={'query': mutation})
print(response.json())