from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from main import app

cliente= TestClient(app)

def test_crear_usuario():
    usuario = {
        "username": "nn",
        "password": "nn",
        "nombre": "string",
        "apellido": "string",
        "direccion": "string",
        "telefono": 0,
        "correo": "neyen@gmail.com",
        "creacion": "2023-12-28T09:12:03.423679"
    }
    response = cliente.post('/user/crear_usuario', json=usuario)
    assert response.status_code == 201
    print(response.json())
    pass