from listados.modulos.propiedades.dominio.entidades import Propiedad
from listados.seedwork.dominio.repositorios import Mapeador
from listados.seedwork.dominio.fabricas import Fabrica


class MapeadorCreatePropiedad(Mapeador):

    def dto_a_entidad(self, dto: dict) -> Propiedad:
        try:
            return Propiedad(
                id=dto["id"],
                nombre=dto["nombre"],
                fecha_creacion=dto["fecha_creacion"],
                fecha_actualizacion=dto["fecha_actualizacion"],
            )
        except KeyError as e:
            raise ValueError(
                f"Error en el mapeo de la propiedad: {e} no existe en el diccionario"
            )
            


class FabricaPropiedad(Fabrica):

    def crear_objeto(self, obj, mapeador: Mapeador = None) -> Propiedad:
        if mapeador is None:
            mapeador = MapeadorCreatePropiedad()
        result = mapeador.dto_a_entidad(obj)
        assert isinstance(result, Propiedad)
        return result
