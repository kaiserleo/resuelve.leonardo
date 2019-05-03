# flask_web/app.py

from flask import Flask, make_response, jsonify, request
from resuelvefc.exceptions import *
from resuelvefc.salaries import *
from resuelvefc.input import *
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Server up and running\n'

@app.route('/calcula_sueldo', methods=['POST'])
def compute_income():
    try:
        validator = InputValidator(request.data)
        players_in = validator.encode()
        salaries = Salaries(players_in)
        players_out = salaries.process()
        return make_response(jsonify(players_out), 200)
    except LevelNotFoundException as e:
        return make_response(\
                jsonify({'error': str(e) + ' level not found'}), 422)
    except ZeroPlayersReceivedException:
        return make_response(jsonify({'error': 'Zero Players Received'}), 422)
    except MissingFieldsException as e:
        return make_response(jsonify({'error': 'Missing fields' + str(e)}), 422)
    except NonValidFieldsException as e:
        return make_response(\
                jsonify({'error': 'Non valid fields' + str(e)}), 422)
    except ArrayExpectedException:
        return make_response(jsonify({'error': 'Array expected'}), 422)
    except InvalidPlayerFormatException:
        return make_response(jsonify({'error': 'Invalid player format'}), 422)
    except InvalidDataTypeFormatException as e:
        return make_response(\
                jsonify({'error': 'Invalid data type ' + str(e)}), 422)
    except InvalidRangeNumberException as e:
        return make_response(\
                jsonify({'error': 'Number outside range ' + str(e)}), 422)
    except JSONDecodeException as e:
        return make_response(jsonify({'error': str(e)}), 422)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'Method not allowed'}), 405)

@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Internal error'}), 500)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
