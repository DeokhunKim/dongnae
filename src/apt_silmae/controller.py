from flask import Blueprint, jsonify, request, abort, make_response
from . import service


api = Blueprint("apt_silmae", __name__)


@api.route("/downloaddata", methods=['GET'])
def download_data():
    service.update_all_region_data()

    response = {
        "result": "ok"
    }
    return jsonify(response)


@api.route("/updategeocoord", methods=['GET'])
def update_geocoord():
    service.update_geocoord()

    response = {
        "result": "ok"
    }
    return jsonify(response)


@api.route("/compile", methods=['GET'])
def compiler_all():
    service.recompile_all_region()

    response = {
        "result": "ok"
    }
    return jsonify(response)


@api.route("/", methods=["GET"])
def test():
    response = {
        "result": "ok"
    }

    abort(400)

    return jsonify(response)


@api.errorhandler(400)
def response400(error):
    print('400kk')
    response = {
        "result": "request param error",
    }
    return jsonify(response), 400


@api.route("/map", methods=["OPTION", "GET"])
def get_map():
    #level = request.args.get('level')
    yyyy = request.args.get('yyyy')
    mm = request.args.get('mm')

    if yyyy is None:
        abort(400)
    if( mm is None):
        mm = ''

    response = make_response(jsonify({
        "result": "ok",
        "data": service.get_map_by_date(yyyy, mm)
    }))
    response.status_code = 200

    # TODO - 배포할때 바꿔야함
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")

    return response



