from flask import Flask, jsonify, request
import apt_silmae.controller as apt_silmae_controller


# Definition
app = Flask(__name__)
app.register_blueprint(apt_silmae_controller.api, url_prefix="/apts")


@app.route("/", methods=['GET'])
def hello_world():
    print('access!')

    response = {
        "result": "ok"
    }

    return jsonify(response)


# 참고용
@app.route("/", methods=['POST'])
def hello_world_post():
    print('access!')

    params = request.get_json()
    print("받은 Json 데이터 ", params)

    response = {
        "result": "ok"
    }

    return jsonify(response)


if __name__ == '__main__':
    #apt_silmae_service.recompile_all_region()
    app.run(host='0.0.0.0', port=5050)


