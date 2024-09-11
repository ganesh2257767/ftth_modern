from datetime import datetime
import requests
import json
from typing import Dict, Tuple, List
import dotenv
import os

dotenv.load_dotenv()

user = os.getenv('uname')
password = os.getenv('pw')


def load_address_json():
    with open("addresses.json", "r") as f:
        addresses = json.load(f)
        print("Addresses:", addresses)
        return addresses

DATA = load_address_json()

class AddressException(Exception):
    """Raised when the address is invalid (Decided when split)."""
    pass


def get_token(get_token_url: str) -> str | Dict:
    now = datetime.now().strftime('%a %b %d %H:%M:%S %Y')
    get_token: str = f"""{{
                        "apiName": "checkFTTHFeasibility",
                        "apiVersion": "V2",
                        "userName": "{user}",
                        "password": "{password}",
                        "sessionId": "{now}",
                        "sourceApp": "IDA"
                    }}"""
    get_token_json = json.loads(get_token)

    try:
        token_response = requests.post(
            get_token_url, json=get_token_json).json()
    except requests.exceptions.ConnectionError:
        return {"success": False, "errorMessage": "Make sure VPN is connected, or check network connection."}
    except json.decoder.JSONDecodeError:
        return {"success": False, "errorMessage": "Token generation failed!"}
    else:
        return token_response


def check_feasibility(env, address) -> Dict | str:
    get_token_url = DATA[env]['get_token']
    check_feasibility_url = DATA[env]['check_feasibility']

    try:
        street_num, street_name, city, state, zipc = format_address(address)
    except AddressException:
        return {"success": False, "errorMessage": "Invalid Address."}

    token_response = get_token(get_token_url)
    print(token_response)

    if token_response['success']:
        check_feasibility_request = f"""{{
                                            "sessionId" : "{token_response['sessionId']}",
                                            "sourceApp" : "IDA",
                                            "token" : "{token_response['token']}",
                                            "address" : {{
                                                "streetNumber" : "{street_num}",
                                                "streetName" : "{street_name}",
                                                "city" : "{city}",
                                                "state" : "{state}",
                                                "zipCode" : "{zipc}"
                                            }}
                                        }}"""
        check_feasibility_request_json = json.loads(check_feasibility_request)

        try:
            feasibility_response = requests.post(
                check_feasibility_url, json=check_feasibility_request_json).json()
        except requests.exceptions.ConnectionError:
            return {"success": False, "errorMessage": "VPN or Connection Error."}

        with open('temp.json', 'w') as f:
            json.dump(feasibility_response, f, indent=4)
        feasibility_response['address'] = address
        return feasibility_response
    return token_response


def next_available(env, technology, side):
    try:
        addresses = DATA[env]['addresses'][side][technology]
    except KeyError:
        return {"success": False, "errorMessage": "Please select Technology."}

    addresses = [x for x in addresses if '=' not in x]

    for address in addresses:
        feasibility = check_feasibility(env, address)
        print(feasibility)
        if feasibility['success']:
            av = feasibility.get("availability", 'None')
            if av == "AVAILABLE":
                return feasibility
        else:
            return feasibility
    return {"success": False, "errorMessage": "No Ports available."}


def format_address(address: str) -> Tuple[str, str, str, str, str] | None:
    try:
        address: List = address.split()
    except AttributeError:
        raise AddressException

    if len(address) == 6:
        street_num, street_name, city, state, zipc = address[0], " ".join(
            address[1:3]), address[3], address[4], address[5]
        return street_num, street_name, city, state, zipc
    else:
        raise AddressException


