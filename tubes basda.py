from koneksiDB import connect
from psycopg2.extras import RealDictCursor
from tabulate import tabulate
import os
import pyfiglet
import datetime as dt

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
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
    print(f"\033[96m",pyfiglet.figlet_format(apa, font='small'),f"\033[0m")

def register():
    koneksi = connect()
    syntax = koneksi.cursor()
    nama = input("Masukkan nama : ")
    no_hp = input("Masukkan nomor hp : ")
    username = input("Masukkan username : ")
    password = input("Masukkan password : ")
    email = input("Masukkan alamat email : ")
    while True:
        try:
            query = f"INSERT INTO customer (nama, no_hp, username, password, email_address) VALUES ({nama},{no_hp},{username},{password},{email})"
            syntax.execute(query)
            koneksi.commit()
            print("Data berhasil disimpan")
            input("Tekan enter untuk melanjutkan")
            clear_terminal()
            break
        except Exception as e:
            print("Data gagal disimpan")
            print(e)
            print("Silahkan coba lagi")
            print("Apakah anda ingin mendaftar lagi? (y/n)")
            pilihan = input("Pilih program : ")
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
            else:
                print("Username atau password salah")
        except Exception as e:
            print("Login gagal")
            print(e)
        finally:
            syntax.close()
            koneksi.close()
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
            else:
                print("Username atau password salah")
        except Exception as e:
            print("Login gagal")
            print(e)
        finally:
            syntax.close()
            koneksi.close()

def kuasaAdmin(pilihan):
    koneksi = connect()
    syntax = koneksi.cursor()
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
                    query = "SELECT * FROM produk WHERE id_produk = %s"
                    syntax.execute(query, (produk,))
                except ValueError:
                    query = "SELECT * FROM produk WHERE nama ILIKE %s"
                    syntax.execute(query, (f"%{produk}%"))
                try:
                    data = syntax.fetchone()
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
                    print(f"Nama Produk Lama : {data['nama']}")
                    print(f"Nama Produk Baru : {nama}")
                    konfirmasi = input("\nSimpan Perubahan? (y/n) : ").lower()
                    if konfirmasi == 'y':
                        try:
                            query = "UPDATE produk SET nama = %s WHERE id_produk = %s"
                            syntax.execute(query, (nama, data["id_produk"]))
                            koneksi.commit()
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
                    print(f"Harga Produk Lama : {data['harga']}")
                    print(f"Harga Produk Baru : {harga}")
                    konfirmasi = input("\nSimpan Perubahan? (y/n) : ").lower()
                    if konfirmasi == 'y':
                        query = f"UPDATE produk SET harga={harga} WHERE id={produk} OR nama='{produk}'"
                        syntax.execute(query)
                        koneksi.commit()
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
                    print(f"Stok Produk Lama : {data['stok']}")
                    print(f"Stok Produk Baru : {data['stok'] + stok}")
                    konfirmasi = input("\nSimpan Perubahan? (y/n) : ").lower()
                    if konfirmasi == 'y':   
                        try:
                            query = "UPDATE produk SET stok = %s WHERE id_produk = %s"
                            syntax.execute(query, (data["stok"]+stok, data["id_produk"]))
                            koneksi.commit()    
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
                    print(f"Kategori Produk Lama : {data['kategori']}")
                    print(f"Kategori Produk Baru : {kategori}")
                    konfirmasi = input("\nSimpan Perubahan? (y/n) : ").lower()
                    if konfirmasi == 'y':
                        query = "UPDATE produk SET kategori = %s WHERE id_produk = %s"
                        syntax.execute(query, (data_kategori["id_kategori"], data["id_produk"]))
                        koneksi.commit()
                        print("Kategori berhasil diubah")
                        input("Tekan enter untuk melanjutkan")
                        clear_terminal()
                    else:
                        print("Perubahan dibatalkan")
                        input("Tekan enter untuk melanjutkan")
                        clear_terminal()
                elif pilihan == '5':
                    clear_terminal()
                    break
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
                    query = "SELECT * FROM produk WHERE id_produk = %s"
                    syntax.execute(query, (id_produk,))
                except ValueError:
                    query = "SELECT * FROM produk WHERE nama ILIKE %s"
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

