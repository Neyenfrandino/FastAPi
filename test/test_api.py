from fastapi.testclient import TestClient
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from app.db.models import Base
from app.hashing import Hash
from app.db.database import get_db
import time

db_path = os.path.join(os.path.dirname(__file__), 'test_db')
db_uri = 'sqlite:///{}'.format(db_path)
SQLALCHEMY_DATABASE_URL = db_uri
engine_test = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
Base.metadata.create_all(bind=engine_test)

from main import app

cliente= TestClient(app)
testingSessionLocal = sessionmaker(bind=engine_test, autocommit=False, autoflush=False)


def override_get_db():

    db = testingSessionLocal()
    try:
        yield db   
    finally:   
        db.close()

app.dependency_overrides[get_db] = override_get_db


def insertar_usuario_prueba():
    db = testingSessionLocal()
    password_hash = Hash.hash_password('prueba123')
    statement = text(
        f"""
        INSERT INTO usuario(username, password, nombre, apellido, direccion, telefono, correo)
        VALUES('prueba', '{password_hash}', 'prueba_nombre', 'prueba_apellido', 'prueba_direcc', 1234, 'Neyen@gmail.com')
        """
    )
    db.execute(statement)
    db.commit()

insertar_usuario_prueba()

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
    assert response.status_code == 401
    usuario_login = {
        'username': 'prueba',
        'password': 'prueba123'
    }

    response_token = cliente.post('/login/', data= usuario_login)
    # print(response_token)
    # print(response_token.json())
    assert response_token.status_code == 200
    assert response_token.json()['token_type'] == 'bearer'

    headers = {
        'Authorization':f"Bearer {response_token.json()['access token']}"
    }

    response = cliente.post('/user/crear_usuario', json=usuario, headers=headers)
    print(response.status_code)
    print(response.json())
    assert response.status_code == 201
    assert response.json()['Respuesta'] == 'Usuario creado exitosamente!!'

def test_obtener_usuarios():
    usuario_login = {
    'username': 'prueba',
    'password': 'prueba123'
    }

    response_token = cliente.post('/login/', data= usuario_login)
    # print(response_token)
    # print(response_token.json())
    assert response_token.status_code == 200
    assert response_token.json()['token_type'] == 'bearer'

    headers = {
        'Authorization':f"Bearer {response_token.json()['access token']}"
    }

    response = cliente.get('/user/', headers=headers)
    print(response.json(), 'response')
    print(len(response.json()))


def test_obtener_usuarios_por_id():
    usuario_login = {
        'username': 'prueba',
        'password': 'prueba123'
    }

    response_token = cliente.post('/login/', data= usuario_login)
    # print(response_token)
    # print(response_token.json())
    assert response_token.status_code == 200
    assert response_token.json()['token_type'] == 'bearer'

    headers = {
        'Authorization':f"Bearer {response_token.json()['access token']}"
    }

    response = cliente.get('/user/1', headers=headers)
    print(response.json())
    assert response.json()['username'] == 'prueba'


# def test_eliminar_usuarios():
#     usuario_login = {
#         'username': 'prueba',
#         'password': 'prueba123'
#     }

#     response_token = cliente.post('/login/', data= usuario_login)
#     # print(response_token)
#     # print(response_token.json())
#     assert response_token.status_code == 200
#     assert response_token.json()['token_type'] == 'bearer'

#     headers = {
#         'Authorization':f"Bearer {response_token.json()['access token']}"
#     }

#     response = cliente.delete('/user/1', headers=headers)
#     print(response.json())
#     assert response.json()['Respuesta'] == 'El usuario a sido eliminado correctamente'

#     response_user = cliente.get('/user/1', headers=headers)
#     print(response_user.json())

#     assert response_user.json()['detail'] == 'No existe el usuario con el id 1'

def test_actualizar_usuarios():
    usuario_login = {
        'username': 'prueba',
        'password': 'prueba123'
    }

    response_token = cliente.post('/login/', data= usuario_login)
    # print(response_token)
    # print(response_token.json())
    assert response_token.status_code == 200
    assert response_token.json()['token_type'] == 'bearer'

    headers = {
        'Authorization':f"Bearer {response_token.json()['access token']}"
    }

    usuario_body = {
        "username": "Prueba_modificar"
        }

    response = cliente.patch('/user/2', json=usuario_body, headers=headers)
    print(response.json())
    assert response.json()['Respuesta'] == 'El usuario ha sido modificado correctamente'
    res = cliente.get('/user/2', headers=headers)
    print(res.json())
    assert res.json()['username'] == 'Prueba_modificar'
    assert res.json()['nombre'] == 'string'
  

def test_delete_database():
    db_path = os.path.join(os.path.dirname(__file__), 'test_db')

    # Cerrar todas las conexiones o sesiones de la base de datos
    engine_test.dispose()

    # Introducir un pequeño retraso antes de intentar eliminar el archivo
    time.sleep(2)

    # Intentar eliminar el archivo
    try:
        os.remove(db_path)
        print(f"Archivo de base de datos eliminado: {db_path}")
    except FileNotFoundError:
        print(f"El archivo de base de datos no existe: {db_path}")
    except Exception as e:
        print(f"Error al eliminar la base de datos: {e}")