from datetime import datetime
import requests
import json
from typing import Dict, Tuple, List
import dotenv
import os

dotenv.load_dotenv()

user = os.getenv('uname')
password = os.getenv('pw')

# DATA = {
#     "QA INT": {
#         "addresses": {
#             "OPT": {
#                 "GPON": [                    
#                     "30 ASH LN HICKSVILLE NY 11801",
#                     "34 ASH LN HICKSVILLE NY 11801",
#                     "36 ASH LN HICKSVILLE NY 11801",
#                     "38 ASH LN HICKSVILLE NY 11801",
#                     "40 ASH LN HICKSVILLE NY 11801",
#                     "48 ASH LN HICKSVILLE NY 11801",
#                     "315 ACRE LN HICKSVILLE NY 11801",
#                     "336 ACRE LN HICKSVILLE NY 11801",
#                     "27 ATLAS LN HICKSVILLE NY 11801",
#                     "29 ATLAS LN HICKSVILLE NY 11801",
#                     "33 ATLAS LN HICKSVILLE NY 11801",
#                     "35 ATLAS LN HICKSVILLE NY 11801",
#                     "38 ATLAS LN HICKSVILLE NY 11801",
#                     "39 ATLAS LN HICKSVILLE NY 11801",
#                     "41 ATLAS LN HICKSVILLE NY 11801",
#                     "15 BEACON LN HICKSVILLE NY 11801"
#                 ],
#                 "XGSPON": [                    
#                     "61 SLEEPY LN HICKSVILLE NY 11801",
#                     "65 SLEEPY LN HICKSVILLE NY 11801",
#                     "53 SLEEPY LN HICKSVILLE NY 11801",
#                     "67 SLEEPY LN HICKSVILLE NY 11801"
#                 ],
#                 "CHT": [                    
#                     f"{'C01_EAST':=^30}",
#                     "17 DANTE AVE HICKSVILLE NY 11801",
#                     "11 DANTE AVE HICKSVILLE NY 11801",
#                     "19 DANTE AVE HICKSVILLE NY 11801",
#                     "16 DANTE AVE HICKSVILLE NY 11801",
                    
#                     f"{'C02_EAST':=^30}",
#                     "51 DANTE AVE HICKSVILLE NY 11801",
#                     "49 DANTE AVE HICKSVILLE NY 11801",
#                     "47 DANTE AVE HICKSVILLE NY 11801",
#                     "31 DANTE AVE HICKSVILLE NY 11801",
                    
#                     f"{'C03_EAST':=^30}",
#                     "87 DANTE AVE HICKSVILLE NY 11801",
#                     "85 DANTE AVE HICKSVILLE NY 11801",
#                     "89 DANTE AVE HICKSVILLE NY 11801",
#                     "52 DANTE AVE HICKSVILLE NY 11801",
#                 ],
#                 "WITH DELAY": [                    
#                     "3 WILLOW AVE HICKSVILLE NY 11801",
#                     "6 BISHOP LN HICKSVILLE NY 11801",
#                     "11 ATLAS LN HICKSVILLE NY 11801",
#                     "14 ASH LN HICKSVILLE NY 11801",
#                     "326 ACRE LN HICKSVILLE NY 11801"
#                 ],
#             },
#             "SDL": {
#                 "XGSPON": [                    
#                     "3103 BAYLOR ST LUBBOCK TX 79415",
#                     "3105 BAYLOR ST LUBBOCK TX 79415",
#                     "3107 BAYLOR ST LUBBOCK TX 79415",
#                     "3109 BAYLOR ST LUBBOCK TX 79415"
#                 ],
#                 "RFOG": [                    
#                     "3309 AUBURN ST LUBBOCK TX 79415",
#                     "3311 AUBURN ST LUBBOCK TX 79415",
#                     "3313 AUBURN ST LUBBOCK TX 79415",
#                 ],
#                 "CHT": [                    
#                     f"{'C01_WEST':=^30}",
#                     "3313 DUKE ST LUBBOCK TX 79415",
#                     "3311 DUKE ST LUBBOCK TX 79415",
#                     "3309 DUKE ST LUBBOCK TX 79415",
#                     "3307 DUKE ST LUBBOCK TX 79415",

#                     f"{'C02_WEST':=^30}",
#                     "3221 DUKE ST LUBBOCK TX 79415",
#                     "3219 DUKE ST LUBBOCK TX 79415",
#                     "3217 DUKE ST LUBBOCK TX 79415",
#                     "3301 DUKE ST LUBBOCK TX 79415",

