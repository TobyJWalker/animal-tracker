from flask import Flask, request, render_template, session, redirect
from lib.models import *

# create the app and configure it
app = Flask(__name__)
create_db_tables()







# run the app if file is executed
if __name__ == "__main__":
    if os.environ.get('APP_ENV') == 'test':
        app.secret_key = os.urandom(16)
        app.run(debug=True, port=int(os.environ.get('PORT', 7474)))
    else:
        app.secret_key = os.urandom(16)
        app.run(debug=False, host='0.0.0.0', port=7474, ssl_context='adhoc')