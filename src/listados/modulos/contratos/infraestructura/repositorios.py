""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de contratos

"""

import pdb
from listados.config.db import db
from listados.modulos.contratos.dominio.repositorios import RepositorioTransacciones, RepositorioProveedores
from listados.modulos.contratos.dominio.objetos_valor import FechaInicio, FechaVencimiento, Valor, NoticiaMedio, MaterialMercado
from listados.modulos.contratos.dominio.entidades import Transaccion, Venta, Alquiler, Listado, Subarrendamiento, TrabajoConjunto
from listados.modulos.contratos.dominio.fabricas import FabricaTransacciones
from .dto import TransaccionDB as TransaccionDTO
from .mapeadores import MapeadorTransaccion
from uuid import UUID

class RepositorioProveedoresDB(RepositorioProveedores):

    def obtener_por_id(self, id: UUID) -> Transaccion:
        # TODO
        raise NotImplementedError

    def obtener_todos(self) -> list[Transaccion]:
        # TODO
        return []

    def agregar(self, entity: Transaccion):
        # TODO
        raise NotImplementedError

    def actualizar(self, entity: Transaccion):
        # TODO
        raise NotImplementedError

    def eliminar(self, entity_id: UUID):
        # TODO
        raise NotImplementedError


class RepositorioTrasaccionesDB(RepositorioTransacciones):

    def __init__(self):
        self._fabrica_transacciones: FabricaTransacciones = FabricaTransacciones()

    @property
    def fabrica_transacciones(self):
        return self._fabrica_transacciones

    def obtener_por_id(self, id: UUID) -> Transaccion:
        transaccion_dto = db.session.query(TransaccionDTO).filter_by(id=str(id)).one()
        return self.fabrica_transacciones.crear_objeto(transaccion_dto, MapeadorTransaccion())

    def obtener_todos(self) -> list[Transaccion]:
        # TODO
        raise NotImplementedError

    def agregar(self, transaccion: Transaccion):
        transaccion_dto = MapeadorTransaccion().entidad_a_dto(transaccion)
        db.session.add(transaccion_dto)

    def actualizar(self, transaccion: Transaccion):
        # TODO
        raise NotImplementedError

    def eliminar(self, transaccion_id: UUID):
        # TODO
        raise NotImplementedError