from flask import render_template
from . import gift_list

@gift_list.route('/')
def index():
    return 'Welcome to my gift list!'
