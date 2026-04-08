from curl_cffi import requests
from utils.headers import get_base_headers
import config

async def temukan_toko(session: requests.AsyncSession, keyword: str, jwt_token: str, waf_token: str) -> list:
    """Mencari toko-toko Indomaret terdekat berdasarkan keyword"""
    
    url = f"{config.BASE_URL_ORDER}/get/catalog-xpress/api/webapp/stores/nearest"
    params = {
        "latitude": config.DEFAULT_LATITUDE,
        "longitude": config.DEFAULT_LONGITUDE,
        "page": 0,
        "keyword": keyword
    }
    
    headers = get_base_headers(jwt_token, waf_token)
    
    # Adding application specific headers
    import json
    headers["apps"] = json.dumps({
        "app_version": config.DEFAULT_APP_VERSION,
        "device_class": "browser|browser",
        "device_family": "none",
        "device_id": config.DEVICE_ID,
        "os_name": "Windows",
        "os_version": "10"
    })
    
    resp = await session.get(url, params=params, headers=headers, impersonate="chrome")
    
    if resp.status_code == 401:
        raise Exception("Token (JWT) expired atau tidak valid. Silakan jalankan fitur login ulang.")
    elif resp.status_code == 403:
        raise Exception("Akses diblokir oleh WAF. AWS WAF Token mungkin expired.")
        
    resp.raise_for_status()
    
    data = resp.json()
    if data.get("status") == "00":
        return data.get("data", {}).get("content", [])
        
    return []