def Beli(data_produk,data_akun,jumlah):
    koneksi = connect()
    kursor = koneksi.cursor(cursor_factory=RealDictCursor)
    try:
        query = f"SELECT * FROM keranjang Where id_customer={data_akun['id_customer']}"
        kursor.execute(query)
        data_keranjang = kursor.fetchall()

        total_harga = 0
        daftar_pembelian = []

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

            else:
                harga = data_produk['harga'] * int(jumlah)
                daftar_pembelian.append({
                    'id_produk': data_produk['id_produk'],
                    'nama': data_produk['nama'],
                    'harga': data_produk['harga'],
                    'jumlah': jumlah
                })
                total_harga = harga

        else:
            harga = data_produk['harga'] * int(jumlah)
            daftar_pembelian.append({
                'id_produk': data_produk['id_produk'],
                'nama': data_produk['nama'],
                'harga': data_produk['harga'],
                'jumlah': jumlah})
            total_harga = harga

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
            metode_pembayaran = input("Pilih metode pembayaran : ")
            match metode_pembayaran:
                case "1":
                    metode_pembayaran = "Bank BRI"
                case "2":
                    metode_pembayaran = "Bank BCA"
                case "3":
                    metode_pembayaran = "Shopee Pay"
                case "4":
                    metode_pembayaran = "Dana"
                case "5":
                    metode_pembayaran = "Cash"
                case "6":
                    clear_terminal()
                case _:
                    print("Metode pembayaran tidak valid, silahkan coba lagi")
        for item in daftar_pembelian:
            query = f"INSERT INTO transaksi (tanggal, nominal, id_produk, id_customer, id_metode_pembayaran, id_penyewaan) VALUES (%s, %s, %s, %s, %s))"
            kursor.execute(query,(
                tanggal,
                item['harga'] * int(item['jumlah']),
                item['id_produk'],
                data_akun['id_customer'],
                data_metode[0]['id_metode_pembayaran']
            ))
            koneksi.commit()
            query = f"UPDATE produk SET stok=stok-{item['jumlah']} WHERE id_produk={item['id_produk']}"
            kursor.execute(query)
            koneksi.commit()
        print("Pembelian berhasil")
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

def ChatWa(data_akun,data_produk,jumlah,data_metode,data_penyewaan,teks):
    link = "https://wa.me/6287863306466?text="
    pesan = (
        "Halo admin Cantiknya Mahar, saya ingin melakukan penyewaan produk berikut:\n"
        f"Id Penyewaan \t: {data_penyewaan['id_penyewaan']}\n"
        f"Nama Customer \t : {data_akun['nama']}\n"
        f"Nama Produk \t : {data_produk['nama']}\n"
        f"Jumlah Produk \t : {jumlah}\n"
        f"Jumlah dp \t : {data_penyewaan['pembayaran_dp']}\n"
        f"Tanggal Penyewaan \t : {data_penyewaan['tanggal_sewa']}\n"
        f"Tanggal Kembali \t : {data_penyewaan['tanggal_kembali']}\n"
        f"Metode Pembayaran \t : {data_metode[0]['metode_pembayaran']}\n"
        f"{teks}\n"
    )
    pesan = pesan.replace(" ", "%20").replace("\n", "%0A").replace("\t", "%09")
    return link + pesan
    
