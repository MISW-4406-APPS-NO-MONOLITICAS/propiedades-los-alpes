from dataclasses import dataclass, field
from listados.modulos.propiedades.aplicacion.dto import PropiedadDTO
from listados.modulos.propiedades.dominio.fabricas import FabricaPropiedad
from listados.seedwork.aplicacion.comandos import Comando, ComandoHandler

@dataclass
class CrearPropiedad(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    nombre: str
    

class CrearPropiedadHandler(ComandoHandler):
    fabrica_propiedades:
    
    def __init__(self):
        self.fabrica_propiedades = FabricaPropiedad()
    
    def handle(self, comando: CrearPropiedad):
        dto = PropiedadDTO(
            id=comando.id,
            nombre=comando.nombre,
            fecha_creacion=comando.fecha_creacion,
            fecha_actualizacion=comando.fecha_actualizacion,
        )
        
        propiedad = self.fabrica_propiedades.crear_objeto(dto, self.mapeador)