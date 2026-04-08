import datetime
import os

OUTPUT_FILE = "hasil.txt"

def simpan_hasil(keyword, semua_hasil):
    """
    Menyimpan hasil ke file hasil.txt
    semua_hasil: list of tuples (nama_toko, list_produk)
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M WIB")
    
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write("\n=== HASIL CEK STOK POKEMON ===\n")
        f.write(f"Lokasi  : {keyword}\n")
        f.write(f"Tanggal : {now}\n")
        f.write("-" * 30 + "\n")
        
        for toko_nama, toko_alamat, produk_list in semua_hasil:
            has_stock = False
            store_info_text = f"{toko_nama} ({toko_alamat})"
            for prod in produk_list:
                if prod["stok"] > 0:
                    f.write(f"> {keyword} - {store_info_text} [{prod['nama']} ({prod['stok']})] Ready\n")
                    has_stock = True
                else:
                    # Opsional log stockout
                    # f.write(f"> {keyword} - {store_info_text} [{prod['nama']} (0)] Habis\n")
                    pass
            
            if not has_stock:
                f.write(f"> {keyword} - {store_info_text} [No Stock]\n")
                
        f.write("=" * 30 + "\n")
        
    return os.path.abspath(OUTPUT_FILE)
