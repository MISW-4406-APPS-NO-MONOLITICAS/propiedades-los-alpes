""" from auditorias.modulos.verificacion.dominio.entidades import Transaccion
from auditorias.modulos.verificacion.aplicacion.mapeadores import MapeadorTransaccion
from auditorias.seedwork.dominio.repositorios import Mapeador
from auditorias.seedwork.dominio.fabricas import Fabrica
from dataclasses import dataclass


@dataclass
class FabricaTransacciones(Fabrica):
    def crear_objeto(self, obj, mapeador: Mapeador | None = None) -> Transaccion:
        mapeador = mapeador or MapeadorTransaccion()
        result = mapeador.dto_a_entidad(obj)
        assert isinstance(result, Transaccion)
        return result
 """