def Sewa(data_akun,data_produk,jumlah):
    koneksi = connect()
    kursor = koneksi.cursor(cursor_factory=RealDictCursor)
    if data_akun['id_alamat'] == None:
        print("Silahkan lengkapi data alamat anda terlebih dahulu")
        return
    while True:
        if int(jumlah) > data_produk['stok']:
            print("Jumlah produk yang ingin disewa melebihi stok yang tersedia")
        elif int(jumlah) <= 0:
            print("Jumlah produk yang ingin disewa tidak valid")
        else:
            break
    try:
        tanggal = dt.datetime.now()
        query = f"SELECT * FROM metode_pembayaran"
        kursor.execute(query)
        data_metode = kursor.fetchall()
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
            metode_pembayaran = input("Pilih metode pembayaran : ")
            match metode_pembayaran:
                case "1":
                    metode_pembayaran = "Bank BRI"
                case "2":
                    metode_pembayaran = "Bank BCA"
                case "3":
                    metode_pembayaran = "Shopee Pay"
                case "4":
                    metode_pembayaran = "Dana"
                case "5":
                    metode_pembayaran = "Cash"
                case "6":
                    clear_terminal()
                case _:
                    print("Metode pembayaran tidak valid, silahkan coba lagi")
        query = f"UPDATE produk SET stok=stok-{jumlah} WHERE id_produk ={data_produk['id_produk']}"
        kursor.execute(query)
        koneksi.commit()
        tanggal_penyewaan = input("Masukkan tanggal penyewaan (YYYY-MM-DD) : ")
        tanggal_kembali = input("Masukkan tanggal kembali (YYYY-MM-DD) : ")
        biaya_sewa = (data_produk['harga']//50/100) * int(jumlah)
        pembayaran_dp = input(f"Masukkan pembayaran dp jumlah dp sebesar {biaya_sewa} : ")
        while True:
            if int(pembayaran_dp) < biaya_sewa:
                print(f"Jumlah dp kurang dari {biaya_sewa}")
            elif int(pembayaran_dp) <= 0:
                print("Jumlah dp tidak valid")
            else:
                break
        query = f"INSERT INTO penyewaan (tanggal_sewa, tanggal_kembali, pembayaran_dp, status_dp, status_peminjaman, id_produk, id_customer, id_metode_pembayaran) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        kursor.execute(query,(
            tanggal_penyewaan,
            tanggal_kembali,
            pembayaran_dp,
            'belum dibayarkan',
            'masih proses',
            data_produk['id_produk'],
            data_akun['id_customer'],
            data_metode[0]['id_metode_pembayaran']
        ))
        koneksi.commit()
        query = f"SELECT * FROM penyewaan"
        kursor.execute(query)
        data_penyewaan = kursor.fetchall()
        query = f"INSERT INTO transaksi (tanggal, nominal, id_produk, id_customer, id_metode_pembayaran, id_penyewaan) VALUES (%s, %s, %s, %s, %s, %s))"
        tanggal = dt.datetime.now()
        kursor.execute(query,(
                tanggal,
                data_produk['harga'] * int(jumlah),
                data_produk['id_produk'],
                data_akun['id_customer'],
                data_metode[0]['id_metode_pembayaran'],
                data_penyewaan[0]['id_penyewaan']
                ))
        koneksi.commit()
        input("Tekan enter untuk mengenerate link whatsapp")
        url = ChatWa(data_akun,data_produk,jumlah,data_metode,data_penyewaan[0],"\nSaya ingin menghubungi admin untuk konfirmasi penyewaan, Mohon untuk diacc")
        print(f"Silahkan klik link berikut untuk menghubungi admin : \n{url}")
        input("Tekan enter untuk melanjutkan")
        clear_terminal()
    except Exception as e:
        print("Penyewaan gagal")
        print(e)
        print("Silahkan coba lagi")
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
        kursor.execute(query)
        data = kursor.fetchall()
        if data:
            print("Berikut adalah informasi akun customer:")
            print(f"Nama Customer \t: {data[0]['nama']}")
            print(f"No HP Customer \t: {data[0]['no_hp']}")
            print(f"Username Customer \t: {data[0]['username']}")
            print(f"Password Customer \t: {data[0]['password']}")
            print(f"Email Customer \t: {data[0]['email_address']}")
            if data[0]['id_alamat'] != None:
                query = "SELECT * FROM alamat WHERE id_alamat = %s"
                kursor.execute(query, (data[0]['id_alamat'],))
                data_alamat = kursor.fetchall()
                if data_alamat:
                    print(f"""Alamat : {data_alamat['provinsi']},{data_alamat['kecamatan']},
                          {data_alamat['desa']},{data_alamat['dusun']},{data_alamat['rw']}/{data_alamat[rt]}""")
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

