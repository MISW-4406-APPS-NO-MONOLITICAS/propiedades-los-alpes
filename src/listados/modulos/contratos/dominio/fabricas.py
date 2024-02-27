""" Fábricas para la creación de objetos del dominio de contratos

"""

import pdb
from .entidades import Transaccion
from .reglas import ValorMayorQueCero
from .excepciones import TipoObjetoNoExisteEnDominioVuelosExcepcion
from listados.seedwork.dominio.repositorios import Mapeador, Repositorio
from listados.seedwork.dominio.fabricas import Fabrica
from listados.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class FabricaTransacciones(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> Transaccion:
        print('FabricaT')
        print('obj ', obj)
        print(mapeador.__class__)
        if mapeador.obtener_tipo() == Transaccion.__class__:
            result = mapeador.dto_a_entidad(obj)
            assert isinstance(result, Entidad)
            return result
        else:
            raise TipoObjetoNoExisteEnDominioVuelosExcepcion()
