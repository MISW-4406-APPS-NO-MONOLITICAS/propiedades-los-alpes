import json
import uuid
from flask import Blueprint, request, Response
from listados.modulos.propiedades.aplicacion.queries.obtener_listado_propiedades import (
    ObtenerPropiedades,
)
from listados.modulos.propiedades.aplicacion.queries.obtener_propiedad import (
    ObtenerPropiedad,
)
from listados.seedwork.aplicacion.queries import ejecutar_query
from listados.modulos.propiedades.aplicacion.mapeadores import MapeadorPropiedadDTOJson
from listados.modulos.arrendamiento.aplicacion.mapeadores import MapeadorArrendamientoDTOJson

from listados.modulos.arrendamiento.aplicacion.comandos.arrendar_propiedad import (
    ComandoArrendarPropiedad
)

from listados.seedwork.aplicacion.comandos import ejecutar_commando
from listados.seedwork.dominio.excepciones import ExcepcionDominio

import faker

blueprint = Blueprint('listados', __name__, url_prefix='/listados')
mapeador = MapeadorArrendamientoDTOJson()


@blueprint.route("", methods=("POST",))
def crear_arrendamiento():
    try:
        arrendamiento_dict = request.json
        arrendamiento_dto = mapeador.externo_a_dto(arrendamiento_dict)

        comando = ComandoArrendarPropiedad(
            id_correlacion=arrendamiento_dto.id_correlacion,
            id_propiedad=arrendamiento_dto.id_propiedad,
            id_transaccion=arrendamiento_dto.id_transaccion,
            fecha_evento=arrendamiento_dto.fecha_evento,
            valor=arrendamiento_dto.valor,
            inquilino=arrendamiento_dto.inquilino,
            arrendatario=arrendamiento_dto.arrendatario
        )
        ejecutar_commando(comando)
        return Response("{}", status=202, mimetype="application/json")
    except ExcepcionDominio as e:
        return Response(
            json.dumps(dict(error=str(e))), status=400, mimetype="application/json"
        )

@blueprint.route("propiedades", methods=("GET",))
def obtener_propiedades():
    result = ejecutar_query(ObtenerPropiedades())
    map_propiedad = MapeadorPropiedadDTOJson()
    return [map_propiedad.dto_a_externo(propiedad) for propiedad in result.resultado]


@blueprint.route("propiedades/<id>", methods=("GET",))
def obtener_propiedad(id: uuid.UUID):
    result = ejecutar_query(ObtenerPropiedad(id))
    map_propiedad = MapeadorPropiedadDTOJson()
    if result.resultado is None:
        return {"mensaje": "Propiedad no encontrada"}, 404
    return map_propiedad.dto_a_externo(result.resultado)


@blueprint.route("seeder", methods=("POST",))
def seeder():
    from listados.modulos.propiedades.aplicacion.comandos.crear_propiedad import (
        ComandoCrearPropiedad, ComandoCrearPropiedadHandler
    )
    datos = request.json
    if datos is not None:
        cantidad = datos.get('cantidad', 10)
    else:
        cantidad = 10
       
    for i in range(cantidad):
        comando = ComandoCrearPropiedad(
            id_propiedad = str(uuid.uuid4()),
            tipo_construccion = faker.Faker().random_element(elements=("casa", "apartamento", "oficina", "local comercial")),
            estado = faker.Faker().random_element(elements=(True, False)),
            area = faker.Faker().random_int(min=50, max=500),
            direccion = faker.Faker().street_address(),
            lote = "lote " + str(faker.Faker().random_number(digits=3, fix_len=True)),
            compania = faker.Faker().company(),
            fecha_creacion = faker.Faker().date_between(start_date='-5y', end_date='today'),
            id_transaccion = str(uuid.uuid4())
        )
        ComandoCrearPropiedadHandler().handle(comando)   

    return Response("{}", status=202, mimetype="application/json")