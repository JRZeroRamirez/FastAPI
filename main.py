from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from typing import List
import csv
import asyncio
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from passlib.hash import bcrypt


app = FastAPI()

# OAuth2PasswordBearer es una clase de FastAPI que maneja la obtención del token de la solicitud
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelo de datos para el usuario
class User(BaseModel):
    id: int
    email: str
    hashed_password: str

# Modelo de datos para la creación de usuario (registro)
class UserCreate(BaseModel):
    email: str
    password: str

# Modelo de datos para la creación de token
class Token(BaseModel):
    access_token: str
    token_type: str

# Modelo de datos para el Cliente
class Cliente(BaseModel):
    id: int
    documento: str
    first_name: str
    last_name: str
    email: str
    password: str

# Modelo de datos para la Factura
class Factura(BaseModel):
    id: int
    client_id: int
    company_name: str
    nit: str
    code: str

# Modelo de datos para el Producto
class Producto(BaseModel):
    id: int
    name: str
    description: str

# Base de datos ficticia para almacenar usuarios
db_users = {}
# Base de datos ficticia para almacenar clientes
db_clientes = {}
# Base de datos ficticia para almacenar facturas
db_facturas = {}
# Base de datos ficticia para almacenar productos
db_productos = {}

# Función para obtener un usuario por su correo electrónico
def get_user(db, email: str):
    if email in db:
        user_dict = db[email]
        return User(**user_dict)

# Ruta para registrar un nuevo usuario
@app.post("/register", response_model=User)
async def register(user: UserCreate):
    if user.email in db_users:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = bcrypt.hash(user.password)
    user_data = {"id": len(db_users) + 1, "email": user.email, "hashed_password": hashed_password}
    db_users[user.email] = user_data
    return User(**user_data)

# Ruta para iniciar sesión y obtener un token
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordBearer = Depends()):
    user = get_user(db_users, form_data.username)
    if user and bcrypt.verify(form_data.password, user.hashed_password):
        return {"access_token": form_data, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Ruta protegida que requiere un token JWT
@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    # Lógica para acceder a la ruta protegida
    return {"message": "Access granted"}

# Ruta para crear un cliente
@app.post("/clientes", response_model=Cliente)
async def create_cliente(cliente: Cliente):
    if cliente.id in db_clientes:
        raise HTTPException(status_code=400, detail="Client ID already exists")
    db_clientes[cliente.id] = cliente
    return cliente

# Ruta para obtener todos los clientes
@app.get("/clientes", response_model=List[Cliente])
async def read_clientes():
    return list(db_clientes.values())

# Ruta para obtener un cliente por ID
@app.get("/clientes/{cliente_id}", response_model=Cliente)
async def read_cliente(cliente_id: int):
    if cliente_id not in db_clientes:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_clientes[cliente_id]

# Ruta para exportar clientes a un archivo CSV
@app.get("/export_clients_csv")
async def export_clients_csv():
    # Lógica para exportar clientes a un archivo CSV (por ejemplo, en segundo plano)
    # Devuelve un archivo CSV con los datos exportados
    headers = ["ID", "Documento", "Nombre Completo", "Cantidad de Facturas"]
    rows = []
    for cliente_id, cliente in db_clientes.items():
        nombre_completo = f"{cliente.first_name} {cliente.last_name}"
        cantidad_facturas = len([f for f in db_facturas.values() if f.client_id == cliente_id])
        rows.append([cliente.id, cliente.documento, nombre_completo, cantidad_facturas])

    async def generate():
        content = f"{','.join(headers)}\n"
        for row in rows:
            content += f"{','.join(map(str, row))}\n"
            await asyncio.sleep(0)  # Para permitir operaciones asincrónicas

        yield content

    return StreamingResponse(generate(), media_type="text/csv", headers={"Content-Disposition": "attachment;filename=clientes.csv"})

# Ruta para cargar clientes desde un archivo CSV
@app.post("/upload_clients_csv")
async def upload_clients_csv(file: UploadFile = File(...)):
    # Lógica para cargar clientes desde un archivo CSV (por ejemplo, en segundo plano)
    # Agrega los clientes a la base de datos ficticia db_clientes
    content = await file.read()
    content = content.decode("utf-8")
    reader = csv.DictReader(content.splitlines())
    for row in reader:
        cliente = Cliente(**row)
        db_clientes[cliente.id] = cliente

    return {"message": "Clientes cargados exitosamente"}

# Ruta para crear una factura
@app.post("/facturas", response_model=Factura)
async def create_factura(factura: Factura):
    if factura.id in db_facturas:
        raise HTTPException(status_code=400, detail="Factura ID already exists")
    db_facturas[factura.id] = factura
    return factura

# Ruta para obtener todas las facturas
@app.get("/facturas", response_model=List[Factura])
async def read_facturas():
    return list(db_facturas.values())

# Ruta para obtener una factura por ID
@app.get("/facturas/{factura_id}", response_model=Factura)
async def read_factura(factura_id: int):
    if factura_id not in db_facturas:
        raise HTTPException(status_code=404, detail="Factura not found")
    return db_facturas[factura_id]

# Ruta para crear un producto
@app.post("/productos", response_model=Producto)
async def create_producto(producto: Producto):
    if producto.id in db_productos:
        raise HTTPException(status_code=400, detail="Producto ID already exists")
    db_productos[producto.id] = producto
    return producto

# Ruta para obtener todos los productos
@app.get("/productos", response_model=List[Producto])
async def read_productos():
    return list(db_productos.values())

# Ruta para obtener un producto por ID
@app.get("/productos/{producto_id}", response_model=Producto)
async def read_producto(producto_id: int):
    if producto_id not in db_productos:
        raise HTTPException(status_code=404, detail="Producto not found")
    return db_productos[producto_id]