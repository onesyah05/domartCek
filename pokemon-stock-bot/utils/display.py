from rich.console import Console
from rich.panel import Panel
import questionary

console = Console()

def tampilkan_banner():
    banner_text = """[bold yellow]
╔══════════════════════════════════════════════════╗
║  🎴 Pokémon Card Stock Finder — Klik Indomaret   ║
╚══════════════════════════════════════════════════╝[/bold yellow]"""
    console.print(banner_text)

async def select_menu():
    return await questionary.select(
        "Pilih Mode Pencarian:",
        choices=[
            "Cari Berdasarkan Nama (Manual)",
            "Auto-Scan Wilayah (Pilih Provinsi -> Kota -> Semua Kecamatan)",
            "Keluar"
        ]
    ).ask_async()

async def select_province(provinces_data):
    choices = [p["label"] for p in provinces_data]
    return await questionary.select(
        "Pilih Provinsi:",
        choices=choices
    ).ask_async()

async def select_city(cities_data):
    choices = [c["label"] for c in cities_data]
    return await questionary.select(
        "Pilih Kota:",
        choices=choices
    ).ask_async()

def print_toko_ditemukan(keyword, jumlah):
    console.print(f"\n[cyan]🔍 Ditemukan {jumlah} toko di area \"{keyword}\". Mengecek stok...[/cyan]\n")

def print_tidak_ada_toko():
    console.print("[red]❌ Tidak ada toko ditemukan di area tersebut.[/red]")

def print_stok_toko(kota, nama_toko, alamat_toko, produk_list):
    has_stock = False
    
    # Format the store info string
    store_info = f"{nama_toko} [dim]({alamat_toko})[/dim]"
    
    for prod in produk_list:
        if prod["stok"] > 0:
            console.print(f"> [bold]{kota}[/bold] — {store_info} [green][{prod['nama']} ({prod['stok']})][/green]  ✅ Ready")
            has_stock = True
            
    if not has_stock:
        console.print(f"> [bold]{kota}[/bold] — {store_info} [dim]Tidak ada stok kartu Pokémon[/dim]")


def print_info_simpan(filepath):
    console.print(f"\n[bold green]💾 Hasil disimpan ke {filepath}[/bold green]\n")

def print_error(msg):
    console.print(f"[bold red]❌ Error: {msg}[/bold red]")
