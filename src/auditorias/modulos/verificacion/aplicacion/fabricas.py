from auditorias.modulos.verificacion.dominio.entidades import Analisis
from auditorias.modulos.verificacion.aplicacion.mapeadores import MapeadorAnalisis
from auditorias.seedwork.dominio.repositorios import Mapeador
from auditorias.seedwork.dominio.fabricas import Fabrica
from dataclasses import dataclass


@dataclass
class FabricaAnalisis(Fabrica):
    def crear_objeto(self, obj, mapeador: Mapeador | None = None) -> Analisis:
        mapeador = mapeador or MapeadorAnalisis()
        result = mapeador.dto_a_entidad(obj)
        assert isinstance(result, Analisis)
        return result
