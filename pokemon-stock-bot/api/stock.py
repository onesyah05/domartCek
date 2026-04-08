from curl_cffi import requests
import config
import json
from utils.headers import get_base_headers
from rich.console import Console

console = Console()

async def cek_stok(session: requests.AsyncSession, store_code: str, jwt_token: str, waf_token: str, lat: float = None, lon: float = None) -> list:
    """Mengecek stok produk dengan memasukkan ke keranjang dan melihat response stoknya"""
    
    url = f"{config.BASE_URL_CORE}/post/cart-xpress/api/webapp/cart/add-to-cart"
    
    # Gunakan koordinat toko jika tersedia, jika tidak fallback ke default config
    current_lat = lat if lat is not None else config.DEFAULT_LATITUDE
    current_lon = lon if lon is not None else config.DEFAULT_LONGITUDE
    
    products_payload = [{"plu": plu, "qty": 1} for plu in config.POKEMON_PLUS]
    
    payload = {
        "storeCode": store_code,
        "latitude": current_lat,
        "longitude": current_lon,
        "mode": "PICKUP",
        "districtId": 140200469, # Hardcoded default for Jakarta
        "products": products_payload
    }
    
    headers = get_base_headers(jwt_token, waf_token)
    headers["apps"] = json.dumps({
        "app_version": config.DEFAULT_APP_VERSION,
        "device_class": "browser|browser",
        "device_family": "none",
        "device_id": config.DEVICE_ID,
        "os_name": "Windows",
        "os_version": "10"
    })
    
    resp = await session.post(url, json=payload, headers=headers, impersonate="chrome")
    resp.raise_for_status()
    data = resp.json().get("data", {})
    
    hasil = []
    
    # Produk yang memiliki stok akan masuk ke 'products'
    for prod in data.get("products", []):
        stok = prod.get("stock", 0)
        is_available = prod.get("isAvailable", False)
        
        # Stok benar-benar ada jika stock > 0 DAN isAvailable = True
        status_ready = (stok > 0) and is_available
        
        hasil.append({
            "plu": prod.get("plu"),
            "nama": prod.get("productName"),
            "stok": stok,
            "status": "Ready" if status_ready else "Habis"
        })
        
    # Produk yang tidak ada stoknya akan masuk ke 'dataTracker.productStockout'
    tracker = data.get("dataTracker", {})
    for stockout in tracker.get("productStockout", []):
        plu_so = stockout.get("plu")
        nama_so = stockout.get("productName")
        
        # Cari nama asli dari config jika productName di stockout null
        if not nama_so:
            nama_so = f"Produk PLU {plu_so}"
            
        hasil.append({
            "plu": plu_so,
            "nama": nama_so,
            "stok": 0,
            "status": "Habis"
        })
        
    return hasil
