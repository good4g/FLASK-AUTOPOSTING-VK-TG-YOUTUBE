from flask import render_template, current_app

from app.api.yotube import delete_video


def base_page():
    return render_template('index.html')


def login():
    return render_template('login.html')
