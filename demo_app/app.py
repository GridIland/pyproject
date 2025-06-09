"""Application Flask principale."""
from flask import Flask, jsonify


def create_app():
    """Factory pour créer l'application Flask."""
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return jsonify(
            {"message": "Hello World!", "status": "success", "app": "demo-app"}
        )

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})

    @app.route("/api/info")
    def info():
        return jsonify(
            {
                "name": "demo-app",
                "version": "1.0.0",
                "description": "Application de démonstration",
            }
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
