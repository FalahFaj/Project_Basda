import psycopg2

def connect():
    try:
        return psycopg2.connect("dbname='Cantiknya Mahar' user='postgres' host='125.161.165.56' password= 'ns4dpn'port='5432'")
    except Exception as e:
        print("Koneksi Gagal")
        print(e)