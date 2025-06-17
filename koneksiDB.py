import psycopg2

def connect():
    try:
        return psycopg2.connect("dbname='Cantiknya Mahar' user='postgres' host='serveo.net' password= 'ns4dpn'port='8081'")
    except Exception as e:
        print("Koneksi Gagal")
        print(e)

connect()