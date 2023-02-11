from flask import Flask, render_template, request, flash, g, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import sqlite3 as sql
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #tensorflow warning 끄는 용
import ssl





def create_app():
    app = Flask(__name__)

    from .views import main_views, first_test, second_test, third_test, fourth_test, fifth_test, sixth_test, result
    app.register_blueprint(main_views.bp)
    app.register_blueprint(first_test.bp)
    app.register_blueprint(second_test.bp)
    app.register_blueprint(third_test.bp)
    app.register_blueprint(fourth_test.bp)
    app.register_blueprint(fifth_test.bp)
    app.register_blueprint(sixth_test.bp)
    app.register_blueprint(result.bp)

    return app