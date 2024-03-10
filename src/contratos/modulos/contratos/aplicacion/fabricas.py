from contratos.modulos.contratos.dominio.entidades import Transaccion
from contratos.modulos.contratos.aplicacion.mapeadores import MapeadorCrearTransaccion
from contratos.seedwork.dominio.repositorios import Mapeador
from contratos.seedwork.dominio.fabricas import Fabrica
from dataclasses import dataclass


@dataclass
class FabricaTransacciones(Fabrica):
    mapeador: Mapeador

    def __init__(self, mapeador: Mapeador):
        self.mapeador = mapeador

    def crear_objeto(self, obj) -> Transaccion:
        result = self.mapeador.dto_a_entidad(obj)
        assert isinstance(result, Transaccion)
        return result
