from decimal import Decimal
from koneksiDB import connect
from psycopg2.extras import RealDictCursor
from tabulate import tabulate
import os
import pyfiglet
import datetime as dt
import re

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def format_rupiah(number):
    return f"Rp {int(number):,}".replace(",", ".")

def banner():
    b = 130
    blue = "\033[34m"
    cyan = "\033[96m"
    endc = "\033[0m"
    print(blue + "=" * b + endc)
    print(cyan)
    print(" ██████╗ █████╗ ███╗   ██╗████████╗██╗██╗  ██╗███╗   ██╗██╗   ██╗ █████╗     ███╗   ███╗ █████╗ ██╗  ██╗ █████╗ ██████╗".center(b))
    print("██╔════╝██╔══██╗████╗  ██║╚══██╔══╝██║██║ ██╔╝████╗  ██║╚██╗ ██╔╝██╔══██╗    ████╗ ████║██╔══██╗██║  ██║██╔══██╗██╔══██╗".center(b))
    print("██║     ███████║██╔██╗ ██║   ██║   ██║█████╔╝ ██╔██╗ ██║ ╚████╔╝ ███████║    ██╔████╔██║███████║███████║███████║██████╔╝".center(b))
    print("██║     ██╔══██║██║╚██╗██║   ██║   ██║██╔═██╗ ██║╚██╗██║  ╚██╔╝  ██╔══██║    ██║╚██╔╝██║██╔══██║██╔══██║██╔══██║██╔══██╗".center(b))
    print("╚██████╗██║  ██║██║ ╚████║   ██║   ██║██║  ██╗██║ ╚████║   ██║   ██║  ██║    ██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██║██║  ██║".center(b))
    print(" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝".center(b))
    print(endc)
    print(blue + "=" * b + endc)                                                                                        


def hiasan(apa):
    print("\033[96m",pyfiglet.figlet_format(apa, font='small'),"\033[0m")

def register():
    koneksi = connect()
    syntax = koneksi.cursor(cursor_factory=RealDictCursor)
    while True:
        nama = input("Masukkan nama : ")
        if nama == "":
            print("Nama tidak boleh kosong")
        else:
            break
    while True:
        no_hp = input("Masukkan nomor hp : ")
        if no_hp == "":
            print("Nomor hp tidak boleh kosong")
        elif not no_hp.isdigit():
            print("Nomor hp hanya boleh berisi angka")
        elif not no_hp.startswith("62"):
            print("Nomor hp harus dimulai dengan '62'")
        elif not (10 <= len(no_hp) <= 13):  
            print("Nomor hp harus terdiri dari 10 hingga 13 digit")
        else:
            break
    query = "SELECT * FROM customer"
    syntax.execute(query)
    data_customer = syntax.fetchall()
    username_sudah_ada = [user['username'] for user in data_customer]

    while True:
        username = input("Masukkan username : ").strip()

        if not username:
            print("Username tidak boleh kosong.")
        elif ' ' in username:
            print("Username tidak boleh mengandung spasi.")
        elif not username.isalnum():
            print("Username hanya boleh berisi huruf dan angka.")
        elif username in username_sudah_ada:
            print("Username sudah terdaftar. Silakan pilih username lain.")
        else:
            break
    while True:
        password = input("Masukkan password : ")
        if password == "":
            print("Password tidak boleh kosong")
        elif len(password) < 6:
            print("Password harus memiliki panjang minimal 6 karakter")
        elif not re.search(r'(?=.*[A-Za-z])(?=.*\d)', password):
            print("Password harus mengandung kombinasi huruf dan angka")
        else:
            break
    while True:
        domain_diizinkan = ["gmail.com","mail.unej.ac.id"]
        email_sudah_ada = [user['email_address'] for user in data_customer]
        email = input("Masukkan alamat email : ")
        if email == "":
            print("Alamat email tidak boleh kosong")
        elif "@" not in email:
            print("Alamat email harus mengandung '@'.")
        elif email in email_sudah_ada:
            print("Alamat email sudah terdaftar. Silahkan gunakan alamat email lain.")
        else:
            domain = email.split('@')[1]
            if domain not in domain_diizinkan:
                print(f"Alamat email hanya boleh menggunakan domain : {', '.join(domain_diizinkan)}")
            else:
                break
    while True:
        try:
            query = "INSERT INTO customer (nama, no_hp, username, password, email_address) VALUES (%s,%s,%s,%s,%s)"
            syntax.execute(query, (nama,no_hp,username,password,email))
            koneksi.commit()
            print("Data berhasil disimpan")
            input("Tekan enter untuk melanjutkan")
            clear_terminal()
            break
        except Exception as e:
            print("Data gagal disimpan")
            print(e)
            print("Silahkan coba lagi")
            pilihan = input("Apakah anda ingin mendaftar lagi? (y/n) : ")
            if pilihan.lower() == 'y':
                continue
            else:
                break
        finally:
            syntax.close()
            koneksi.close()

def login():
    koneksi = connect()
    syntax = koneksi.cursor(cursor_factory=RealDictCursor)
    admin_query = "SELECT * FROM akun_admin WHERE username=%s"
    customer_query = "SELECT * FROM customer WHERE username=%s"
    while True:
        username = input("Masukkan username : ")
        syntax.execute(admin_query, (username,))
        data_admin = syntax.fetchone()
        if not data_admin:
            syntax.execute(customer_query, (username,))
            data_customer = syntax.fetchone()
        else:
            data_customer = None

        if not data_admin and not data_customer:
            print("Username tidak terdaftar, silahkan coba lagi atau daftarkan diri anda")
            tanya = input("Apakah anda ingin mendaftar? (y/n) : ")
            if tanya.lower() == 'y':
                register()
                clear_terminal()
            continue
        else:
            break
    while True:
        password = input("Masukkan password : ")
        if data_admin:
            try:
                query = "SELECT * FROM akun_admin WHERE username=%s AND password=%s"
                syntax.execute(query, (username, password))
                data = syntax.fetchone()
                if data:
                    hiasan("Login Berhasil")
                    hiasan(f"Selamat datang Admin {data['nama']}")
                    input("Tekan enter untuk melanjutkan")
                    clear_terminal()
                    Menu('admin', data)
                    break
                else:
                    print("Password salah")
            except Exception as e:
                print("Login gagal")
                print(e)
        elif data_customer:
            try:
                query = "SELECT * FROM customer WHERE username=%s AND password=%s"
                syntax.execute(query, (username, password))
                data = syntax.fetchone()
                if data:
                    hiasan("Login Berhasil")
                    hiasan(f"Selamat datang {data['nama']}")
                    input("Tekan enter untuk melanjutkan")
                    clear_terminal()
                    Menu('customer', data)
                    break
                else:
                    print("Password salah")
            except Exception as e:
                print("Login gagal")
                print(e)
    syntax.close()
    koneksi.close()

