from curl_cffi import requests
from utils.headers import get_base_headers
import config

async def get_provinces(session: requests.AsyncSession, jwt_token: str, waf_token: str) -> list:
    """Mengambil daftar provinsi dari Klik Indomaret"""
    url = f"{config.BASE_URL_COVERAGE}/provinsi"
    headers = get_base_headers(jwt_token, waf_token)
    
    resp = await session.get(url, headers=headers, impersonate="chrome")
    resp.raise_for_status()
    
    data = resp.json()
    if data.get("status") == "00":
        return data.get("data", [])
    return []

async def get_cities(session: requests.AsyncSession, province: str, jwt_token: str, waf_token: str) -> list:
    """Mengambil daftar kota berdasarkan provinsi"""
    url = f"{config.BASE_URL_COVERAGE}/kota"
    params = {"provinsi": province}
    headers = get_base_headers(jwt_token, waf_token)
    
    resp = await session.get(url, params=params, headers=headers, impersonate="chrome")
    resp.raise_for_status()
    
    data = resp.json()
    if data.get("status") == "00":
        return data.get("data", [])
    return []

async def get_districts(session: requests.AsyncSession, province: str, city: str, jwt_token: str, waf_token: str) -> list:
    """Mengambil daftar kecamatan berdasarkan provinsi dan kota"""
    url = f"{config.BASE_URL_COVERAGE}/kecamatan"
    params = {"provinsi": province, "kota": city}
    headers = get_base_headers(jwt_token, waf_token)
    
    resp = await session.get(url, params=params, headers=headers, impersonate="chrome")
    resp.raise_for_status()
    
    data = resp.json()
    if data.get("status") == "00":
        return data.get("data", [])
    return []