def Keranjang(data):
    koneksi = connect()
    kursor = koneksi.cursor(cursor_factory=RealDictCursor)
    query = f"SELECT * FROM keranjang WHERE id_customer={data['id_customer']}"
    kursor.execute(query)
    data_keranjang = kursor.fetchall()
    if data_keranjang:
        print("Berikut adalah keranjang belanja anda:")
        print(tabulate(data_keranjang, headers="keys", tablefmt="fancy_grid"))
        tanya = input("Apakah anda ingin lanjut ke pembelian? (y/n) : ")
        if tanya.lower() == 'y':
            tanya = input("Anda inngin membeli salah satu produk atau semua produk? (s/a) : ")
            if tanya.lower() == 's':
                produk = input("Masukkan id/nama produk yang ingin dibeli : ")
                try:
                    id_produk = int(produk) 
                    query = "SELECT * FROM produk WHERE id_produk = %s"
                    kursor.execute(query, (id_produk,))
                except ValueError:
                    query = "SELECT * FROM produk WHERE nama ILIKE %s"
                    kursor.execute(query, (f"%{produk}%",))
                while True:
                    try:
                        data_produk = kursor.fetchone()
                        if data_produk:
                            print("Berikut adalah data produk yang ingin dibeli:")
                            print(tabulate(data_produk, headers="keys", tablefmt="fancy_grid"))
                            Beli(data_produk)
                            clear_terminal()
                            break
                        else:
                            print("Produk tidak ditemukan")
                            break
                    except Exception as e:
                        print("Gagal menampilkan data produk")
                        print(e)
            elif tanya.lower() == 'a':
                query = f"SELECT * FROM produk WHERE id IN (SELECT id_produk FROM keranjang WHERE id_customer={data['id_customer']})"
                kursor.execute(query)
                data_produk = kursor.fetchall()
                if data_produk:
                    print("Berikut adalah data produk yang ingin dibeli:")
                    print(tabulate(data_produk, headers="keys", tablefmt="fancy_grid"))
                else:
                    print("Tidak ada produk yang tersedia")
        print("Silahkan pilih produk yang ingin dibeli")