def kuasaAdmin(pilihan):
    koneksi = connect()
    syntax = koneksi.cursor(cursor_factory=RealDictCursor)
    if pilihan == '1':
        try:
            nama = input("Masukkan nama produk : ")
            while True:
                try:
                    harga = int(input("Masukkan harga produk : "))
                    stok = int(input("Masukkan stok produk : "))
                    break
                except ValueError:
                    print("Harga atau stok harus angka")
            foto = 0
            while True:
                kategori = input("Masukkan kategori produk (seserahan/dekorasi/souvenir/mahar): ").lower().strip()
                if kategori not in ['seserahan', 'dekorasi', 'souvenir', 'mahar']:
                    print("Kategori tidak valid, silahkan coba lagi")
                    continue
                else:
                    break
            syntax.execute("SELECT id_kategori FROM kategori WHERE kategori = %s", (kategori,))
            data_kategori = syntax.fetchone()
            if not data_kategori:
                print("Kategori tidak ditemukan")
                return
            id_kategori = data_kategori[0]
            query = "INSERT INTO produk (nama, harga, stok, foto, id_kategori) VALUES (%s,%s,%s,%s,%s)"
            syntax.execute(query, (nama, harga, stok, foto, id_kategori))
            koneksi.commit()
            print("Data berhasil disimpan")
            input("Tekan enter untuk melanjutkan")
            clear_terminal()
        except Exception as e:
            print("Data gagal disimpan")
            print(e)
            print("Silahkan coba lagi")
        finally:
            syntax.close()
            koneksi.close()

    elif pilihan == '2':
        try:
            while True:
                produk = input("Masukkan id/nama produk yang ingin diubah : ")
                try:
                    int(produk)
                    query = """SELECT id_produk, nama AS "Nama", harga AS "Harga", stok AS "Stok", disewakan FROM produk WHERE id_produk = %s"""
                    syntax.execute(query, (produk,))
                    data = syntax.fetchone()
                    query_semua = "SELECT * FROM produk WHERE id_produk = %s"
                    syntax.execute(query_semua, (produk,))
                    data_semua = syntax.fetchone()
                except ValueError:
                    query = """SELECT id_produk, nama AS "Nama", harga AS "Harga", stok AS "Stok", disewakan FROM produk WHERE nama ILIKE %s"""
                    syntax.execute(query, (f"%{produk}%",))
                    data = syntax.fetchone()
                    query_semua = "SELECT * FROM produk WHERE nama ILIKE %s"
                    syntax.execute(query_semua, (f"%{produk}%",))
                    data_semua = syntax.fetchone()
                try:
                    if not data:
                        print("Produk tidak ditemukan")
                        print("Silahkan masukkan ulang")
                    else:
                        print("Berikut adalah data produk yang ingin diubah :")
                        break
                except Exception as e:
                    print("Gagal menampilkan data produk")
                    print(e)
            while True:
                print(tabulate([data], headers="keys", tablefmt="fancy_grid"))
                print("""
                            ╔══════════════════════════════════╗
                            ║     Pilih yang ingin diubah      ║
                            ║┌────────────────────────────────┐║
                            ║│        1. Nama Produk          │║
                            ║│        2. Harga                │║ 
                            ║│        3. Stok                 │║
                            ║│        4. Kategori             │║
                            ║│        5. Kembali              │║
                            ║└────────────────────────────────┘║
                            ╚══════════════════════════════════╝""")
                pilihan = input("Pilih program : ")
                if pilihan == '1':
                    nama = input("Masukkan nama produk baru : ")
                    print("\nPreview Perubahan")
                    print(f"Nama Produk Lama : {data['Nama']}")
                    print(f"Nama Produk Baru : {nama}")
                    konfirmasi = input("\nSimpan Perubahan? (y/n) : ").lower()
                    if konfirmasi == 'y':
                        try:
                            query = "UPDATE produk SET nama = %s WHERE id_produk = %s"
                            syntax.execute(query, (nama, data["id_produk"]))
                            koneksi.commit()
                            data['Nama'] = nama
                            print("Data berhasil diubah")
                            input("Tekan enter untuk melanjutkan")
                            clear_terminal()
                        except Exception as e:
                            print("Data gagal diubah")
                            print(e)
                            print("Silahkan coba lagi")
                    else:
                        print("Perubahan dibatalkan")
                        input("Tekan enter untuk melanjutkan")
                        clear_terminal()
                elif pilihan == '2':
                    while True:
                        try:
                            harga = int(input("Masukkan harga produk baru : "))
                            break
                        except ValueError:
                            print("Harga harus berupa angka")
                    
                    print("\nPreview Perubahan")
                    print(f"Harga Produk Lama : {data_semua['harga']}")
                    print(f"Harga Produk Baru : {harga}")
                    konfirmasi = input("\nSimpan Perubahan? (y/n) : ").lower()
                    if konfirmasi == 'y':
                        query = f"UPDATE produk SET harga={harga} WHERE id={produk} OR nama='{produk}'"
                        syntax.execute(query)
                        koneksi.commit()
                        data['Harga'] = harga
                        print("Data berhasil diubah")
                        input("Tekan enter untuk melanjutkan")
                        clear_terminal()
                    else:
                        print("Perubahan dibatalkan")
                        input("Tekan enter untuk melanjutkan")
                        clear_terminal()
                elif pilihan == '3':
                    while True:
                        try:
                            stok = int(input("Masukkan stok tambahan : "))
                            break
                        except ValueError:
                            print("Stok harus berupa angka")
                    print("\nPreview Perubahan")
                    print(f"Stok Produk Lama : {data_semua['stok']}")
                    print(f"Stok Produk Baru : {data_semua['stok'] + stok}")
                    konfirmasi = input("\nSimpan Perubahan? (y/n) : ").lower()
                    if konfirmasi == 'y':   
                        try:
                            query = "UPDATE produk SET stok = %s WHERE id_produk = %s"
                            syntax.execute(query, (data_semua["stok"]+stok, data_semua["id_produk"]))
                            koneksi.commit()
                            data['Stok'] = data_semua['stok'] + stok    
                            print("Stok berhasil ditambah")
                            input("Tekan enter untuk melanjutkan")
                            clear_terminal()
                        except Exception as e:
                            print("Data gagal diubah")
                            print(e)
                            print("Silahkan coba lagi")
                    else:
                        print("Perubahan dibatalkan") 
                        input("Tekan enter untuk melanjutkan")
                        clear_terminal()
                elif pilihan == '4':
                    while True:
                        kategori = input("Masukkan kategori produk baru : ").lower().strip()
                        if kategori not in ['seserahan', 'dekorasi', 'souvenir', 'mahar']:
                            print("Kategori tidak valid, silahkan coba lagi")
                            continue
                        else:
                            break
                    syntax.execute("SELECT id_kategori FROM kategori kategori = %s", (kategori,))
                    data_kategori = syntax.fetchone()
                    print("\nPreview Perubahan")
                    print(f"Kategori Produk Lama : {data_semua['kategori']}")
                    print(f"Kategori Produk Baru : {kategori}")
                    konfirmasi = input("\nSimpan Perubahan? (y/n) : ").lower()
                    if konfirmasi == 'y':
                        query = "UPDATE produk SET kategori = %s WHERE id_produk = %s"
                        syntax.execute(query, (data_kategori["id_kategori"], data["id_produk"]))
                        koneksi.commit()
                        data['Kategori'] = kategori
                        print("Kategori berhasil diubah")
                        input("Tekan enter untuk melanjutkan")
                        clear_terminal()
                    else:
                        print("Perubahan dibatalkan")
                        input("Tekan enter untuk melanjutkan")
                        clear_terminal()
                elif pilihan == '5':
                    clear_terminal()
                    return
                else:
                    print("Hanya masukkan (1/2/3/4/5)")
                    input("Tekan enter untuk melanjutkan")
                    clear_terminal()
        except Exception as e:
            print("Terjadi Kesalahan :", e)
            koneksi.rollback()
            input("Tekan enter untuk kembali")
            clear_terminal()
    elif pilihan == '3':
        try:
            while True:
                produk = input("Masukkan id/nama produk yang ingin dihapus : ")
                try:
                    id_produk = int(produk) 
                    query = "SELECT nama AS \"Nama\", harga AS \"Harga\", stok AS \"Stok\", disewakan FROM produk WHERE id_produk = %s"
                    syntax.execute(query, (id_produk,))
                except ValueError:
                    query = "SELECT nama AS \"Nama\", harga AS \"Harga\", stok AS \"Stok\", disewakan FROM produk WHERE nama ILIKE %s"
                    syntax.execute(query, (f"%{produk}%",))
                    
                data = syntax.fetchone()
                if not data:
                    print("Produk tidak ditemukan")
                else:
                    print("Berikut adalah data produk yang akan dihapus :")
                    print(tabulate([data]), header="keys", tablefmt="fancy_grid")
                    break
            while True:
                print("""
                            ╔══════════════════════════════════╗
                            ║        Yakin ingin dihapus       ║
                            ║┌────────────────────────────────┐║
                            ║│        1. Hapus Produk         │║
                            ║│        2. Kembali              │║
                            ║└────────────────────────────────┘║
                            ╚══════════════════════════════════╝""")
                pilihan = input("Pilih program : ")
                if pilihan == '1':
                    try:
                        query = "DELETE FROM produk WHERE id_produk =%s"
                        syntax.execute(query, (data['id_produk'],))
                        koneksi.commit()
                        print("Data berhasil dihapus")
                        input("Tekan enter untuk melanjutkan")
                        clear_terminal()
                        break
                    except Exception as e:
                        print("Data gagal dihapus")
                        print("Tekan enter untuk kembali")
                        clear_terminal()
                        break
                elif pilihan == '2':
                    clear_terminal()
                    break
                else:
                    print("Hanya masukkan (1/2)")
                    continue
        except Exception as e:
            print("Terjadi Kesalahan", e)
            input("Tekan enter untuk kembali")
            clear_terminal()
        finally:
            syntax.close()
            koneksi.close()

def ChatWa(data_akun,data_produk,jumlah,data_metode,id_metode_pembayaran,data_penyewaan,teks, mode='beli'):
    metode_bayar = next((item for item in data_metode if item['id_metode_pembayaran'] == id_metode_pembayaran), None) 
    if not metode_bayar:
        metode_nama = "Tidak dikenali"
    else:
        metode_nama = metode_bayar['metode_pembayaran']
    link = "https://wa.me/6287863306466?text="
    if mode == 'beli':
        total_harga = data_produk['harga'] * int(jumlah)
        pesan = (
            "Halo admin Cantiknya Mahar,\n"
            f"Saya ingin melakukan konfirmasi pembelian:\n\n"
            f"Nama Customer \t\t: {data_akun['nama']}\n"
            f"Nama Produk \t\t: {data_produk['nama']}\n"
            f"Jumlah Produk \t\t: {jumlah}\n"
            f"Metode Pembayaran \t: {metode_nama}\n"
            f"Total Harga \t\t: {format_rupiah(total_harga)}\n"
            f"{teks}"
        )
    elif mode == 'sewa':
        id_penyewaan = data_penyewaan['id_penyewaan']
        pembayaran_dp = data_penyewaan['pembayaran_dp']
        tanggal_sewa = data_penyewaan['tanggal_sewa']
        tanggal_kembali = data_penyewaan['tanggal_kembali']
        try:
            if tanggal_sewa != '-' and tanggal_kembali != '-':
                durasi = (dt.datetime.strptime(str(tanggal_kembali), '%Y-%m-%d') - 
                          dt.datetime.strptime(str(tanggal_sewa), '%Y-%m-%d')).days
            else:
                durasi = '-'
        except Exception as e:
            print("Error saat hitung durasi:", e)
            durasi = '-'
        pesan = (
            "Halo admin Cantiknya Mahar, saya ingin melakukan penyewaan produk berikut:\n"
            f"Id Penyewaan \t\t: {id_penyewaan}\n"
            f"Nama Customer \t\t : {data_akun['nama']}\n"
            f"Nama Produk \t\t : {data_produk['nama']}\n"
            f"Jumlah Produk \t\t : {jumlah}\n"
            f"Jumlah dp \t\t : {format_rupiah(pembayaran_dp)}\n"
            f"Tanggal Penyewaan \t : {tanggal_sewa}\n"
            f"Tanggal Kembali \t\t : {tanggal_kembali}\n"
            f"Durasi Penyewaan \t : {durasi} hari\n"
            f"Metode Pembayaran \t : {metode_nama}\n"
            f"{teks}\n"
        )
    else:
        pesan = (
            "Halo admin Cantiknya Mahar, saya ingin melakukan konfirmasi:\n"
            f"Nama Customer \t: {data_akun['nama']}\n"
            f"{teks}\n"
        )
    pesan = pesan.replace(" ", "%20").replace("\n", "%0A").replace("\t", "%09")
    return link + pesan

