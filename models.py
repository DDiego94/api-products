
from sqlalchemy import Column, Integer, String, Float, CheckConstraint
from database import Base

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

class ProductosDB(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    precio = Column(Float, CheckConstraint('precio > 0'), nullable=False)