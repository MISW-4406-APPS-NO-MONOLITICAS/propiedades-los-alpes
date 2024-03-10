import time
from auditorias.config.logger import logger
from auditorias.modulos.verificacion.aplicacion.dto import CompensacionDTO, TransaccionDTO
from auditorias.modulos.verificacion.dominio.entidades import Analisis
from auditorias.modulos.verificacion.dominio.objetos_valor import TipoAnalisis
from auditorias.modulos.verificacion.dominio.reglas import ValorMayorQueCero
from auditorias.modulos.verificacion.infraestructura.repositorios import RepositorioAnalisisDB
from auditorias.seedwork.dominio.servicios import Servicio


class ServicioAuditoria(Servicio):
  
    def auditar_contrato(self, contrato: TransaccionDTO) -> Analisis:
        logger.info(
            f"Auditando contrato {contrato.id_transaccion}"
        )
        # TODO: refinar calculos basados en reglas
        oficial = True 
        consistente = True 
        completo: bool = self.es_valido(ValorMayorQueCero(contrato.valor.valor))
        indice_confiabilidad = 1 if oficial and consistente and completo else 0
        analisis = Analisis(
            tipo_analisis = TipoAnalisis("Contrato"),
            id_correlacion = contrato.id_correlacion,
            id_transaccion = contrato.id_transaccion,
            oficial = oficial,
            consistente = consistente,
            completo = completo,
            indice_confiabilidad = indice_confiabilidad,
            auditado = False
        )
        # TODO: refinar ajustando valor mínimo de indice de confiabilidad
        analisis.auditado = True if analisis.indice_confiabilidad > 0 else False
        # delay para experimento - 2 peticiones por segundo
        time.sleep(0.5)
        
        return analisis
      
    def buscar_analisis(self, contrato_cancelar: CompensacionDTO) -> Analisis:
        repositorio = RepositorioAnalisisDB()
        result = repositorio.obtener_por_columna("id_transaccion", contrato_cancelar.id_transaccion)
        return result[0]
      