def JualSewa(data_akun):
    koneksi = connect()
    kursor = koneksi.cursor(cursor_factory=RealDictCursor)
    query = "SELECT * FROM produk"
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
                query = "SELECT * FROM produk WHERE id_produk = %s"
                kursor.execute(query, (id_produk,))
            except ValueError:
                query = "SELECT * FROM produk WHERE nama ILIKE %s"
                kursor.execute(query, (f"%{keyword}%",))
            try:
                data_produk = kursor.fetchall()
                if data_produk:
                    print("Berikut adalah data produk yang ingin dibeli/disewa:")
                    print(tabulate(data_produk, headers="keys", tablefmt="fancy_grid"))
                    break
                else:
                    print("Produk tidak ditemukan")
                    print("Silahkan coba lagi")
            except Exception as e:
                print("Gagal menampilkan data produk")
                print(e)
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
                jumlah = input("Masukkan jumlah produk yang ingin dibeli : ")
                while True:
                    if int(jumlah) > data_produk['stok']:
                        print("Jumlah produk yang ingin dibeli melebihi stok yang tersedia")
                    elif int(jumlah) <= 0:
                        print("Jumlah produk yang ingin dibeli tidak valid")
                    else:
                        break
                Beli(data_produk,data_akun,jumlah)
                clear_terminal()
            elif pilihan == '2':
                if data_produk['disewakan'] == False:
                    print("Produk tidak tersedia untuk disewa")
                    input("Tekan enter untuk melanjutkan")
                    clear_terminal()
                    break
                jumlah = input("Masukkan jumlah produk yang ingin disewa : ")
                while True:
                    if int(jumlah) > data_produk['stok']:
                        print("Jumlah produk yang ingin disewa melebihi stok yang tersedia")
                    elif int(jumlah) <= 0:
                        print("Jumlah produk yang ingin disewa tidak valid")
                    else:
                        break
                Sewa(data_produk,data_akun,jumlah)
                clear_terminal()
            elif pilihan == '3':
                try:
                    while True:
                        jumlah = input("Masukkan jumlah produk yang ingin dimasukkan ke keranjang : ")
                        if int(jumlah) > data_produk['stok']:
                            print("Jumlah produk yang ingin dimasukkan ke keranjang melebihi stok yang tersedia")
                        else:
                            break
                    query = f"INSERT INTO keranjang (id_produk, id_customer, jumlah) VALUES ({data_produk['id_produk']}, {data_akun ['id_customer']}, {jumlah})"
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
    koneksi = connect()
    kursor = koneksi.cursor(cursor_factory=RealDictCursor)
    query = f"SELECT * FROM penyewaan WHERE id_customer={data_akun['id_customer']}"
    kursor.execute(query)
    data_penyewaan = kursor.fetchall()
    query = f"SELECT * FROM produk WHERE id_produk = {data_penyewaan[0]['id_produk']})"
    kursor.execute(query)
    data_produk = kursor.fetchall()
    if data_penyewaan[0]['status_peminjaman'] == 'dipinjam':
        print("Berikut adalah data barang yang anda sewa : ")
        print(tabulate(data_penyewaan, headers="keys", tablefmt="fancy_grid"))
        tanya = input("Apakah anda ingin mengembalikan barang? (y/n) : ")
        if tanya.lower() == 'y':
            try:
                query = f"UPDATE penyewaan SET status_peminjaman = 'dikembalikan' WHERE id_customer={data_akun['id_customer']}"
                kursor.execute(query)
                koneksi.commit()
                print(f"Barang {data_produk[0]['nama']} berhasil dikembalikan")
                input("Tekan enter untuk melanjutkan")
                # clear_terminal()
            except Exception as e:
                print("Barang gagal dikembalikan")
                print(e)
                print("Silahkan coba lagi")
                input("Tekan enter untuk melanjutkan")
                # clear_terminal()
        masih_proses = input("Apakah anda ingin melihat barang yang masih dalam proses penyewaan? (y/n) : ")
        if masih_proses.lower() == 'y':
            query = f"SELECT * FROM penyewaan WHERE id_customer={data_akun['id_customer']} AND status_peminjaman='masih proses'"
            kursor.execute(query)
            data_penyewaan = kursor.fetchall()
            query = f"SELECT * FROM produk WHERE id_produk = {data_penyewaan[0]['id_produk']})"
            kursor.execute(query)
            data_produk = kursor.fetchone()
            query = f"SELECT * FROM metode_pembayaran WHERE id_metode_pembayaran = {data_penyewaan[0]['id_metode_pembayaran']}"
            kursor.execute(query)
            data_metode = kursor.fetchall()
            if data_penyewaan:
                print("Berikut adalah barang yang masih dalam proses penyewaan:")
                print(tabulate(data_penyewaan, headers="keys", tablefmt="fancy_grid"))
                chat = input("Apakah anda mau menghubungi admin untuk mempercepat proses penyewaan? (y/n) : ")
                if chat.lower() == 'y':
                    pesan = input("Masukkan pesan yang ingin disampaikan ke admin : ")
                    url = ChatWa(data_akun,data_produk,data_penyewaan[0]['jumlah'],data_metode,data_penyewaan[0], pesan)
                    print(f"Silahkan klik link berikut untuk menghubungi admin : \n{url}")
                    input("Tekan enter untuk melanjutkan")
                    clear_terminal()
            else:
                print("Tidak ada barang yang masih dalam proses penyewaan")
    else:
        print("Tidak ada barang yang disewa")
        input("Tekan enter untuk melanjutkan")
        clear_terminal()
                

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
    query = f"SELECT * FROM transaksi"
    kursor.execute(query)
    data_transaksi = kursor.fetchall()
    query = f"SELECT * FROM penyewaan"
    kursor.execute(query)
    data_penyewaan = kursor.fetchall()
    if role == 'admin':
        if data_transaksi:
            query = f"""SELECT t.tanggal AS 'Tanggal', 
            t.Nominal AS 'Nominal', 
            p.status_peminjaman AS 'Status Peminjaman' 
            FROM transaksi t 
            FULL JOIN penyewaan p ON t.{data_transaksi['id_penyewaan']} = p.{data_penyewaan['id_penyewaan']}"""
            kursor.execute(query)
            data_transaksi = kursor.fetchall()
            print("Berikut adalah riwayat transaksi:")
            print(tabulate(data_transaksi, headers="keys", tablefmt="fancy_grid"))
            input("Tekan enter untuk kembali")
            clear_terminal()
        else:
            print("Tidak ada riwayat transaksi yang tersedia")
            input("Tekan enter untuk kembali ke menu")
            clear_terminal()
    elif role == 'customer':
        query = f"SELECT t.tanggal AS 'Tanggal', t.Nominal AS 'Nominal', p.status_peminjaman AS 'Status Peminjaman' FROM transaksi t FULL JOIN penyewaan p ON t.{data_transaksi['id_penyewaan']} = p.{data_penyewaan['id_penyewaan']} WHERE t.id_customer = t.{data_akun['id_customer']}"
        kursor.execute(query)
        data_penyewaan = kursor.fetchall()
        if data_penyewaan:
            print("Berikut adalah riwayat transaksi:")
            print(tabulate(data_penyewaan, headers="keys", tablefmt="fancy_grid"))
            input("Tekan enter untuk kembali")
            clear_terminal()
        else:
            print("Tidak ada riwayat transaksi yang tersedia")
            input("Tekan enter untuk kembali ke menu")
            clear_terminal()

