from flask import Flask, render_template

from routes.student_routes import student_bp


def create_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "dev-secret-key"

    app.register_blueprint(student_bp)

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