#                     f"{'C0_WEST':=^30}",
#                     "3207 DUKE ST LUBBOCK TX 79415",
#                     "3205 DUKE ST LUBBOCK TX 79415",
#                     "3209 DUKE ST LUBBOCK TX 79415",
#                     "3203 DUKE ST LUBBOCK TX 79415",
#                 ]
#             }
#         },
#         "get_token": "http://microservices-int.lab.cscqa.com/GateKeeper_V1/api/getToken",
#         "check_feasibility": "http://microservices-int.lab.cscqa.com/checkFTTHFeasibility_V2/api/m1"
#     },

#     "QA 2": {
#         "addresses": {
#             "OPT": {
#                 "GPON": [
#                     "186 JACKSON AVE MINEOLA NY 11501",
#                     "179 GRANT AVE MINEOLA NY 11501",
#                     "177 JEFFERSON AVE MINEOLA NY 11501",
#                     "231 WASHINGTON AVE MINEOLA NY 11501",
#                 ],
#                 "XGSPON": [
#                     f"{'PDO1':=^30}",
#                     "305 WALTER AVE MINEOLA NY 11501",
#                     "306 WALTER AVE MINEOLA NY 11501",
#                     "309 WALTER AVE MINEOLA NY 11501",
#                     f"{'PDO2':=^30}",
#                     "299 WELLINGTON RD MINEOLA NY 11501",
#                     "305 WELLINGTON RD MINEOLA NY 11501",
#                     "315 WELLINGTON RD MINEOLA NY 11501",
#                     f"{'PDO3':=^30}",
#                     "341 BAUER PL MINEOLA NY 11501",
#                     "343 BAUER PL MINEOLA NY 11501",
#                     "345 BAUER PL MINEOLA NY 11501",
#                     f"{'PDO4':=^30}",
#                     "321 COOLIDGE AVE MINEOLA NY 11501",
#                     "325 COOLIDGE AVE MINEOLA NY 11501",
#                     "326 COOLIDGE AVE MINEOLA NY 11501",
#                 ],
#                 "CISCO BNG": [
#                     "130 WALKER RD MINEOLA NY 11501",
#                     "134 WALKER RD MINEOLA NY 11501",
#                     "135 WALKER RD MINEOLA NY 11501",
#                     "143 WALKER RD MINEOLA NY 11501",
#                     "146 WALKER RD MINEOLA NY 11501"
#                 ]
#             },
#             "SDL": {
#                 "XGSPON": [
#                     f"{'PDO1':=^30}",
#                     "531 ROANE ST CHARLESTON WV 25302",
#                     "525 ROANE ST CHARLESTON WV 25302",
#                     "523 ROANE ST CHARLESTON WV 25302",
                    
#                     f"{'PDO2':=^30}",
#                     "521 WYOMING ST CHARLESTON WV 25302",
#                     "522 WYOMING ST CHARLESTON WV 25302",
#                     "523 WYOMING ST CHARLESTON WV 25302",
#                     "524 WYOMING ST CHARLESTON WV 25302",
                    
#                     f"{'PDO3':=^30}",
#                     "519 WYOMING ST CHARLESTON WV 25302",
#                     "518 WYOMING ST CHARLESTON WV 25302",
#                     "517 WYOMING ST CHARLESTON WV 25302",
                    
#                     f"{'PDO4':=^30}",
#                     "536 WYOMING ST CHARLESTON WV 25302",
#                     "537 WYOMING ST CHARLESTON WV 25302",
#                     "534 WYOMING ST CHARLESTON WV 25302",
                    
#                     f"{'PDO5':=^30}",
#                     "624 RANDOLPH ST CHARLESTON WV 25302",
#                     "625 RANDOLPH ST CHARLESTON WV 25302",
#                     "623 RANDOLPH ST CHARLESTON WV 25302",
#                 ],
#                 "RFOG": [
#                     "733 CENTRAL AVE CHARLESTON WV 25302",
#                     "735 CENTRAL AVE CHARLESTON WV 25302",
#                     "736 CENTRAL AVE CHARLESTON WV 25302",
#                     "737 CENTRAL AVE CHARLESTON WV 25302",
#                     "738 CENTRAL AVE CHARLESTON WV 25302",
#                     "739 CENTRAL AVE CHARLESTON WV 25302",
#                     "306 BEUHRING AVE CHARLESTON WV 25302",
#                     "308 BEUHRING AVE CHARLESTON WV 25302",
#                     "305 BEUHRING AVE CHARLESTON WV 25302",
#                     "303 BEUHRING AVE CHARLESTON WV 25302",
#                 ],
#             }
#         },
#         "get_token": "http://microservices-q2.lab.cscqa.com/GateKeeper_V1/api/getToken",
#         "check_feasibility": "http://microservices-q2.lab.cscqa.com/checkFTTHFeasibility_V2/api/m1"
#     }
# }


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
