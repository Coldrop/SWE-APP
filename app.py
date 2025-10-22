from flask import Flask, redirect, jsonify
from metrics import metrics

app = Flask(__name__)
app.secret_key = 'simplekey'

metrics.init_app(app)

from routes.admin_routes import admin_blueprint
from routes.store_routes import store_blueprint

# Register blueprints with correct URL prefixes
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(store_blueprint, url_prefix='/store')

# Redirect root to store home
@app.route('/')
def index():
    return redirect('/store')

@app.route('/health')
@metrics.do_not_track()
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
