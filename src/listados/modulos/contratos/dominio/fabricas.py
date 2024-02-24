""" Fábricas para la creación de objetos del dominio de contratos

"""

from .entidades import Transaccion
from .reglas import ValorMayorQueCero
from .excepciones import TipoObjetoNoExisteEnDominioVuelosExcepcion
from listados.seedwork.dominio.repositorios import Mapeador, Repositorio
from listados.seedwork.dominio.fabricas import Fabrica
from listados.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaTransaccion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        print('_Fabrica')
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            transaccion: Transaccion = mapeador.dto_a_entidad(obj)

            #self.validar_regla(MinimoUnItinerario(reserva.itinerarios))
            #[self.validar_regla(RutaValida(ruta)) for itin in reserva.itinerarios for odo in itin.odos for segmento in odo.segmentos for ruta in segmento.legs]
            
            return transaccion


@dataclass
class FabricaTransacciones(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        print('FabricaT')
        print('obj ', obj)
        if mapeador.obtener_tipo() == Transaccion.__class__:
            fabrica_transaccion = _FabricaTransaccion()
            return fabrica_transaccion.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioVuelosExcepcion()
