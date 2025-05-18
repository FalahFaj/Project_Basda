import psycopg2

def connect():
    try:
        conn = psycopg2.connect("dbname='Cantiknya Mahar' user='postgres' host='125.161.191.47' password= 'ns4dpn'port='5432'")
        print("Koneksi Berhasil")
    except Exception as e:
        print("Koneksi Gagal")
        print(e)

connect()