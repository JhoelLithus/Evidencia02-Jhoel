from flask import Flask, jsonify, request, make_response
import jwt 
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisthesecretkey'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : '¡Falta el token!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : '¡El token no válido!'}), 403

        return f(*args, **kwargs)

    return decorated

@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : '¡Cualquiera puede ver esto, No esta Protegido!'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message' : 'Esto solo está disponible para personas con tokens válidos.'})

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'jhoel' and auth.username == "jhoel":
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=15)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token})

    return make_response('¡No se pudo verificar!; ingrese los datos correspondientes', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

if __name__ == '__main__':
    app.run(debug=True)