def Beli(data_produk,data_akun,jumlah):
    koneksi = connect()
    kursor = koneksi.cursor(cursor_factory=RealDictCursor)
    try:
        query = f"SELECT * FROM keranjang Where id_customer={data_akun['id_customer']}"
        kursor.execute(query)
        data_keranjang = kursor.fetchall()

        total_harga = 0
        daftar_pembelian = []
        tanya = ''

        if data_keranjang:
            print("Nampaknya anda memiliki barang dikeranjang, apakah anda ingin membelinya sekalian?", end=" ")
            tanya = input("(Y/N) : ")
            if tanya.lower() == 'y':
                for item in data_keranjang:
                    query = f"SELECT * FROM produk WHERE id_produk = {item['id_produk']}"
                    kursor.execute(query)
                    data_produk = kursor.fetchone()
                    if data_produk:
                        daftar_pembelian.append({
                            'id_produk': data_produk['id_produk'],
                            'nama': data_produk['nama'],
                            'harga': data_produk['harga'],
                            'jumlah': item['jumlah']
                        })
                        total_harga += data_produk['harga'] * item['jumlah']
                print("\nBerikut adalah barang-barang di keranjang Anda:")
                for p in daftar_pembelian:
                    print(f"{p['nama']} x {p['jumlah']} = Rp{p['harga'] * p['jumlah']}")
                print(f"\nTotal harga \t: Rp{total_harga}")


        if not (data_keranjang and tanya.lower() == 'y'):
            if not data_produk:
                print("Data produk tidak ditemukan")
                input("Tekan enter untuk melanjutkan...")
                clear_terminal()
                return
            daftar_pembelian.append({
                'id_produk': data_produk['id_produk'],
                'nama': data_produk['nama'],
                'harga': data_produk['harga'],
                'jumlah': jumlah})
            total_harga = data_produk['harga'] * int(jumlah)

        print("Apakah Anda ingin melanjutkan ke pembayaran?", end=" ")
        konfirmasi = input("(Y/N) : ")
        if konfirmasi.lower() != 'y':
            print("Pembelian dibatalkan")
            return

        tanggal = dt.datetime.now()
        harga = data_produk ['harga'] * int(jumlah)
        query = f"SELECT * FROM metode_pembayaran"
        kursor.execute(query)
        data_metode = kursor.fetchall()
        id_metode_pembayaran = None
        print("""
                    ╔══════════════════════════════════╗
                    ║      Pilih Metode Pembayaran     ║
                    ║┌────────────────────────────────┐║
                    ║│        1. Bank BRI             │║
                    ║│        2. Bank BCA             │║
                    ║│        3. Shopee Pay           │║
                    ║│        4. Dana                 │║
                    ║│        5. Cash                 │║
                    ║│        6. Kembali              │║
                    ║└────────────────────────────────┘║
                    ╚══════════════════════════════════╝""")
        while True:
            metode_pembayaran = input("Pilih metode pembayaran : ")
            if metode_pembayaran in ["1", "2", "3", "4", "5"]:
                id_metode_pembayaran = int(metode_pembayaran)
                break
            elif metode_pembayaran == "6":
                print("Kembali ke menu utama")
                input("Tekan enter untuk melanjutkan...")
                clear_terminal()
                return
            else:
                print("Metode pembayaran tidak valid, silahkan coba lagi")
        query = "SELECT * FROM jenis_transaksi WHERE nama_jenis = 'Pembelian'"
        kursor.execute(query)
        jenis_transaksi = kursor.fetchone()
        for item in daftar_pembelian:
            try:
                if 'id_transaksi' not in locals():
                    query = "INSERT INTO transaksi (tanggal, nominal, id_customer, id_metode_pembayaran, id_penyewaan, id_jenis_transaksi) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_transaksi"
                    kursor.execute(query,(
                        tanggal,
                        total_harga,
                        data_akun['id_customer'],
                        id_metode_pembayaran,
                        None,
                        jenis_transaksi['id_jenis_transaksi']
                    ))
                    id_transaksi = kursor.fetchone()['id_transaksi']
                    koneksi.commit()
                query = """
                    INSERT INTO item_transaksi
                    (id_produk, jumlah, id_transaksi)
                    VALUES (%s, %s, %s)"""
                nominal = item['harga'] * int(item['jumlah'])
                kursor.execute(query, (item['id_produk'], item['jumlah'], id_transaksi))
                print(f"Berikut detail pembelian {data_akun['nama']}:")
                print(f"Nama Produk \t\t: {item['nama']}")
                print(f"Jumlah Produk \t\t: {item['jumlah']}")
                print(f"Total Harga \t\t: {format_rupiah(nominal)}")
                print(f"Metode Pembayaran\t: {data_metode[id_metode_pembayaran-1]['metode_pembayaran']}")
                print(f"Tanggal Pembelian\t: {tanggal.strftime('%Y-%m-%d %H:%M:%S')}")
                print("Silahkan melakukan pembayaran ke nomo rekening berikut : ", data_metode[id_metode_pembayaran-1]['no_rekening'],"\n")
                print("Setelah melakukan pembayaran, silahkan konfirmasi ke admin dengan klik link berikut:")
                url = ChatWa(data_akun, item, item['jumlah'], data_metode,id_metode_pembayaran, {}, "Saya ingin melakukan konfirmasi pembayaran", mode='beli')
                print(url)

                query = f"UPDATE produk SET stok=stok-{item['jumlah']} WHERE id_produk={item['id_produk']}"
                kursor.execute(query)
                koneksi.commit()
            except Exception as e:
                print("Terjadi kesalahan saat menyimpan transaksi")
                print(e)
                input("Tekan enter untuk melanjutkan...")
                return
        input("Tekan enter untuk melanjutkan...")
        clear_terminal()

        if data_keranjang and tanya.lower() == 'y':
            query = f"DELETE FROM keranjang WHERE id_customer={data_akun['id_customer']}"
            kursor.execute(query)
            koneksi.commit()
        input("Tekan enter untuk melanjutkan")
        clear_terminal()
    except Exception as e:
        print("Pembelian gagal")
        print(e)
        print("Silahkan coba lagi")
    finally:
        kursor.close()
        koneksi.close()
    
