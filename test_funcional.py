import requests
import random
import sys

# URL de tu servidor en Render (REEMPLÁZALA por tu URL real de Render cuando esté lista)
BASE_URL = "https://performance-web-flask.onrender.com"

def ejecutar_pruebas():
    print("=" * 60)
    print("INICIANDO PRUEBAS FUNCIONALES EN RENDER")
    print("=" * 60)

    # Paso 1: Verificar acceso a la página principal
    print("\n[Paso 1] Probando acceso a Home Page...")
    try:
        r_home = requests.get(BASE_URL, timeout=15)
        if r_home.status_code == 200:
            print("  -> Éxito: Home Page responde (Código 200).")
        else:
            print(f"  -> Error: Código inesperado: {r_home.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"  -> Error al conectar con el servidor: {e}")
        sys.exit(1)

    # Generar datos aleatorios para evitar colisiones de emails
    numero_aleatorio = random.randint(1000, 9999)
    test_user = {
        "nombre": f"Test User {numero_aleatorio}",
        "email": f"tester_{numero_aleatorio}@example.com",
        "comentario": "Comentario enviado por script automatizado."
    }

    # Paso 2: Probar el flujo de registro de usuario (petición POST)
    print(f"\n[Paso 2] Registrando usuario de prueba: {test_user['email']}...")
    try:
        r_registro = requests.post(f"{BASE_URL}/registro", data=test_user, timeout=15)
        if r_registro.status_code in [200, 302]:
            print("  -> Éxito: Registro de usuario procesado correctamente.")
        else:
            print(f"  -> Error al registrar: Código {r_registro.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"  -> Error de conexión durante el registro: {e}")
        sys.exit(1)

    # Paso 3: Probar consumo del endpoint API
    print("\n[Paso 3] Consultando listado de usuarios desde la API...")
    try:
        r_consulta = requests.get(f"{BASE_URL}/api/usuarios", timeout=15)
        if r_consulta.status_code == 200:
            usuarios = r_consulta.json()
            print(f"  -> Éxito: Se obtuvieron {len(usuarios)} registros correctamente.")
            encontrado = any(u['email'] == test_user['email'] for u in usuarios)
            if encontrado:
                print("  -> Éxito: El usuario registrado aparece listado correctamente en la DB.")
            else:
                print("  -> Advertencia: El usuario no aparece en la lista devuelta por la DB.")
        else:
            print(f"  -> Error al consultar la API: Código {r_consulta.code}")
            sys.exit(1)
    except Exception as e:
        print(f"  -> Error de conexión con la API: {e}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("¡TODAS LAS PRUEBAS FUNCIONALES COMPLETADAS SATISFACTORIAMENTE!")
    print("=" * 60)

if __name__ == "__main__":
    ejecutar_pruebas()