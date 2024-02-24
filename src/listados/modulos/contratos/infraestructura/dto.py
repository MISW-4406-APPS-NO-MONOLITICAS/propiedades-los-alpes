"""DTOs para la capa de infrastructura del dominio de contratos
"""
import uuid
from listados.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table, Float

Base = db.declarative_base()

class Transaccion(db.Model):
    __tablename__ = "transacciones"
    id = db.Column(db.String, primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    comprador = db.Column(db.String, nullable=True)
    vendedor = db.Column(db.String, nullable=True)
    inquilino = db.Column(db.String, nullable=True)
    arrendatario = db.Column(db.String, nullable=True)