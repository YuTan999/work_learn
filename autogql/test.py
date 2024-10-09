from graphql_queries import get_device_info
from graphql_requests import send_graphql_query

graphql_url = "http://10.200.1.33/graphql"

get_sid = get_sid()
query = get_device_info()
result = send_graphql_query(query, graphql_url)
if result:
    print(result)
