from flask import render_template, request
from app import app


@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(f"{error}\nURL Called: {request.url}")
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"{error}\nURL Called: {request.url}")
    return render_template("500.html"), 500
