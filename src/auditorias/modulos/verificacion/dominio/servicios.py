from auditorias.modulos.verificacion.dominio.entidades import Analisis
from auditorias.modulos.verificacion.dominio.objetos_valor import TipoAnalisis
from auditorias.modulos.verificacion.dominio.reglas import ValorMayorQueCero
from auditorias.seedwork.dominio.servicios import Servicio
from auditorias.modulos.verificacion.dominio.eventos import ContratoCreadoIntegracion


class ServicioAuditoria(Servicio):
  
    def auditar_contrato(self, contrato: ContratoCreadoIntegracion) -> Analisis:
        # TODO: refinar calculos basados en reglas
        oficial = True 
        consistente = True 
        completo: bool = self.es_valido(ValorMayorQueCero(contrato.valor))
        indice_confiabilidad = 1 if oficial and consistente and completo else 0
        analisis = Analisis(
            tipo_analisis=TipoAnalisis("Contrato"),
            contrato_id=contrato.id_transaccion,
            oficial=oficial,
            consistente=consistente,
            completo=completo,
            indice_confiabilidad=indice_confiabilidad,
            auditado=False
        )
        # TODO: refinar ajustando valor mínimo de indice de confiabilidad
        analisis.auditado = True if analisis.indice_confiabilidad >= 0 else False
        
        return analisis