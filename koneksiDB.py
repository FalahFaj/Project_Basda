import psycopg2

def connect():
    try:
        return psycopg2.connect("dbname='Cantiknya Mahar' user='postgres' host='serverpostgre.duckdns.org' password= 'ns4dpn'port='5432'")
    except Exception as e:
        print("Koneksi Gagal")
        print(e)