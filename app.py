from flask import Flask, render_template
"""Imports Flask core class for creating the app and render_template for HTML rendering."""

from routes.auth_routes import auth_bp
"""Imports the authentication Blueprint to handle login-related routes."""

from routes.api_routes import api_bp
"""Imports the API Blueprint to handle weather alert routes."""

from routes.event_routes import event_bp
"""Imports the event Blueprint to handle campus event routes."""

app = Flask(__name__)
"""Initializes the Flask application instance."""

app.template_folder = "templates"
"""Specifies the folder where HTML templates are stored."""

app.static_folder = "static"
"""Specifies the folder where static files (CSS, JS, images) are stored."""

# Define what they user should see when they visit the root URL
@app.route("/")

def index():
    """Function that renders the homepage template."""

    return render_template("index.html")
    """Renders the index.html template when the root URL is accessed."""

# Register blueprints
app.register_blueprint(auth_bp)
"""Registers the authentication Blueprint with the app."""

app.register_blueprint(api_bp)
"""Registers the API Blueprint with the app."""

app.register_blueprint(event_bp)
"""Registers the event Blueprint with the app."""

if __name__ == "__main__":
    """Ensures the app runs only when executed directly, not when imported."""

    app.run(debug=True)
    """Runs the Flask app in debug mode, enabling live reload and error details."""