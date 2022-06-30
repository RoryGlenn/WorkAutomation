import urllib3
from winwifi import WinWiFi

from time import sleep


WIFI_SSID = "SENAHOUSE 5G FL-3A"


def is_internet_connected() -> bool:
    try:
        urllib3.connection_from_url('https://www.youtube.com/', timeout=1)
    except Exception as e:
        print(e)
        return False
    return True


def is_router_connected() -> bool:
    for interface in WinWiFi.get_connected_interfaces():
        print(interface.name, interface.ssid, interface.state)
        return interface.state == 'connected'
    return False


if __name__ == '__main__':
    while True:
        if is_internet_connected() and is_router_connected():
            break
        else:
            WinWiFi.connect(WIFI_SSID)
            sleep(10)
