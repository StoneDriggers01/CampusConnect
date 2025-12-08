from flask import Blueprint, render_template
"""Imports Flask components for creating modular routes and rendering HTML templates."""

auth_bp = Blueprint('auth', __name__)
"""Creates a Blueprint named 'auth' to group authentication-related routes."""

@auth_bp.route("/login")

def login():
    """Function that handles rendering of the login page."""

    return render_template("login.html")
"""Renders the login.html template to display the login form to users."""