from flask import Flask, redirect
from routes.admin_routes import admin_blueprint
from routes.store_routes import store_blueprint

app = Flask(__name__)
app.secret_key = 'simplekey'

# Register blueprints with correct URL prefixes
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(store_blueprint, url_prefix='/store')

# Redirect root to store home
@app.route('/')
def index():
    return redirect('/store')
from flask import Flask, jsonify
app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

@app.get("/ready")
def ready():
    # Optionally check DB connectivity here
    return jsonify(ready=True), 200

# For /metrics, either expose a simple counter or integrate prometheus_client
# pip install prometheus-client
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
REQUESTS = Counter("http_requests_total", "Total HTTP requests")

@app.before_request
def _inc():
    REQUESTS.inc()

@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
