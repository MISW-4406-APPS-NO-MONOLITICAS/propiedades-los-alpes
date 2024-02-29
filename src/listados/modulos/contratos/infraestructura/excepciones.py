""" Excepciones para la capa de infrastructura del dominio de contratos
"""

from listados.seedwork.dominio.excepciones import ExcepcionFabrica


class NoExisteImplementacionParaTipoFabricaExcepcion(ExcepcionFabrica):
    def __init__(
        self,
        mensaje="No existe una implementación para el repositorio con el tipo dado.",
    ):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)
