# 🛒 Productos API - FastAPI + PostgreSQL + Docker

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Status](https://img.shields.io/badge/status-active-success)

API RESTful para gestión de productos con autenticación JWT, desarrollada con **FastAPI**, **PostgreSQL** y **Docker**.

---

## 🚀 Demo (Deploy)

👉 Producción: *(agregar URL cuando deployes)*
👉 Swagger Docs: `/docs`
👉 ReDoc: `/redoc`

---

## 🧱 Arquitectura

```id="arch1"
FastAPI (API)
   │
   ├── SQLAlchemy (ORM)
   │
   ├── PostgreSQL (DB)
   │
   └── Docker (Infraestructura)
```

---

## ⚙️ Instalación

### 🔹 Opción 1: Docker (Recomendada)

```bash id="docker1"
docker-compose up --build
```

---

### 🔹 Opción 2: Local

```bash id="local1"
pip install -r requirements.txt
uvicorn app:app --reload
```

---

## 🔐 Autenticación (JWT)

### 📌 Registro

`POST /registro`

```json id="reg1"
{
  "email": "user@test.com",
  "password": "1234"
}
```

---

### 📌 Login

`POST /login`

**Content-Type:** `application/x-www-form-urlencoded`

```id="login1"
username=user@test.com
password=1234
```

**Respuesta:**

```json id="login2"
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

---

### 📌 Uso del token

```http id="auth1"
Authorization: Bearer JWT_TOKEN
```

---

## 📚 Endpoints (OpenAPI Ready)

---

### 🟢 Health Check

`GET /`

```json id="h1"
"H"
```

---

### 📦 Productos

---

### 🔹 Obtener todos los productos

`GET /productos`

🔒 Requiere autenticación

**Respuesta:**

```json id="p1"
[
  {
    "id": 1,
    "nombre": "Coca Cola",
    "descripcion": "Botella 2L",
    "precio": 1500
  }
]
```

---

### 🔹 Crear producto

`POST /productos`

🔒 Requiere autenticación

```json id="p2"
{
  "nombre": "Pepsi",
  "descripcion": "Botella 1.5L",
  "precio": 1200
}
```

---

### 🔹 Actualizar precio

`PUT /productos/{id}`

🔒 Requiere autenticación

```http id="p3"
/productos/1?precio=2000
```

---

### 🔹 Eliminar producto

`DELETE /productos/{id}`

🔒 Requiere autenticación

---

## 🧠 Reglas de negocio

* `precio > 0`
* `precio` obligatorio
* Autenticación requerida en endpoints protegidos
* Contraseñas encriptadas con bcrypt

---

## 🧪 Testing

Swagger UI:

👉 http://localhost:8000/docs

Flujo recomendado:

1. Crear usuario
2. Login
3. Authorize
4. Probar endpoints

---

## 🐳 Docker

### Servicios

* `web`: API FastAPI
* `db`: PostgreSQL

### Volumen persistente

```id="vol1"
postgres_data
```

---

## ☁️ Deploy (Paso a paso)

### 🚀 Opción: Railway

1. Crear cuenta en Railway
2. Conectar repo de GitHub
3. Agregar variables:

```env id="env1"
DATABASE_URL=postgresql://...
SECRET_KEY=supersecret
```

4. Deploy automático

---

### 🚀 Opción: Render

1. Crear Web Service
2. Build command:

```bash id="render1"
docker build -t app .
```

3. Start command:

```bash id="render2"
uvicorn app:app --host 0.0.0.0 --port 10000
```

---

## 🧑‍💻 Autor

Diego Ditter
