import json
from flask import Blueprint, request, Response
from listados.modulos.propiedades.aplicacion.queries.obtener_listado_contratos import (
    ObtenerPropiedades,
)
from listados.seedwork.aplicacion.queries import ejecutar_query
from listados.modulos.propiedades.aplicacion.mapeadores import MapeadorPropiedadDTOJson
from listados.modulos.propiedades.aplicacion.comandos.crear_propiedad import (
    ComandoCrearPropiedad
)
from listados.seedwork.aplicacion.comandos import ejecutar_commando
from listados.seedwork.dominio.excepciones import ExcepcionDominio

blueprint = Blueprint('listados', __name__, url_prefix='/listados')
mapeador = MapeadorPropiedadDTOJson()


@blueprint.route("", methods=("POST",))
def crear_propiedad():
    try:
        propiedad_dict = request.json

        propiedad_dto = mapeador.externo_a_dto(propiedad_dict)

        comando = ComandoCrearPropiedad(
            tipo_construccion=propiedad_dto.tipo_construccion,
            estado=propiedad_dto.estado,
            area=propiedad_dto.area,
            direccion=propiedad_dto.direccion,
            lote=propiedad_dto.lote,
            compania=propiedad_dto.compania,
            fecha_registro=propiedad_dto.fecha_registro,
            fecha_actualizacion=propiedad_dto.fecha_actualizacion,

        )
        ejecutar_commando(comando)
        return Response("{}", status=202, mimetype="application/json")
    except ExcepcionDominio as e:
        return Response(
            json.dumps(dict(error=str(e))), status=400, mimetype="application/json"
        )
        

@blueprint.route("", methods=("GET",))
def listar_transacciones():
    result = ejecutar_query(ObtenerPropiedades())
    return [mapeador.dto_a_externo(dto) for dto in result.resultado]
