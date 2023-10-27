from flask import Flask, request, render_template, session, redirect
from lib.models import *

app = Flask(__name__)

if __name__ == "__main__":
    if os.environ.get('APP_ENV') == 'test':
        app.secret_key = os.urandom(16)
        app.run(debug=True, port=int(os.environ.get('PORT', 7474)))
    else:
        app.secret_key = os.urandom(16)
        app.run(debug=False, host='0.0.0.0', port=7474, ssl_context='adhoc')