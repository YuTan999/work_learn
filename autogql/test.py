from graphql_queries import get_device_info
from graphql_mutations import update_fan_speed,get_sid
from graphql_requests import send_graphql_query


# graphql_url = "http://10.200.1.40/graphql"
#
# get_sid = get_sid()
# # query = update_fan_speed('beQenn77gZEzhMUJeSenWyhufq54yNsX','{fanspeedControlMode:FAN_SPEED_CONTROL_MODE_AUTO}')
# query = update_fan_speed('beQenn77gZEzhMUJeSenWyhufq54yNsX','{fanspeedControlMode:FAN_SPEED_CONTROL_MODE_MANUAL,fanspeedPercentage:100}')
# print(query)
# result = send_graphql_query(query, graphql_url)
# if result:
#     print(result)


fanspeedinput_test = f'{{fanspeedControlMode:FAN_SPEED_CONTROL_MODE_{mode},fanspeedPercentage:{speed}}}'


fstest = fanspeedinput_test(mode='AUTO',speed=100)
print(fstest)