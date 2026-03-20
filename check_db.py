import sqlite3
import os

print("🔍 VERIFICANDO BASE DE DATOS")
print("=" * 50)

# Verificar ruta
db_path = "database/landing_page.db"
abs_path = os.path.abspath(db_path)

print(f"📁 Ruta relativa: {db_path}")
print(f"📁 Ruta absoluta: {abs_path}")
print(f"📁 ¿Existe el archivo? {os.path.exists(abs_path)}")

if os.path.exists(abs_path):
    size = os.path.getsize(abs_path)
    print(f"📁 Tamaño: {size} bytes")
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(abs_path)
        cursor = conn.cursor()
        
        # Verificar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n📊 Tablas encontradas: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")
            
            # Contar registros en cada tabla
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
            count = cursor.fetchone()[0]
            print(f"     Registros: {count}")
        
        # Verificar específicamente configuracion_sitio
        cursor.execute("SELECT * FROM configuracion_sitio;")
        config = cursor.fetchone()
        
        if config:
            print(f"\n✅ Datos de configuración encontrados:")
            print(f"   ID: {config[0]}")
            print(f"   Nombre: {config[1]}")
            print(f"   Tagline: {config[2]}")
        else:
            print(f"\n⚠️ No hay datos en configuracion_sitio")
        
        conn.close()
        print(f"\n✅ Conexión exitosa a la base de datos")
        
    except Exception as e:
        print(f"\n❌ Error al conectar: {e}")
else:
    print(f"\n❌ El archivo de base de datos NO existe")
    print("\n📝 Para crear la base de datos:")
    print("1. Abre DBeaver")
    print("2. Crea una nueva conexión SQLite")
    print("3. Guarda el archivo en: database/landing_page.db")
    print("4. Ejecuta el script bd.sql para crear las tablas")

print("\n" + "=" * 50)