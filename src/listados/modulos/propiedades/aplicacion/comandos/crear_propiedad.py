from dataclasses import dataclass, field
from listados.seedwork.aplicacion.comandos import Comando

@dataclass
class CrearPropiedad(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    #itinerarios: list[ItinerarioDTO]