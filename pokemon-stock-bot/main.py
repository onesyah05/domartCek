import asyncio
import sys

# To fix Windows event loop RuntimeWarning
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import os
from curl_cffi import requests
import questionary

from api.store import temukan_toko
from api.cart import set_mode_pickup
from api.stock import cek_stok
from api.coverage import get_provinces, get_cities, get_districts
from utils.display import (
    console, tampilkan_banner, print_toko_ditemukan, 
    print_tidak_ada_toko, print_stok_toko, print_info_simpan, print_error,
    select_menu, select_province, select_city
)
from utils.output import simpan_hasil

async def cek_toko_async(session, toko, keyword, jwt_token, waf_token):
    store_code = toko.get("storeCode")
    store_name = toko.get("storeName")
    store_address = toko.get("address", "")
    lat = toko.get("latitude")
    lon = toko.get("longitude")
    
    try:
        # Set mode pickup ke toko ini
        if not await set_mode_pickup(session, store_code, jwt_token, waf_token):
            return store_name, store_address, []
            
        # Cek stok dengan koordinat toko asli
        hasil_stok = await cek_stok(session, store_code, jwt_token, waf_token, lat=lat, lon=lon)
        return store_name, store_address, hasil_stok
        
    except requests.errors.RequestsError as e:
        if e.response and e.response.status_code in [401, 403]:
            raise e
        return store_name, store_address, []
    except Exception as e:
        return store_name, store_address, []

async def minta_input_token():
    console.print("\n[bold yellow]--- UPDATE TOKEN MANUAL ---[/bold yellow]")
    console.print("Silakan ambil token dari browser (DevTools -> Network -> cari request apa saja).")
    jwt = await questionary.text("Masukkan JWT Token (berawalan 'ey...'):").ask_async()
    waf = await questionary.text("Masukkan AWS WAF Token:").ask_async()
    return (jwt or "").strip(), (waf or "").strip()

async def proses_pencarian_stok(session, keyword, jwt_token, waf_token):
    """Fungsi pembantu untuk menjalankan proses pencarian stok per keyword (kecamatan)"""
    try:
        toko_list = await temukan_toko(session, keyword, jwt_token, waf_token)
        
        if not toko_list:
            print_tidak_ada_toko()
            return

        print_toko_ditemukan(keyword, len(toko_list))
        semua_hasil = []
        
        # Proses SEQUENTIAL (satu per satu) karena satu akun = satu keranjang.
        # Kalau parallel, set-mode akan saling tumpuk dan stok jadi kacau.
        # Menambahkan delay 2 detik antar toko agar tidak kena rate limit Cloudflare (Error 1015).
        for i_toko, toko in enumerate(toko_list):
            try:
                res = await cek_toko_async(session, toko, keyword, jwt_token, waf_token)
                if isinstance(res, Exception):
                    raise res
                
                store_name, store_address, stok_list = res
                semua_hasil.append((store_name, store_address, stok_list))
                print_stok_toko(keyword, store_name, store_address, stok_list)
                
            except requests.errors.RequestsError as e:
                if e.response and e.response.status_code == 429:
                    print_error(f"IP Terkena Rate Limit (429) oleh Cloudflare! Menunggu 10 detik...")
                    await asyncio.sleep(10)
                    continue
                elif e.response and e.response.status_code in [401, 403]:
                    raise e
            except Exception as e:
                # Jika error karena stock kosong (bukan network/auth), tetap lanjut
                if "401" in str(e) or "403" in str(e):
                    raise e
                continue
            
            # Delay antar toko (kecuali toko terakhir)
            if i_toko < len(toko_list) - 1:
                await asyncio.sleep(2)
                
        if semua_hasil:
            filepath = simpan_hasil(keyword, semua_hasil)
            print_info_simpan(filepath)

    except Exception as e:
        raise e

async def main():
    tampilkan_banner()
    
    jwt_token, waf_token = await minta_input_token()
    
    if not jwt_token or not waf_token:
        print_error("Gagal menjalankan bot, token tidak boleh kosong.")
        sys.exit(1)
        
    async with requests.AsyncSession(timeout=30.0) as session:
        while True:
            pilihan = await select_menu()
            
            if pilihan == "Keluar":
                console.print("[yellow]Bot selesai. Sampai jumpa![/yellow]")
                break
                
            elif pilihan == "Cari Berdasarkan Nama (Manual)":
                console.print("\n[bold cyan]Masukkan kota/kecamatan:[/bold cyan]")
                keyword = input("> ").strip()
                if not keyword: continue
                
                try:
                    await proses_pencarian_stok(session, keyword, jwt_token, waf_token)
                except requests.errors.RequestsError as e:
                    status_code = e.response.status_code if e.response else None
                    if status_code in [401, 403]:
                        print_error("Token expired atau diblokir WAF. Silakan update token.")
                        jwt_token, waf_token = await minta_input_token()
                except Exception as e:
                    print_error(str(e))
                
            elif pilihan == "Auto-Scan Wilayah (Pilih Provinsi -> Kota -> Semua Kecamatan)":
                try:
                    # 1. Pilih Provinsi
                    provinces = await get_provinces(session, jwt_token, waf_token)
                    if not provinces:
                        print_error("Gagal mengambil daftar provinsi.")
                        continue
                    
                    prov_label = await select_province(provinces)
                    
                    # 2. Pilih Kota
                    cities = await get_cities(session, prov_label, jwt_token, waf_token)
                    if not cities:
                        print_error(f"Gagal mengambil daftar kota di {prov_label}.")
                        continue
                        
                    city_label = await select_city(cities)
                    
                    # 3. Ambil Semua Kecamatan
                    districts = await get_districts(session, prov_label, city_label, jwt_token, waf_token)
                    if not districts:
                        print_error(f"Gagal mengambil daftar kecamatan di {city_label}.")
                        continue
                    
                    console.print(f"\n[bold green]🚀 Memulai Auto-Scan untuk {len(districts)} kecamatan di {city_label}...[/bold green]")
                    console.print("[dim]Delay 5 detik per kecamatan untuk keamanan.[/dim]\n")
                    
                    for i, dist in enumerate(districts):
                        dist_label = dist["label"]
                        console.print(f"[bold yellow][{i+1}/{len(districts)}] Memproses Kecamatan: {dist_label}[/bold yellow]")
                        
                        retry_count = 0
                        while retry_count < 2:
                            try:
                                await proses_pencarian_stok(session, dist_label, jwt_token, waf_token)
                                break # Sukses, lanjut ke kecamatan berikutnya
                            except Exception as e:
                                if "401" in str(e) or "403" in str(e):
                                    print_error(f"Gagal scan {dist_label}: Token Expired/Invalid ({str(e)})")
                                    jwt_token, waf_token = await minta_input_token()
                                    retry_count += 1
                                else:
                                    print_error(f"Gagal scan {dist_label}: {str(e)}")
                                    break # Gagal karena alasan lain, lanjut
                        
                        if i < len(districts) - 1:
                            await asyncio.sleep(5) # Delay 5 detik sesuai permintaan
                            
                    console.print(f"\n[bold green]✅ Selesai scanning kota {city_label}![/bold green]")

                except Exception as e:
                    print_error(f"Terjadi kesalahan saat auto-scan: {str(e)}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Membatalkan dari keyboard. Sayonara![/yellow]")
