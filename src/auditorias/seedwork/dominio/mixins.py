from .reglas import ReglaNegocio
from .excepciones import ReglaNegocioExcepcion

class ValidarReglasMixin:
    def validar_regla(self, regla: ReglaNegocio):
        if not regla.es_valido():
            raise ReglaNegocioExcepcion(regla)
          
    def es_valido(self, regla: ReglaNegocio) -> bool:
        try:
            self.validar_regla(regla)            
        finally:
            return regla.es_valido()