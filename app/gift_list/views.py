import os
from flask import render_template, request, url_for, redirect, send_from_directory
from werkzeug.utils import secure_filename
from . import gift_list
from ..__init___ import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, db
from app.models import Gift


@gift_list.route('/')
def index():
    gifts = Gift.query.order_by(Gift.date.desc()).all()
    return render_template('gift_list/index.html', gifts=gifts)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@gift_list.route('/create', methods=['GET', 'POST'])
def create_gift():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            name = request.form['name']
            price = request.form['price']
            url = request.form['url']
            gift = Gift(image_path=filename, name=name, price=price, url=url)
            try:
                db.session.add(gift)
                db.session.commit()
            except:
                return 'При создании произошла ошибка'
            return redirect('/')
    else:
        return render_template('gift_list/create.html')


@gift_list.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