def Sewa(data_produk,data_akun, jumlah):
    koneksi = connect()
    kursor = koneksi.cursor(cursor_factory=RealDictCursor)

    try:
        if data_akun['id_alamat'] is None:
            hiasan("Mohon Maaf, anda belum bisa meminjam")
            print("Silahkan lengkapi data alamat Anda terlebih dahulu")
            input("Tekan enter untuk melanjutkan...")
            clear_terminal()
            return

        query = f"SELECT * FROM keranjang WHERE id_customer={data_akun['id_customer']}"
        kursor.execute(query)
        data_keranjang = kursor.fetchall()

        daftar_sewa = []
        tanya = ''

        if data_keranjang:
            print("Nampaknya Anda memiliki barang di keranjang.")
            tanya = input("Apakah Anda ingin menyewa barang dari keranjang? (Y/N): ").strip().lower()
            if tanya == 'y':
                for item in data_keranjang:
                    query = f"SELECT * FROM produk WHERE id_produk = {item['id_produk']}"
                    kursor.execute(query)
                    produk = kursor.fetchone()
                    if produk and produk['disewakan']:
                        daftar_sewa.append({
                            'id_produk': produk['id_produk'],
                            'nama': produk['nama'],
                            'harga_sewa': (produk['harga'] // 50),
                            'jumlah': item['jumlah']
                        })
                if not daftar_sewa:
                    print("Tidak ada produk yang tersedia untuk disewa di keranjang.")
                    input("Tekan enter untuk melanjutkan...")
                    return

                print("\nBerikut adalah barang di keranjang:")
                print(tabulate(daftar_sewa, headers="keys", tablefmt="fancy_grid"))
                print("""
Apakah Anda ingin:
1. Menyewa semua produk?
2. Menyewa hanya satu produk?
""")
                pilih = input("Pilih opsi (1/2): ").strip()
                if pilih == "2":
                    while True:
                        id_pilih = int(input("Masukkan ID produk yang ingin disewa: "))
                        ditemukan = False
                        daftar_sewa_baru = []
                        for item in daftar_sewa:
                            if item['id_produk'] == id_pilih:
                                daftar_sewa_baru.append(item)
                                ditemukan = True
                        if not ditemukan:
                            print("ID produk tidak ditemukan di keranjang.")
                            input("Enter untuk mencoba lagi...")
                        else:
                            daftar_sewa = daftar_sewa_baru
                            break
        try:
            if not (data_keranjang and tanya == 'y'):
                if not data_produk['disewakan']:
                    print("Produk ini tidak tersedia untuk disewa.")
                    input("Tekan enter untuk melanjutkan...")
                    return
                daftar_sewa.append({
                    'id_produk': data_produk['id_produk'],
                    'nama': data_produk['nama'],
                    'harga_sewa': (data_produk['harga'] * Decimal(0.5)),
                    'jumlah': int(jumlah)
                })
        except Exception as e:
            print(f"Terjadi kesalan : {e}")
            input("Tekan enter untuk melanjutkan...")

        for item in daftar_sewa:
            if item['jumlah'] > data_produk['stok']:
                print(f"Jumlah {item['nama']} melebihi stok yang tersedia.")
                input("Tekan enter untuk melanjutkan...")
                return

        print("Apakah Anda ingin melanjutkan ke pembayaran DP?", end=" ")
        konfirmasi = input("(Y/N): ").strip().lower()
        if konfirmasi != 'y':
            print("Penyewaan dibatalkan.")
            input("Tekan enter untuk melanjutkan...")
            return

        query = "SELECT * FROM metode_pembayaran"
        kursor.execute(query)
        data_metode = kursor.fetchall()
        id_metode_pembayaran = None

        if data_metode:
            print("""
                        ╔══════════════════════════════════╗
                        ║      Pilih Metode Pembayaran     ║
                        ║┌────────────────────────────────┐║
                        ║│        1. Bank BRI             │║
                        ║│        2. Bank BCA             │║
                        ║│        3. Shopee Pay           │║
                        ║│        4. Dana                 │║
                        ║│        5. Cash                 │║
                        ║│        6. Kembali              │║
                        ║└────────────────────────────────┘║
                        ╚══════════════════════════════════╝""")
            while True:
                metode_input = input("Pilih metode pembayaran : ")
                if metode_input in ["1", "2", "3", "4", "5"]:
                    id_metode_pembayaran = int(metode_input)
                    break
                elif metode_input == "6":
                    print("Kembali ke menu utama")
                    clear_terminal()
                    return
                else:
                    print("Metode pembayaran tidak valid, silahkan coba lagi")
                    continue

        if id_metode_pembayaran is None:
            print("Harap pilih metode pembayaran")
            return

        tanggal_penyewaan = input("Masukkan tanggal penyewaan (YYYY-MM-DD) : ")
        tanggal_kembali = input("Masukkan tanggal kembali (YYYY-MM-DD) : ")
        durasi_hari = (dt.datetime.strptime(tanggal_kembali, '%Y-%m-%d') - dt.datetime.strptime(tanggal_penyewaan, '%Y-%m-%d')).days

        for item in daftar_sewa:
            biaya_sewa = item['harga_sewa'] * int(item['jumlah'])
            pembayaran_dp = input(f"Masukkan pembayaran DP (minimal {format_rupiah(biaya_sewa)}): ")

            query = """
                INSERT INTO penyewaan 
                (tanggal_sewa, tanggal_kembali, pembayaran_dp, status_dp, status_peminjaman, id_customer)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_penyewaan
            """
            kursor.execute(query, (
                tanggal_penyewaan,
                tanggal_kembali,
                pembayaran_dp,
                'belum dibayarkan',
                'masih proses',
                data_akun['id_customer']
            ))
            id_penyewaan = kursor.fetchone()['id_penyewaan']
            koneksi.commit()
            query_item = """
                INSERT INTO item_penyewaan (id_penyewaan, id_produk, jumlah, harga_sewa, durasi_hari)
                VALUES (%s, %s, %s, %s, %s)"""
            kursor.execute(query_item, (
                id_penyewaan,
                item['id_produk'],
                item['jumlah'],
                biaya_sewa,
                durasi_hari
            ))
            query = """
                INSERT INTO transaksi 
                (tanggal, nominal, id_customer, id_metode_pembayaran, id_penyewaan, id_jenis_transaksi)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            tanggal_transaksi = dt.datetime.now()
            kursor.execute(query, (
                tanggal_transaksi,
                biaya_sewa,
                data_akun['id_customer'],
                id_metode_pembayaran,
                id_penyewaan,
                2
            ))
            koneksi.commit()

            query = f"UPDATE produk SET stok = stok - {item['jumlah']} WHERE id_produk = {item['id_produk']}"
            kursor.execute(query)
            koneksi.commit()

        if data_keranjang and tanya == 'y':
            query = f"DELETE FROM keranjang WHERE id_customer={data_akun['id_customer']}"
            kursor.execute(query)
            koneksi.commit()
        query = "SELECT * FROM penyewaan WHERE id_penyewaan = %s"
        kursor.execute(query, (id_penyewaan,))
        data_penyewaan = kursor.fetchone()
        print("Penyewaan berhasil diproses!")
        print(f"Berikut adalah detail penyewaan {data_akun['nama']}:")
        print(f"Nama Produk \t\t: {item['nama']}")
        print(f"Jumlah Produk \t\t: {item['jumlah']}")
        print(f"Biaya DP \t\t: {format_rupiah(item['harga_sewa'] * int(item['jumlah']))}")
        print(f"Metode Pembayaran\t: {data_metode[id_metode_pembayaran-1]['metode_pembayaran']}")
        print(f"Tanggal Penyewaan\t: {tanggal_penyewaan}")
        print(f"Tanggal Kembali \t: {tanggal_kembali}")
        print(f"Durasi Penyewaan \t: {durasi_hari} hari")
        print("Silahkan melakukan pembayaran DP ke nomor rekening berikut:", data_metode[id_metode_pembayaran-1]['no_rekening'])
        print("Setelah melakukan pembayaran, silahkan konfirmasi ke admin dengan klik link berikut:")
        input("Tekan enter untuk mengenerate link WhatsApp...")
        try:
            url = ChatWa(data_akun, data_produk, jumlah, data_metode,id_metode_pembayaran, data_penyewaan, "\nSaya ingin menghubungi admin untuk konfirmasi penyewaan, Mohon untuk diacc", mode='sewa')
            print(f"Silahkan klik link berikut untuk menghubungi admin:\n{url}")
        except Exception as e:
            print("Terjadi kesalahan saat membuat link WhatsApp:", e)
            input("Tekan enter untuk melanjutkan...")
            return
        input("Tekan enter untuk melanjutkan...")
        clear_terminal()

    except Exception as e:
        input("Penyewaan gagal:", e)
        koneksi.rollback()
    finally:
        kursor.close()
        koneksi.close()


def InformasiAkun(role,data_akun):
    koneksi = connect()
    kursor = koneksi.cursor(cursor_factory=RealDictCursor)
    if role == 'admin':
        query = f"SELECT * FROM akun_admin WHERE id_admin = {data_akun['id_admin']}"
        kursor.execute(query)
        data = kursor.fetchall()
        if data:
            print("Berikut adalah informasi akun anda:")
            print(f"Nama Admin \t: {data[0]['nama']}")
            print(f"No HP Admin \t: {data[0]['no_hp']}")
            print(f"Username Admin \t: {data[0]['username']}")
            print(f"Password Admin \t: {data[0]['password']}")
            input("Tekan enter untuk kembali")
            clear_terminal()
        else:
            print("Tidak ada informasi akun admin yang tersedia")
            input("Tekan enter untuk kembali")
            clear_terminal()
    elif role == 'customer':
        query = "SELECT * FROM customer WHERE id_customer = %s"
        kursor.execute(query, (data_akun['id_customer'],))
        data = kursor.fetchall()
        if data:
            print("Berikut adalah informasi akun customer:")
            print(f"Nama Customer \t\t: {data[0]['nama']}")
            print(f"No HP Customer \t\t: {data[0]['no_hp']}")
            print(f"Username Customer \t: {data[0]['username']}")
            print(f"Password Customer \t: {data[0]['password']}")
            print(f"Email Customer \t\t: {data[0]['email_address']}")
            if data[0]['id_alamat'] != None:
                query = "SELECT * FROM alamat WHERE id_alamat = %s"
                kursor.execute(query, (data[0]['id_alamat'],))
                data_alamat = kursor.fetchall()
                if data_alamat:
                    print(f"Alamat : {data_alamat[0]['provinsi']},{data_alamat[0]['kabupaten']},{data_alamat[0]['kecamatan']},{data_alamat[0]['desa']},{data_alamat[0]['dusun']},{data_alamat[0]['rw']}/{data_alamat[0]['rt']}")
                    input("Tekan enter untuk melanjutkan")
            else:
                print("Nampaknya anda belum memiliki alamat yang terdaftar")
                tanya = input("Apakah anda ingin menambahkan alamat? (y/n) : ")
                if tanya.lower() == 'y':
                    provinsi = input("Masukkan provinsi : ")
                    kabupatenkota = input("Masukkan kabupaten/kota : ")
                    kecamatan = input("Masukkan kecamatan : ")
                    desa = input("Masukkan desa : ")
                    dusun = input("Masukkan dusun : ")
                    rt = input("Masukkan rt : ")
                    rw = input("Masukkan rw : ")
                    query = f"INSERT INTO alamat (provinsi, kabupatenkota, kecamatan, desa, dusun, rt, rw) VALUES ('{provinsi}', '{kabupatenkota}', '{kecamatan}', '{desa}', '{dusun}', '{rt}', '{rw}')"
                    kursor.execute(query)
                    koneksi.commit()
                    print("Data alamat berhasil disimpan")
                    query = f"UPDATE customer SET id_alamat=(SELECT id_alamat FROM alamat WHERE provinsi='{provinsi}' AND kabupatenkota='{kabupatenkota}' AND kecamatan='{kecamatan}' AND desa='{desa}' AND dusun='{dusun}' AND rt='{rt}' AND rw='{rw}') WHERE id_customer={data[0]['id_customer']}"
                    kursor.execute(query)
                    koneksi.commit()
                    hiasan("Terimakasih telah menambahkan Alamat")
                    input("Tekan enter untuk melanjutkan")
                    clear_terminal()
                else:
                    print("Jika anda tidak mengisi alamat maka anda tidak bisa melakukan penyewaan")
                    input("Tekan enter untuk melanjutkan")
                    clear_terminal()
        else:
            print("Tidak ada informasi akun customer yang tersedia")
            input("Tekan enter untuk melanjutkan")
            clear_terminal()

def Keranjang(data_akun):
    koneksi = connect()
    kursor = koneksi.cursor(cursor_factory=RealDictCursor)
    try:
        query = f"SELECT * FROM keranjang WHERE id_customer={data_akun['id_customer']}"
        kursor.execute(query)
        data_keranjang = kursor.fetchall()
        if not data_keranjang:
            print("Keranjang belanja anda kosong")
            input("Tekan enter untuk kembali")
            clear_terminal()
            return
        print("Berikut adalah keranjang belanja anda:")
        print(tabulate(data_keranjang, headers="keys", tablefmt="fancy_grid"))
        tanya = input("Apakah anda ingin lanjut ke pembelian? (y/n) : ")
        if tanya != 'y':
            clear_terminal()
            return
        pilihan = input("Anda ingin membeli salah satu produk atau semua produk? (s/a) : ").strip().lower()
        daftar_pembelian = []
        if pilihan == 's':
            produk_input = input("Masukkan id/nama produk yang ingin dibeli : ")
            try:
                id_produk = int(produk_input)
                query = """
                    SELECT p.id_produk, p.nama, p.harga, k.jumlah
                    FROM produk p
                    JOIN keranjang k ON p.id_produk = k.id_produk
                    WHERE k.id_produk = %s AND k.id_customer = %s"""
                kursor.execute(query, (id_produk, data_akun['id_customer']))
            except ValueError:
                query = """
                    SELECT p.id_produk, p.nama, p.harga, k.jumlah
                    FROM produk p
                    JOIN keranjang k ON p.id_produk = k.id_produk
                    WHERE p.nama ILIKE %s AND k.id_customer = %s"""
                kursor.execute(query, (f"%{produk_input}%", data_akun['id_customer']))
            data_produk = kursor.fetchone()
            if not data_produk:
                print("Produk tidak ditemukan di keranjang")
                input("Tekan enter untuk kembali")
                clear_terminal()
                return
            print("Berikut adalah data produk yang ingin dibeli:")
            print(tabulate([data_produk], headers="keys", tablefmt="fancy_grid"))
            while True:
                jumlah_input = input(f"Masukkan jumlah (tersedia : {data_produk['jumlah']}): ")
                try:
                    jumlah = int(jumlah_input)
                    if jumlah <= 0 or jumlah > data_produk['jumlah']:
                        print("Jumlah tidak valid atau melebihi stok yang tersedia")
                    else:
                        break
                except ValueError:
                    print("Jumlah harus berupa angka")
            Beli(data_produk, data_akun, jumlah)
            sisa = data_produk['jumlah'] - jumlah
            if sisa <= 0:
                query = "DELETE FROM keranjang WHERE id_produk = %s AND id_customer = %s"
                kursor.execute(query, (data_produk['id_produk'], data_akun['id_customer']))
            else:
                query = "UPDATE keranjang SET jumlah = %s WHERE id_produk = %s AND id_customer = %s"
                kursor.execute(query, (sisa, data_produk['id_produk'], data_akun['id_customer']))
            koneksi.commit()
        elif pilihan == 'a':
            query = """
                SELECT p.id_produk, p.nama, p.harga, k.jumlah 
                FROM produk p 
                JOIN keranjang k ON p.id_produk = k.id_produk 
                WHERE k.id_customer = %s
            """
            kursor.execute(query, (data_akun['id_customer'],))
            semua_produk = kursor.fetchall()
            if not semua_produk:
                print("Tidak ada produk yang tersedia di keranjang")
                input("Tekan enter untuk kembali")
                clear_terminal()
                return
            print("Berikut adalah semua produk yang ingin dibeli:")
            print(tabulate(semua_produk, headers="keys", tablefmt="fancy_grid"))
            konfirmasi = input("Apakah Anda ingin membeli semua produk? (y/n) : ").strip().lower()
            if konfirmasi != 'y':
                print("Pembelian dibatalkan")
                input("Tekan enter untuk kembali")
                clear_terminal()
                return
            for item in semua_produk:
                Beli(item, data_akun, item['jumlah'])
            query = "DELETE FROM keranjang WHERE id_customer = %s"
            kursor.execute(query, (data_akun['id_customer'],))
            koneksi.commit()
        else:
            print("Pilihan tidak valid, silahkan coba lagi")
            input("Tekan enter untuk kembali")
            clear_terminal()
    except Exception as e:
        print("Terjadi kesalahan:", e)
        input("Tekan enter untuk kembali")
        koneksi.rollback()
    finally:
        kursor.close()
        koneksi.close()

def JualSewa(data_akun):
    koneksi = connect()
    kursor = koneksi.cursor(cursor_factory=RealDictCursor)
    query = "SELECT id_produk,nama,harga,stok FROM produk order by id_produk"
    kursor.execute(query)
    data_produk = kursor.fetchall()
    print("Berikut adalah katalog produk:")
    print(tabulate(data_produk, headers="keys", tablefmt="fancy_grid"))
    print("Silahkan pilih produk yang ingin dibeli/disewa")
    try:
        while True:
            keyword = input("Masukkan id/nama produk : ")
            try:
                id_produk = int(keyword) 
                query = "SELECT id_produk,nama,harga,stok,disewakan FROM produk WHERE id_produk = %s ORDER BY id_produk"
                kursor.execute(query, (id_produk,))
            except ValueError:
                query = "SELECT id_produk,nama,harga,stok,disewakan FROM produk WHERE nama ILIKE %s ORDER BY id_produk"
                kursor.execute(query, (f"%{keyword}%",))
            try:
                data_produk = kursor.fetchall()
                if not data_produk:
                    print("Produk tidak ditemukan")
                    continue
                elif len(data_produk) > 1:
                    data_tampil = []
                    for produk in data_produk:
                        teks = "Bisa Disewa" if produk['disewakan'] else "Dijual"
                        data_tampil.append([
                            produk["id_produk"],
                            produk["nama"],
                            format_rupiah(produk["harga"]),
                            produk["stok"],
                            teks
                        ])
                    headers = ["Id Produk", "Nama", "Harga", "Stok", "Keterangan"]
                    print("Ditemukan beberapa produk dengan nama yang sama")
                    print(tabulate(data_tampil, headers=headers, tablefmt="fancy_grid"))
                    print("\nHarap masukkan id/nama produk secara spesifik")
                    continue
                else:
                    data_tampil = []
                    produk = data_produk[0]
                    teks = "Bisa Disewa" if produk['disewakan'] else "Dijual"
                    data_tampil.append([
                        produk["id_produk"],
                        produk["nama"],
                        format_rupiah(produk["harga"]),
                        produk["stok"],
                        teks
                    ])
                    headers = ["Id Produk", "Nama", "Harga", "Stok", "Keterangan"]
                    print("Berikut adalah data produk yang dipilih:")
                    print(tabulate(data_tampil, headers=headers, tablefmt="fancy_grid"))
                    break
            except Exception as e:
                print("Gagal menampilkan data produk")
                print(e)
        data_produk = data_produk[0]
        while True:
            print("""\n
                          ╔══════════════════════════════════╗
                          ║          Pilihan Anda            ║
                          ║┌────────────────────────────────┐║
                          ║│        1. Beli Produk          │║
                          ║│        2. Sewa Produk          │║ 
                          ║│        3. Masukkan Kranjang    │║
                          ║│        4. Kembali              │║
                          ║└────────────────────────────────┘║
                          ╚══════════════════════════════════╝""")
            pilihan = input("Pilih program : ")
            if pilihan == '1':
                if data_produk['disewakan'] == True:
                    print("Produk tidak tersedia untuk dibeli")
                    input("Tekan enter untuk melanjutkan")
                    clear_terminal()
                    break
                while True:
                    jumlah = input("Masukkan jumlah produk yang ingin dibeli : ")
                    if int(jumlah) > data_produk['stok']:
                        print("Jumlah produk yang ingin dibeli melebihi stok yang tersedia")
                    elif int(jumlah) <= 0:
                        print("Jumlah produk yang ingin dibeli tidak valid")
                    else:
                        break
                Beli(data_produk,data_akun,jumlah)
                clear_terminal()
                return
            elif pilihan == '2':
                if data_produk['disewakan'] == False:
                    print("Produk tidak tersedia untuk disewa")
                    input("Tekan enter untuk melanjutkan")
                    clear_terminal()
                    break
                while True:
                    jumlah = input("Masukkan jumlah produk yang ingin disewa : ")
                    if int(jumlah) > data_produk['stok']:
                        print("Jumlah produk yang ingin disewa melebihi stok yang tersedia")
                    elif int(jumlah) <= 0:
                        print("Jumlah produk yang ingin disewa tidak valid")
                    else:
                        break
                Sewa(data_produk,data_akun,jumlah)
                clear_terminal()
                return
            elif pilihan == '3':
                try:
                    while True:
                        jumlah = input("Masukkan jumlah produk yang ingin dimasukkan ke keranjang : ")
                        if int(jumlah) > data_produk['stok']:
                            print("Jumlah produk yang ingin dimasukkan ke keranjang melebihi stok yang tersedia")
                        else:
                            break
                    query = f"INSERT INTO keranjang (id_customer) VALUES ({data_akun ['id_customer']})"
                    kursor.execute(query)
                    koneksi.commit()
                    query = f"SELECT id_keranjang FROM keranjang WHERE id_customer = {data_akun['id_customer']}"
                    kursor.execute(query)
                    id_keranjang = kursor.fetchone()['id_keranjang']
                    query = """
                        INSERT INTO detail_keranjang (id_keranjang, id_produk, jumlah)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (id_detail_keranjang)
                        DO UPDATE SET jumlah = detail_keranjang.jumlah + EXCLUDED.jumlah"""
                    kursor.execute(query, (id_keranjang, data_produk['id_produk'], jumlah))
                    koneksi.commit()
                    query = f"UPDATE produk SET stok = stok - {jumlah} WHERE id_produk = {data_produk['id_produk']}"
                    kursor.execute(query)
                    koneksi.commit()
                    print("Data berhasil dimasukkan ke keranjang")
                    input("Tekan enter untuk melanjutkan")
                    clear_terminal()
                except Exception as e:
                    print("Data gagal dimasukkan ke keranjang")
                    print(e)
                    print("Silahkan coba lagi")
            elif pilihan == '4':
                clear_terminal()
                break
            else:
                print("Hanya masukkan (1/2/3)")
                continue
    except Exception as e:
        print("Data gagal ditampilkan")
        print(e)
        print("Silahkan coba lagi")
    finally:
        kursor.close()
        koneksi.close()

def Pengembalian(data_akun):
    koneksi = None
    try:
        koneksi = connect()
        with koneksi.cursor(cursor_factory=RealDictCursor) as kursor:
            kursor.execute("SELECT EXISTS (SELECT 1 FROM penyewaan LIMIT 1)")
            tabel_kosong = not kursor.fetchone()['exists']
            if tabel_kosong:
                print("Tidak ada data penyewaan yang tersedia")
                input("Tekan enter untuk kembali")
                clear_terminal()
                return
            try:
                query = """
                    SELECT p.*, pr.nama as nama_produk
                    FROM penyewaan p
                    JOIN produk pr ON p.id_produk = pr.id_produk
                    WHERE p.id_customer = %s AND p.status_peminjaman IN ('dipinjam','masih proses')"""
                kursor.execute(query, (int(data_akun['id_customer']),))
                data_penyewaan = kursor.fetchall()

                if not data_penyewaan:
                    print("Tidak ada barang yang sedang disewa")
                    input("Tekan enter untuk kembali")
                    clear_terminal()
                    return
                print("Berikut adalah data barang yang anda sewa")
                print(tabulate(data_penyewaan, headers="keys", tablefmt="fancy_grid"))
            except Exception as e:
                print("Gagal menampilkan data penyewaan")
                print(e)
                input("Tekan enter untuk melanjutkan")
                clear_terminal()
                return
            tanya = input("Apakah anda ingin mengembalikan barang? (y/n) : ")
            if tanya.lower() == 'y':
                for sewa in data_penyewaan:
                    if sewa['status_peminjaman'] == 'dipinjam':
                        try:
                            query = """UPDATE penyewaan 
                            SET status_peminjaman = 'dikembalikan'
                            WHERE id_penyewaan = %s"""
                            kursor.execute(query, (sewa['id_penyewaan']))
                            koneksi.commit()
                            print(f"Barang {sewa['nama']} berhasil dikembalikan")
                        except Exception as e:
                            print(f"Gagal mengaembalikan {sewa['nama']}")
                            print(f"Karene {e}") 
                input("Tekan enter untuk melanjutkan")
                clear_terminal()

            masih_proses = input("Apakah anda ingin melihat barang yang masih dalam proses penyewaan? (y/n) : ")
            if masih_proses.lower() == 'y':
                query = """
                    SELECT p.*, pr.nama AS nama_produk
                    FROM penyewaan p
                    JOIN produk pr ON p.id_produk = pr.id_produk
                    WHERE p.id_customer = %s AND p.status_peminjaman = 'masih proses'
                    """
                kursor.execute(query, (data_akun['id_customer'],))
                data_penyewaan_proses = kursor.fetchall()

                if data_penyewaan_proses:
                    print("Berikut adalah barang yang masih dalam proses penyewaan:")
                    print(tabulate(data_penyewaan_proses, headers="keys", tablefmt="fancy_grid"))
                    chat = input("Apakah anda mau menghubungi admin untuk mempercepat proses penyewaan? (y/n) : ")
                    if chat.lower() == 'y':
                        query = """
                            SELECT * FROM metode_pembayaran
                            WHERE id_metode_pembayaran = %s"""
                        kursor.execute(query, (data_penyewaan_proses[0]['id_metode_pembayaran'],))
                        data_metode = kursor.fetchone()
                        pesan = input("Masukkan pesan yang ingin disampaikan ke admin : ")
                        url = ChatWa(data_akun,data_penyewaan_proses[0],data_penyewaan_proses[0]['jumlah'],data_metode,data_penyewaan_proses[0], pesan)
                        print(f"Silahkan klik link berikut untuk menghubungi admin : \n{url}")
                        input("Tekan enter untuk melanjutkan")
                        clear_terminal()
                else:
                    print("Tidak ada barang yang masih dalam proses penyewaan")
                    input("Tekan enter untuk melanjutkan")
                    clear_terminal()
    except Exception as e:
        print("Terjadi kesalahan : ", e)
        input("Tekan enter untuk melanjutkan")
        clear_terminal()
    finally:
        if koneksi:
            koneksi.close()
                
def kategori_produk():
    while True:
        print(
    """
╔══════════════════════════════════╗
║             Kategori             ║
║┌────────────────────────────────┐║""")
        print("║│                                │║")
        print("║│  1. Souvenir                   │║")
        print("║│  2. Dekorasi                   │║")
        print("║│  3. Mahar                      │║")
        print("║│  4. Seserahan                  │║")
        print("║│  5. Semua                      │║")
        print("║│  6. Kembali                    │║")
        print("║└────────────────────────────────┘║")
        print("╚══════════════════════════════════╝") 
        koneksi = connect()
        kursor = koneksi.cursor(cursor_factory=RealDictCursor)
        query = """SELECT pro.nama as "Nama Barang",
        pro.harga as "Harga", pro.stok as "Stok" from produk pro
        join kategori kat on pro.id_kategori = kat.id_kategori
        where kat.kategori = %s"""
        while True:
            kategori = input("Pilih yang ingin ditampilkan : ")
            match kategori:
                case "1":
                    kategori = "souvenir"
                    break
                case "2":
                    kategori = "dekorasi"
                    break
                case "3":
                    kategori = "mahar"
                    break
                case "4":
                    kategori = "seserahan"
                    break
                case "5":
                    kategori = "semua"
                    break
                case "6":
                    clear_terminal()
                    return
                case _:
                    print("Kategori tidak valid, silahkan coba lagi")
        if kategori == "semua":
            query = "SELECT pro.nama as \"Nama Barang\", pro.harga as \"Harga\", pro.stok as \"Stok\" from produk pro"
            kursor.execute(query)
            data = kursor.fetchall()
            if data:
                clear_terminal()
                print("Berikut adalah katalog semua produk:")
                print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
                input("Tekan enter untuk melanjutkan")
                clear_terminal()
            else:
                print("Tidak ada produk yang tersedia")
                input("Tekan enter untuk melanjutkan")
                clear_terminal()
        elif kategori == "seserahan" or kategori == "dekorasi" or kategori == "souvenir" or kategori == "mahar":
            query = f"SELECT pro.nama as \"Nama Barang\", pro.harga as \"Harga\", pro.stok as \"Stok\" from produk pro join kategori kat on pro.id_kategori = kat.id_kategori where lower(kat.kategori) = '{kategori}'"
            kursor.execute(query)
            data = kursor.fetchall()
            if data:
                clear_terminal()
                print(f"Berikut adalah katalog produk {kategori}:")
                print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
                input("Tekan enter untuk melanjutkan")
                clear_terminal()
            else:
                print(f"Tidak ada produk dengan kategori {kategori} yang tersedia")
                input("Tekan enter untuk melanjutkan")
                clear_terminal()
        else:
            print("Kategori tidak valid, silahkan coba lagi")  

def RiwayatTransaksi(role,data_akun):
    koneksi = connect()
    kursor = koneksi.cursor(cursor_factory=RealDictCursor)
    try:
        if role == 'admin':
            query = """
                SELECT 
                t.tanggal AS "Tanggal",
                t.nominal AS "Nominal",
                p.status_peminjaman AS "Status Peminjaman",
                t.id_penyewaan AS "ID Penyewaan"
                FROM transaksi t
                LEFT JOIN penyewaan p ON t.id_penyewaan = p.id_penyewaan
                ORDER BY t.tanggal DESC"""
            kursor.execute(query)
            
        elif role == 'customer':
            query = query = """
                SELECT 
                t.tanggal AS "Tanggal",
                t.nominal AS "Nominal",
                p.status_peminjaman AS "Status Peminjaman",
                t.id_penyewaan AS "ID Penyewaan"
                FROM transaksi t
                LEFT JOIN penyewaan p ON t.id_penyewaan = p.id_penyewaan
                WHERE t.id_customer = %s
                ORDER BY t.tanggal DESC"""
            kursor.execute(query, (data_akun['id_customer'],))
        data_riwayat = kursor.fetchall()
        tampilkan_data = []
        for baris in data_riwayat:
            baris_baru = dict(baris)
            baris_baru['ID Penyewaan'] = baris['ID Penyewaan'] if baris['ID Penyewaan'] is not None else '-'
            baris_baru['Status Peminjaman'] = baris['Status Peminjaman'] if baris['Status Peminjaman'] is not None else '-'
            if baris['ID Penyewaan'] is not None:
                baris_baru['Tipe Trnasaksi'] = 'Sewa'
            else:
                baris_baru['Tipe Trnasaksi'] = 'Beli'
            tampilkan_data.append(baris_baru)
        if tampilkan_data:
            print("Berikut adalah riwayat transaksi : ")
            print(tabulate(tampilkan_data, headers="keys", tablefmt="fancy_grid"))
        else:
            print("Tidak ada riwayat transaksi yang tersedia")
        input("Tekan enter untuk kembali")
        clear_terminal()
    except Exception as e:
        print("Terjadi kesalahan saat menampilkan riwayat transaksi:", e)
        input("Tekan enter untuk kembali")
        clear_terminal()
    finally:
        kursor.close()
        koneksi.close()

def AccPenyewaan():
    koneksi = connect() 
    kursor = koneksi.cursor(cursor_factory=RealDictCursor)
    try:
        query = f"""SELECT p.id_penyewaan, p.tanggal_sewa, p.tanggal_kembali,i.durasi_hari,p.pembayaran_dp, p.status_peminjaman, c.nama as customer, pr.nama as produk
            FROM penyewaan p 
            JOIN customer c ON p.id_customer = c.id_customer
            JOIN item_penyewaan i ON p.id_penyewaan = i.id_penyewaan
            JOIN produk pr ON i.id_produk = pr.id_produk
            WHERE status_peminjaman='masih proses'"""
        kursor.execute(query)
        data_penyewaan = kursor.fetchall()
        if data_penyewaan:
            print("Berikut adalah daftar penyewaan yang masih dalam proses:")
            print(tabulate(data_penyewaan, headers="keys", tablefmt="fancy_grid"))
            id_penyewaan = int(input("Masukkan id penyewaan yang ingin di acc atau ditolak : "))
            query = f"""SELECT p.*,it.*,c.* FROM penyewaan p 
                JOIN item_penyewaan it ON p.id_penyewaan = it.id_penyewaan
                JOIN customer c ON p.id_customer = c.id_customer
                WHERE p.id_penyewaan={id_penyewaan}"""
            kursor.execute(query)
            data_lengkap_penyewaan = kursor.fetchone()
            query = f"""SELECT p.id_penyewaan, p.tanggal_sewa, p.tanggal_kembali,i.durasi_hari,p.pembayaran_dp, p.status_peminjaman, c.nama as customer, pr.nama as produk
                FROM penyewaan p 
                JOIN customer c ON p.id_customer = c.id_customer
                JOIN item_penyewaan i ON p.id_penyewaan = i.id_penyewaan
                JOIN produk pr ON i.id_produk = pr.id_produk
                WHERE status_peminjaman='masih proses'
                AND p.id_penyewaan={id_penyewaan}"""
            kursor.execute(query)
            data_satu_penyewaan = kursor.fetchone()

            if not data_satu_penyewaan:
                print(f"Penyewaan dengan id {id_penyewaan} tidak ditemukan")
                return   
            else:
                print(tabulate([data_satu_penyewaan], headers="keys", tablefmt="fancy_grid"))
                print(
        """
        ╔══════════════════════════════════╗
        ║             Pilihan              ║
        ║┌────────────────────────────────┐║
        ║│                                │║
        ║│  1. Diacc                      │║
        ║│  2. Ditolak                    │║
        ║│  3. Chat customer              │║
        ║│  4. Kembali                    │║
        ║└────────────────────────────────┘║
        ╚══════════════════════════════════╝
        """)
                pilihan = input("Pilih program : ")
                if pilihan == '1':
                    query = f"UPDATE penyewaan SET status_peminjaman='dipinjam' WHERE id_penyewaan={id_penyewaan}"
                    kursor.execute(query)
                    koneksi.commit()
                    print(f"Penyewaan dengan id {id_penyewaan} berhasil di acc")
                elif pilihan == '2':
                    query = f"UPDATE penyewaan SET status_peminjaman='ditolak' WHERE id_penyewaan={id_penyewaan}"
                    kursor.execute(query)
                    koneksi.commit()
                    print(f"Penyewaan dengan id {id_penyewaan} berhasil ditolak")
                elif pilihan == '3':
                    try:
                        pesan = input("Masukkan pesan yang ingin disampaikan ke customer : ").replace(" ", "%20").replace("\n", "%0A")
                        print(f"Silahkan klik link berikut untuk menghubungi customer : \nwa.me/+{data_lengkap_penyewaan['no_hp']}?text={pesan}")
                        input("Tekan enter untuk melanjutkan")
                    except Exception as e:
                        print("Terjadi kesalahan saat menghubungi customer:", e)
                        input("Tekan enter untuk melanjutkan")
                        clear_terminal()
                        return
                elif pilihan == '4':
                    clear_terminal()
                else:
                    print("Hanya masukkan (1/2/3/4)")
            tanya = input("Apakah anda ingin mengacc penyewaan yang lain? (y/n) : ")
            if tanya.lower() == 'y':
                id_penyewaan = input("Masukkan id penyewaan yang ingin di acc : ")
                query = f"UPDATE penyewaan SET status_peminjaman='dipinjam' WHERE id_penyewaan={id_penyewaan}"
                kursor.execute(query)
                koneksi.commit()
                print(f"Penyewaan dengan id {id_penyewaan} berhasil di acc")
                input("Tekan enter untuk melanjutkan")
                clear_terminal()
            else:
                print("Penyewaan tidak di acc")
                input("Tekan enter untuk melanjutkan")
                clear_terminal()
        else:
            print("Tidak ada penyewaan yang masih dalam proses")
            input("Tekan enter untuk melanjutkan")
            clear_terminal()
    except Exception as e:
        print("Terjadi kesalahan saat mengacc penyewaan:", e)
        input("Tekan enter untuk melanjutkan")
        clear_terminal()
    finally:
        kursor.close()
        koneksi.close()

def tampilkan_menu_filter():
    print(
    """
    ╔══════════════════════════════════╗
    ║              Filter              ║
    ║┌────────────────────────────────┐║
    ║│                                │║
    ║│  1. Pembelian                  │║
    ║│  2. Penyewaan                  │║
    ║│  3. Bulan                      │║
    ║│  4. Minggu                     │║
    ║│  5. Kembali                    │║
    ║└────────────────────────────────┘║
    ╚══════════════════════════════════╝
    """)
def LaporanTransaksi():
    koneksi = connect()
    kursor = koneksi.cursor(cursor_factory=RealDictCursor)
    query_awal = """
    SELECT t.tanggal, t.nominal, c.nama, mp.metode_pembayaran 
    FROM transaksi t 
    FULL JOIN penyewaan p ON t.id_penyewaan = p.id_penyewaan
    JOIN metode_pembayaran mp ON t.id_metode_pembayaran = mp.id_metode_pembayaran
    JOIN customer c ON t.id_customer = c.id_customer
    """
    kursor.execute(query_awal)
    semua_transaksi = kursor.fetchall()

    print("Berikut adalah laporan transaksi keseluruhan:")
    print(tabulate(semua_transaksi, headers="keys", tablefmt="fancy_grid"))

    kursor.execute("SELECT SUM(nominal) AS total_transaksi FROM transaksi")
    total = kursor.fetchone()
    print(f"Total transaksi: {format_rupiah(total['total_transaksi'])}\n")
    while True:
        tampilkan_menu_filter()
        pilihan = input("Silakan pilih opsi filter (1-5): ")
        if pilihan == "1":
            query = "SELECT * FROM transaksi WHERE id_penyewaan IS NULL"
            kursor.execute(query)
            hasil = kursor.fetchall()
            print("\nTransaksi Pembelian:")
            print(tabulate(hasil, headers="keys", tablefmt="fancy_grid") if hasil else "Tidak ada data.")
        elif pilihan == "2":
            query = "SELECT * FROM transaksi WHERE id_penyewaan IS NOT NULL"
            kursor.execute(query)
            data_transaksi = kursor.fetchall()
            if data_transaksi:
                print("Berikut adalah laporan transaksi penyewaan:")
                print(tabulate(data_transaksi, headers="keys", tablefmt="fancy_grid"))
            else:
                print("Tidak ada transaksi penyewaan yang tersedia")
        elif pilihan == "3":
            bulan = input("Masukkan bulan (1-12) : ")
            query = f"SELECT * FROM transaksi WHERE EXTRACT(MONTH FROM tanggal) = {bulan}"
            kursor.execute(query)
            data_transaksi = kursor.fetchall()
            if data_transaksi:
                print(f"Berikut adalah laporan transaksi bulan {bulan}:")
                print(tabulate(data_transaksi, headers="keys", tablefmt="fancy_grid"))
            else:
                print(f"Tidak ada transaksi bulan {bulan} yang tersedia")
        elif pilihan == "4":
            minggu = input("Masukkan minggu (1-4) : ")
            bulan = input("Minggu pada bulan berapa? (1-12) : ")
            query = f"SELECT * FROM transaksi WHERE EXTRACT(WEEK FROM tanggal) = {minggu} AND EXTRACT(MONTH FROM tanggal) = {bulan}"
            kursor.execute(query)
            data_transaksi = kursor.fetchall()
            if data_transaksi:
                print(f"Berikut adalah laporan transaksi minggu {minggu} bulan {bulan}:")
                print(tabulate(data_transaksi, headers="keys", tablefmt="fancy_grid"))
            else:
                print(f"Tidak ada transaksi minggu {minggu} bulan {bulan} yang tersedia")
        elif pilihan == "5":
            clear_terminal()
            break
        else:
            print("Hanya masukkan (1/2/3/4/5)")
            continue

        if 'hasil' in locals() and hasil:
            total_filtered = sum(row['nominal'] for row in hasil)
            print(f"\nTotal transaksi setelah filter: Rp {total_filtered}")

    kursor.close()
    koneksi.close()

def Help(data_akun):
    koneksi = connect()
    kursor = koneksi.cursor(cursor_factory=RealDictCursor)
    pesan = input("Masukkan pesan yang anda inginkan: ")
    pesan_siap = pesan.replace(" ", "%20").replace("\n", "%0A").replace("\t", "%09")
    print(
    """
    ╔══════════════════════╗
    ║        Admin         ║
    ║┌────────────────────┐║
    ║│                    │║
    ║│  1. Falah          │║
    ║│  2. Rizqi          │║
    ║│  3. Alfin          │║
    ║└────────────────────┘║
    ╚══════════════════════╝
    """)
    while True:
        pillih = input("Dari ketiga admin tersebut pilih salah satu untuk kamu hubungi (1,2,3): ")
        if pillih not in ["1","2","3"]:
            print("Pilihan tidak ada")
            input("Tekan enter untuk memasukkan ulang")
        else:
            break
    try:
        query = "SELECT * FROM akun_admin WHERE id_admin = %s"
        kursor.execute(query, (int(pillih),))
        data_admin = kursor.fetchone()
        url = f"https://wa.me/+{data_admin['no_hp']}?text={pesan_siap}"
        print(f"Silahkan klik link berikut untuk menghubungi admin {data_admin['nama']} : \n{url}")
        input("Tekan enter untuk kembali ke menu utama")
        clear_terminal()
    except Exception as e:
        print(f"Error: {e}")
        input("Tekan enter untuk kembali ke menu utama")
        clear_terminal()
    finally:
        kursor.close()
        koneksi.close()

def TampilkanKatalog(role):
    koneksi = connect()
    syntax = koneksi.cursor(cursor_factory=RealDictCursor)
    try:
        while True:
            clear_terminal()
            query = """
                        SELECT nama AS "Nama", harga AS "Harga", stok AS "Stok", disewakan 
                        FROM produk 
                        ORDER BY id_produk
                    """
            syntax.execute(query)
            katalog_semua = syntax.fetchall()
            print(tabulate(katalog_semua, headers="keys", tablefmt="fancy_grid"))
            if role != 'admin':
                while True:
                    tanya = input("Apakah anda ingin melihat produk berdasarkan kategori? (y/n) : ")
                    if tanya.lower() == 'y':
                        kategori = input("Masukkan kategori (souvenir/dekorasi/mahar/teserahan): ").strip().lower()
                        query = """
                            SELECT nama AS "Nama", harga AS "Harga", stok AS "Stok", disewakan 
                            FROM produk 
                            WHERE id_kategori = (SELECT id_kategori FROM kategori WHERE kategori = %s)
                            ORDER BY id_produk
                        """
                        syntax.execute(query, (kategori,))
                        katalog_kategori = syntax.fetchall()
                        print(tabulate(katalog_kategori, headers="keys", tablefmt="fancy_grid"))
                    elif tanya.lower() == 'n':
                        input("Tekan enter untuk kembali ke menu utama")
                        clear_terminal()
                        return
            else:
                while True:
                    print(
                """
                ╔══════════════════════════════════╗
                ║         Tampilkan Produk         ║
                ║┌────────────────────────────────┐║
                ║│    1. Semua Produk             │║
                ║│    2. Berdasarkan Kategori     │║
                ║└────────────────────────────────┘║
                ╚══════════════════════════════════╝
                """)
                    pilihan_tampil = input("Pilih opsi (1/2): ")
                    if pilihan_tampil == '2':
                        kategori = input("Masukkan kategori (souvenir/dekorasi/mahar/seserahan): ").strip().lower()
                        query = """
                                SELECT nama AS "Nama", harga AS "Harga", stok AS "Stok", disewakan 
                                FROM produk 
                                WHERE id_kategori = (SELECT id_kategori FROM kategori WHERE kategori = %s)
                                ORDER BY id_produk
                            """
                        syntax.execute(query, (kategori,))
                    else:
                        query = """
                            SELECT nama AS "Nama", harga AS "Harga", stok AS "Stok", disewakan 
                            FROM produk 
                            ORDER BY id_produk
                        """
                        syntax.execute(query)
                    data = syntax.fetchall()
                    if data:
                        print(f"Berikut adalah katalog produk:")
                        print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
                    else:
                        print(f"Tidak ada produk dengan kategori {kategori} yang tersedia")
                    if role == 'admin':
                        print(
            """
            ╔══════════════════════════════════╗
            ║           Kelola Barang          ║
            ║┌────────────────────────────────┐║
            ║│                                │║
            ║│  1. Tambah Barang              │║
            ║│  2. Ubah Barang                │║
            ║│  3. Hapus Barang               │║
            ║│  4. Tampilkan Ulang            │║
            ║│  5. Kembali                    │║
            ║└────────────────────────────────┘║
            ╚══════════════════════════════════╝""") 
                        pilihan_admin = input("Pilih program (1/2/3/4/5): ").strip()
                        if pilihan_admin == '5':
                            clear_terminal()
                            return
                        elif pilihan_admin in ['1', '2', '3']:
                            kuasaAdmin(pilihan_admin)
                        elif pilihan_admin == '4':
                            clear_terminal()
                            continue
                        else:
                            print("Input tidak valid.")
                            input("Tekan enter untuk coba lagi...")
                    else:
                        input("\nTekan enter untuk kembali ke menu utama...")
                        clear_terminal()
                        return
    except Exception as e:
        print("Gagal menampilkan katalog")
        print(e)
    finally:
        syntax.close()
        koneksi.close()

def Menu(role,data_akun):
    w = "\033[96m"
    e = "\033[0m"
    while True:
        banner()
        b = 138
        print(f"{w}╔══════════════════════════════════╗{e}".center(b))
        print(f"{w}║{e}         Cantiknya Mahar          {w}║{e}".center(b+8))
        print(f"{w}║┌────────────────────────────────┐║{e}".center(b))
        if role != 'admin':
                print(f"{w}║│                                │║{e}".center(b))
                print(f"{w}║│{e}  1. Tampilkan Katalog          {w}│║{e}".center(b+8)) 
                print(f"{w}║│{e}  2. Pembelian & Penyewaan      {w}│║{e}".center(b+8))
                print(f"{w}║│{e}  3. Pengembalian               {w}│║{e}".center(b+8))
                print(f"{w}║│{e}  4. Keranjang                  {w}│║{e}".center(b+8))
                print(f"{w}║│{e}  5. Riwayat Transaksi          {w}│║{e}".center(b+8))
                print(f"{w}║│{e}  6. Informasi Akun             {w}│║{e}".center(b+8))
                print(f"{w}║│{e}  7. Help                       {w}│║{e}".center(b+8))
                print(f"{w}║│{e}  8. Kembali                    {w}│║{e}".center(b+8))
                print(f"{w}║├────────────────────────────────┤║{e}".center(b))
                print(f"{w}║│{e}           Menu User            {w}│║{e}".center(b+8))
                print(f"{w}║└────────────────────────────────┘║{e}".center(b))
        else:
                print(f"{w}║│                                │║{e}".center(b))
                print(f"{w}║│{e}  1. Kelola Produk              {w}│║{e}".center(b+8))
                print(f"{w}║│{e}  2. Laporan Transaksi          {w}│║{e}".center(b+8))
                print(f"{w}║│{e}  3. Barang di Sewa             {w}│║{e}".center(b+8))
                print(f"{w}║│{e}  4. Riwayat Transaksi          {w}│║{e}".center(b+8))
                print(f"{w}║│{e}  5. Info Akun                  {w}│║{e}".center(b+8))
                print(f"{w}║│{e}  6. Kembali                    {w}│║{e}".center(b+8))
                print(f"{w}║├────────────────────────────────┤║{e}".center(b))
                print(f"{w}║│{e}           Menu Admin           {w}│║{e}".center(b+8))
                print(f"{w}║└────────────────────────────────┘║{e}".center(b))
        print(f"{w}╚══════════════════════════════════╝{e}".center(b) ) 
        
        if role == "customer":
                pilihan = input("Menu yang dipilih : ")
                match pilihan:
                    case "1":
                        TampilkanKatalog(role)
                    case "2":
                        JualSewa(data_akun)
                    case "3":
                        Pengembalian(data_akun)
                    case "4":
                        Keranjang(data_akun)
                    case "5":
                        RiwayatTransaksi(role,data_akun)
                    case "6":
                        InformasiAkun(role,data_akun)
                    case "7":
                        Help(data_akun)
                    case "8":
                        clear_terminal()
                        break
                    case _:
                        clear_terminal()
                        print("Menu tidak sesuai")
        else:
            pilihan = input("Menu yang dipilih : ")
            match pilihan:
                case "1":
                    TampilkanKatalog(role)
                case "2":
                    LaporanTransaksi()
                case "3":
                    AccPenyewaan()
                case "4":
                    RiwayatTransaksi(role,data_akun)
                case "5":
                    InformasiAkun(role,data_akun)
                case "6":
                    clear_terminal()
                    break
                case _:
                    clear_terminal()
                    print("Menu tidak sesuai")
while True:
    clear_terminal()
    print("Selamat datang di Cantiknya Mahar")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    pilihan = input("Pilih program : ")
    if pilihan == '1':
        register()
    elif pilihan == '2':
        login()
    elif pilihan == '3':
        break
    else:
        print("Hanya masukkan (1/2/3)")