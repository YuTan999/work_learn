import requests
import time

def send_graphql_query(query, url):
   headers = {'Content-Type': 'application/json'}
   data = {'query': query}
   try:
       response = requests.post(url, json=data, headers=headers)
       response.raise_for_status()
       return response.json()
   except requests.RequestException as e:
       print(f"Error sending GraphQL query: {e}")
       return None

def send_graphql_mutation(mutation, url):
   headers = {'Content-Type': 'application/json'}
   data = {'query': mutation}
   try:
       response = requests.post(url, json=data, headers=headers)
       response.raise_for_status()
       return response.json()
   except requests.RequestException as e:
       print(f"Error sending GraphQL mutation: {e}")
       return None