rate_codes = {
    "Optimum": {
        "Bring Codes": {
            "GPON": {
                "Gen7": "F.",
                "Gen8": "8H",
                "Gen9 6E": "=P",
            },
            "XGSPON": {
                "XGS": "(@",
                "XGS 6E": "UQ"
            }
        },

        "Residential": {
            "Install": {
                "Data Only or Data + Voice": "OY/DJ",
                "With Video": "3Q/4Q"
            },
            "Services": {
                "GPON": {
                    "100 Mbps": "F(",
                    "300 Mbps": "G!",
                    "500 Mbps": ")G",
                    "1000 Gbps": "Y*",
                },
                "XGSPON": {
                    "2000 Gbps": "(^",
                    "5000 Gbps": "(*",
                    "8000 Gbps": "#8"
                },
            },
            "Modem Fee": "N^",
            "Video": {
                "Bring Codes": {
                    "Altice Mini": "6Q",
                    "Stream SDMC": "+G and C4",
                    "Stream Sagemcom": ")# and )+"
                },
                "Services": {
                    "Basic TV": "YB",
                    "Core TV": "YC",
                    "Value TV": "YV",
                    "Select TV": "YS",
                    "Premier TV": "YP",
                },
                "Install": "65"
            },
            "Voice": {
                "Services": {
                    "Promo Voice Line": "$.",
                    "Full Rate Voice Line": "2S",
                    "Additional Line": "MT"
                },
                "Install": "1X"
            },
            "NEF": "G8",
            "Promo Tracker": "No Tracker Required."
        },

        "Commercial": {
            "Install": {
                "Data Only or Data + Voice": "HK",
            },
            "Services": {
                "GPON": {
                    "100 Mbps": "=)",
                    "300 Mbps": "=(",
                    "500 Mbps": "=*",
                    "1000 Gbps": "=^",
                },
                "XGSPON": {
                    "2000 Gbps": "(=",
                    "5000 Gbps": "(.",
                    "8000 Gbps": "=H"
                }
            },
            "Modem Fee": ".M",
            "Voice": {
                "Services": {
                    "1-3 Lines": "GC",
                    "4-24 Lines": "GW",
                },
                "Install": "Z1 and ZI"
            },
            "NEF": "No Secure Net.",
            "Promo Tracker": "No Tracker Required."
        }
    },
    "Suddenlink": {
        "Bring Codes": {
            "GPON": {
                "Gen7": "F.",
                "Gen8": "8H",
                "Gen9 6E": "=P",
            },
            "XGSPON": {
                "XGS": "(@",
                "XGS 6E": "UQ"
            }
        },

        "Residential": {
            "Install": {
                "Data Only or Data + Voice": "OY/DJ",
                "With Video": "3Q/4Q"
            },
            "Services": {
                "GPON": {
                    "100 Mbps": "F^",
                    "300 Mbps": "53",
                    "500 Mbps": "MG",
                    "1000 Gbps": "OS",
                },
                "XGSPON": {
                    "2000 Gbps": "TBD",
                    "5000 Gbps": "TBD",
                    "8000 Gbps": "TBD"
                },
            },
            "Modem Fee": "N^",
            "Video": {
                "Bring Codes": {
                    "Altice Mini": "6Q",
                    "Stream SDMC": "+G and C4",
                    "Stream Sagemcom": ")# and )+"
                },
                "Services": {
                    "Basic TV": "YB",
                    "Core TV": "YC",
                    "Value TV": "YV",
                    "Select TV": "YS",
                    "Premier TV": "YP",
                },
                "Install": "65"
            },
            "Voice": {
                "Services": {
                    "Promo Voice Line": "$.",
                    "Full Rate Voice Line": "2S",
                    "Additional Line": "MT"
                },
                "Install": "1X"
            },
            "NEF": "No NEF",
            "Promo Tracker": ".6 (if required)"
        },

        "Commercial": {
            "Install": {
                "Data Only or Data + Voice": "HK",
            },
            "Services": {
                "GPON": {
                    "100 Mbps": "=)",
                    "300 Mbps": "=(",
                    "500 Mbps": "=*",
                    "1000 Gbps": "=^",
                },
                "XGSPON": {
                    "2000 Gbps": "(=",
                    "5000 Gbps": "(.",
                    "8000 Gbps": "TBD"
                }
            },
            "Modem Fee": ".M",
            "Voice": {
                "Services": {
                    "Primary Line": "@1",
                    "Secondary Lines": "NE",
                },
                "Install": "Z1 and ZI"
            },
            "NEF": "No Secure Net.",
            "Promo Tracker": "No Tracker Required."
        },
    }
}
