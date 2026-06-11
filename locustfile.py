import random
from locust import HttpUser, task, between

class OperacionesUsuario(HttpUser):
    # Simula un tiempo de espera aleatorio entre 1 y 3 segundos entre cada acción del usuario
    wait_time = between(1, 3)

    @task(3)
    def ver_home_page(self):
        """Simula a un usuario navegando por la Página de Inicio"""
        self.client.get("/")

    @task(2)
    def consultar_usuarios(self):
        """Simula a un usuario ingresando al módulo embebido de visualización de datos"""
        self.client.get("/registro")

    @task(1)
    def registrar_usuario(self):
        """Simula a un usuario completando y enviando el formulario de registro con datos únicos"""
        id_aleatorio = random.randint(100000, 999999)
        datos_registro = {
            "nombre": f"Locust User {id_aleatorio}",
            "email": f"locust_user_{id_aleatorio}@testload.com",
            "comentario": "Registro automático de carga generado por Locust."
        }
        self.client.post("/registro", data=datos_registro)