import json
import yaml


def json_loads(src='site_info.json'):
    with open(src) as load_f:
        load_dict = json.load(load_f)
    return load_dict


def load_ua(device, win_mac, brower):
    with open('./headers_repo') as file:
        load_dict = yaml.safe_load(file)
    ua = load_dict[device][win_mac][brower]
    return ua


def load_headers(device, win_mac, brower):
    ua = load_ua(device, win_mac, brower)[0]
    headers = {'user-agent': ua}
    return headers
