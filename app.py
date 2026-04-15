from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from database import SessionLocal, engine
from models import ProductosDB, UsuarioDB
from passlib.context import CryptContext
import models
import os
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")

models.Base.metadata.create_all(bind=engine)

# Coneccion a la db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Creacion de la app
app = FastAPI()

# Definicion de esquemas
class UsuarioSchema(BaseModel):
    email: str
    password: str

class ProductoSchema(BaseModel):
    nombre: str
    descripcion: str
    precio:float

# Creacion y verificacion de Tokens
def crear_token(email: str):
    expiracion = datetime.utcnow() + timedelta(hours=24)
    datos = {"sub": email, "exp": expiracion}
    return jwt.encode(datos, SECRET_KEY, algorithm="HS256")

def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token invalido")
        return email
    except:  # noqa: E722
        raise HTTPException(status_code=401, detail="Token invalido")

# Ruta de inicio
@app.get("/")
def inicio():
    return "H"

# Ruta para listar productos
@app.get("/productos")
def listar_productos(db = Depends(get_db), token: str = Depends(verificar_token)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No estás autenticado",
        )
    productos = db.query(ProductosDB).all()
    return productos

# Ruta para crear productos
@app.post("/nuevo_producto")
def crear_nota(producto: ProductoSchema, db = Depends(get_db), Session = Depends(verificar_token)):
    nuevo_producto = ProductosDB(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

@app.put("/actualzar_producto/{id}")
def actualizar(id:int, precio: float, db = Depends(get_db) ,Session = Depends(verificar_token)):
    producto = db.query(ProductosDB).filter(ProductosDB.id == id).first()
    if producto:
        producto.precio = precio
        db.commit()
        db.refresh(producto)
        return "Producto actualizado"
    else:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

# Ruta para eliminar nota
@app.delete("/productos/{id}")
def eliminar_producto(id: int, db = Depends(get_db), token:str = Depends(verificar_token)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No estás autenticado",
        )
    producto = db.query(ProductosDB).filter(ProductosDB.id == id).first()
    if producto:
        db.delete(producto)
        db.commit()
        return "Producto eliminado"
    else:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

# Ruta para registro de usuario
@app.post("/registro")
def crear_usuario(usuario: UsuarioSchema, db = Depends(get_db)):
    password_hasheada = pwd_context.hash(usuario.password)
    nuevo = UsuarioDB(
        email=usuario.email,
        password=password_hasheada
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# Ruta para login de usuario
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    usuario_db = db.query(UsuarioDB).filter(UsuarioDB.email == form_data.username).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not pwd_context.verify(form_data.password, usuario_db.password):
        raise HTTPException(status_code=401, detail="Usuario y clave no coinciden")
    token = crear_token(usuario_db.email)
    return {
        "access_token": token, 
        "token_type": "bearer"
    }