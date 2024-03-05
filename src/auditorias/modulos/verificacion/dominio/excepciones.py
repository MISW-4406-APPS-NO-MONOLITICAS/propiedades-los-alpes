""" # Excepciones del dominio de auditorias

from auditorias.seedwork.dominio.excepciones import ExcepcionFabrica

class TipoObjetoNoExisteEnDominioVuelosExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de auditorias'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)
 """