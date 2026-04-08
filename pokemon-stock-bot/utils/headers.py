import json

def get_base_headers(jwt_token: str, waf_token: str):
    """Membangun base headers untuk request API Klik Indomaret"""
    import config
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "page": "/search",
        "priority": "u=1, i",
        "User-Agent": config.DEFAULT_APP_VERSION,
        "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://www.klikindomaret.com/"
    }
    
    if jwt_token:
        if not jwt_token.startswith("Bearer "):
            jwt_token = f"Bearer {jwt_token}"
        headers["authorization"] = jwt_token
        
    if waf_token:
        headers["x-aws-waf-token"] = waf_token
        
    return headers

def get_app_headers():
    import config
    return {
        "apps": json.dumps({
            "app_version": config.DEFAULT_APP_VERSION,
            "device_class": "browser|browser",
            "device_family": "none",
            "device_id": config.DEVICE_ID,
            "os_name": "Windows",
            "os_version": "10"
        })
    }
