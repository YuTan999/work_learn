import time
import urllib3
from mutation import login, route_groupings, update_route, get_network_interfaces
from graphql_request import send_graphql_mutation, get_cookie_from_login, get_interface_id

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 只适用于全部route都是mpeg/ts输出的情况，如果有其他输出的route不确定会不会引发其他问题
graphql_url = "https://192.168.11.184/graphql"
# graphql_url = "https://192.168.11.185/graphql"
interface_name = "eth0"

cookie = get_cookie_from_login(graphql_url, login())
if not cookie:
    print("Failed to get cookie")
    exit(1)
networkInterfaceId = get_interface_id(get_network_interfaces(), graphql_url, interface_name, cookie)
if not networkInterfaceId:
    print("Failed to get networkInterfaceId")
    exit(1)


def getRouteGroupings():
    response = send_graphql_mutation(route_groupings(), graphql_url, cookie)
    if response:
        return response['data']['routeGroupings']['nodes']
    return None


def updateRouteBitrate(routeids, bitrate):
    for value in routeids:
        response = send_graphql_mutation(update_route(value['id'], bitrate), graphql_url, cookie)
        if response:
            print(f"update_route_bitrate_{value['label']}:\n{response}")
    return None


def main():
    route_groupings = getRouteGroupings()
    bitrate = 60 * 1000000
    updateRouteBitrate(route_groupings, bitrate)


if __name__ == "__main__":
    main()