def AccPenyewaan():
    koneksi = connect()
    kursor = koneksi.cursor(cursor_factory=RealDictCursor)
    query = f"SELECT * FROM penyewaan WHERE status_peminjaman='masih proses'"
    kursor.execute(query)
    data_penyewaan = kursor.fetchall()
    if data_penyewaan:
        print("Berikut adalah daftar penyewaan yang masih dalam proses:")
        print(tabulate(data_penyewaan, headers="keys", tablefmt="fancy_grid"))
        id_penyewaan = int(input("Masukkan id penyewaan yang ingin di acc atau ditolak : "))
        query = f"SELECT * FROM penyewaan WHERE id_penyewaan={id_penyewaan}"
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
                query = f"SELECT * FROM customer WHERE id_customer={data_satu_penyewaan['id_customer']}"
                kursor.execute(query)
                data_customer = kursor.fetchone()
                nomor_hp = data_customer['no_hp']
                query = f"SELECT * FROM produk WHERE id_produk={data_satu_penyewaan['id_produk']}"
                kursor.execute(query)
                data_produk = kursor.fetchone()
                print(f"Silahkan klik link berikut untuk menghubungi customer : \nwa.me/+{nomor_hp}?text=Halo%20saya%20ingin%20menanyakan%20status%20penyewaan%20yang%20{data_customer['nama']}%20ajukan%20terhadap%20produk%20{data_produk['nama']}%20dengan%20id%20penyewaan%20{data_satu_penyewaan['id_penyewaan']}")
                input("Tekan enter untuk melanjutkan")
            elif pilihan == '4':
                clear_terminal()
            else:
                print("Hanya masukkan (1/2/3/4)")
        tanya = input("Apakah anda ingin mengacc penyewaan? (y/n) : ")
        if tanya.lower() == 'y':
            id_penyewaan = input("Masukkan id penyewaan yang ingin di acc : ")
            query = f"UPDATE penyewaan SET status_peminjaman='dipinjam' WHERE id_penyewaan={id_penyewaan}"
            kursor.execute(query)
            koneksi.commit()
            print(f"Penyewaan dengan id {id_penyewaan} berhasil di acc")
    else:
        print("Tidak ada penyewaan yang masih dalam proses")
        input("Tekan enter untuk melanjutkan")
        clear_terminal()

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
    print(f"Total transaksi: Rp {total['total_transaksi']}\n")
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
            query = f"SELECT * FROM transaksi WHERE id_penyewaan IS NOT NULL"
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
        url = f"https://api.whatsapp.com/send?phone= {data_admin['no_hp']}?text={pesan_siap}"
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
        query = "SELECT nama as 'Nama', harga as 'Harga', stok as 'Stok', disewakan FROM produk"
        syntax.execute(query)
        data = syntax.fetchall()
        if data:
            print("Berikut adalah katalog semua produk:")
            print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
            tanya = input("Apakah anda ingin melihat produk berdasarkan kategori? (y/n) : ")
            if tanya.lower() == 'y':
                kategori_produk()
            else:
                input("Tekan enter untuk kembali ke menu utama")
                clear_terminal()
                return
        else:
            print("Tidak ada produk yang tersedia")
    except Exception as e:
        print("Gagal menampilkan katalog")
        print(e)
    finally:
        syntax.close()
        koneksi.close()
    if role == 'admin':
        while True:
            print(
"""
╔══════════════════════════════════╗
║           Kelola Barang          ║
║┌────────────────────────────────┐║""")
            print("║│                                │║")
            print("║│  1. Tambah Barang              │║")
            print("║│  2. Ubah Barang                │║")
            print("║│  3. Hapus Barang               │║")
            print("║│  4. Kembali                    │║")
            print("║└────────────────────────────────┘║")
            print("╚══════════════════════════════════╝") 
            while True:   
                pilihan = input("Pilih program : ")
                if pilihan == "4":
                    clear_terminal()
                    break
                elif pilihan == '1' or pilihan == "2" or pilihan == "3":
                    kuasaAdmin(pilihan)
                    break
                else:
                    print("Hanya masukkan (1/2/3/4)")
            break

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
                print(f"{w}║│{e}  4. Riwayat Transaksi          {w}│║{e}".center(b+8))
                print(f"{w}║│{e}  5. Informasi Akun             {w}│║{e}".center(b+8))
                print(f"{w}║│{e}  6. Help                       {w}│║{e}".center(b+8))
                print(f"{w}║│{e}  7. Kembali                    {w}│║{e}".center(b+8))
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
                        RiwayatTransaksi(role,data_akun)
                    case "5":
                        InformasiAkun(role,data_akun)
                    case "6":
                        Help(data_akun)
                    case "7":
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