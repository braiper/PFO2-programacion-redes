import requests

# Dirección IP y puerto donde escucha nuestro servidor Flask
BASE_URL = "http://127.0.0.1:5000"

# Usamos Session() para que el cliente guarde automáticamente la cookie de sesión al hacer login
sesion_cliente = requests.Session()

def menu():
    while True:
        print("\n==========================================")
        print("   CLIENTE DE CONSOLA - GESTIÓN DE TAREAS")
        print("==========================================")
        print("1. Registrar usuario (POST /registro)")
        print("2. Iniciar sesión (POST /login)")
        print("3. Ver tareas / bienvenida (GET /tareas)")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opción (1-4): ").strip()

        try:
            if opcion == "1":
                usuario = input("Ingrese nuevo nombre de usuario: ").strip()
                password = input("Ingrese contraseña: ").strip()
                
                respuesta = sesion_cliente.post(
                    f"{BASE_URL}/registro",
                    json={"usuario": usuario, "contraseña": password}
                )
                print(f"\n[Código HTTP {respuesta.status_code}] Respuesta:", respuesta.json())

            elif opcion == "2":
                usuario = input("Usuario: ").strip()
                password = input("Contraseña: ").strip()
                
                respuesta = sesion_cliente.post(
                    f"{BASE_URL}/login",
                    json={"usuario": usuario, "contraseña": password}
                )
                print(f"\n[Código HTTP {respuesta.status_code}] Respuesta:", respuesta.json())

            elif opcion == "3":
                respuesta = sesion_cliente.get(f"{BASE_URL}/tareas")
                print(f"\n[Código HTTP {respuesta.status_code}]")
                
                if respuesta.status_code == 200:
                    print("Contenido HTML recibido del servidor:\n")
                    print(respuesta.text)
                else:
                    print("Respuesta:", respuesta.json())

            elif opcion == "4":
                print("Cerrando el cliente de consola...")
                break
            else:
                print("\n[!] Opción inválida. Intente nuevamente.")

        except requests.exceptions.ConnectionError:
            print("\n[ERROR] No se pudo conectar con el servidor.")
            print("Asegúrese de que 'servidor.py' esté en ejecución en otra terminal.")

if __name__ == "__main__":
    menu()