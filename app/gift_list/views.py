from flask import render_template
from . import gift_list

@gift_list.route('/')
def index():
    return render_template('gift_list/index.html')


