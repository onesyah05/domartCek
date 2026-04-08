from curl_cffi import requests
import config
from utils.headers import get_base_headers

async def set_mode_pickup(session: requests.AsyncSession, store_code: str, jwt_token: str, waf_token: str) -> str:
    """
    Update setting cart dengan metode pengambilan di toko yang ditentukan
    Kembalikan districtId dari response.
    """
    url = f"{config.BASE_URL_ORDER}/post/cartgeneral/api/webapp/cart/set-mode"
    
    payload = {
        "mode": "XPRESS_PICKUP",
        "pickupStoreCode": store_code,
        "selectedStore": None
    }
    
    headers = get_base_headers(jwt_token, waf_token)
    
    resp = await session.post(url, json=payload, headers=headers, impersonate="chrome")
    resp.raise_for_status()
    
    data = resp.json()
    # DistrictId mungkin tidak langsung tersedia di sini, 
    # di referensi file request add-to-cart memakai districtId: 140200469 (hardcode)
    # Nanti kita kembalikan store yang berhasil diset.
    return data.get("status") == "00"

async def clear_cart(session: requests.AsyncSession, jwt_token: str, waf_token: str):
    """Membersihkan keranjang setelah di cek (opsional, karena API ini bisa beda endpoint)
    Kita bisa gunakan endpoint delete cart item jika diperlukan, tapi ini sbg placeholder.
    """
    pass
