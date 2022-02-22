import os, pathlib
from flask import render_template, request, url_for, redirect, send_from_directory, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from instance.config import UPLOAD_FOLDER
from . import gift_list
from ..__init___ import ALLOWED_EXTENSIONS, db
from app.models import Gift, User


@gift_list.route('/')
def index():
    return redirect(f'/user_id:{current_user.id}/gift_list') \
        if current_user.is_authenticated \
        else render_template('gift_list/index.html')


@gift_list.route('/user_id:<int:id>/gift_list')
def gifts_list(id):
    user = User.query.get(id)
    gifts = Gift.query.filter_by(user_id=id).order_by(Gift.date.desc()).all()
    return render_template('gift_list/gift_list.html', gifts=gifts, user=user)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@gift_list.route('/create', methods=['GET', 'POST'])
@login_required
def create_gift():
    if request.method == 'POST':
        file = request.files['file']
        filename = 'default_gift.png'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        name = request.form['name']
        price = request.form['price']
        url = request.form['url']
        gift = Gift(image_path=filename, name=name, price=price, url=url, user_id=current_user.id)
        try:
            db.session.add(gift)
            db.session.commit()
        except:
            return 'При создании произошла ошибка'
        return redirect(f'/user_id:{current_user.id}/gift_list')
    else:
        return render_template('gift_list/create.html')


@gift_list.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@gift_list.route('/edit_wish_list')
@login_required
def edit_list():
    gifts = Gift.query.filter_by(user_id=current_user.id).order_by(Gift.date.desc()).all()
    return render_template('gift_list/edit_list.html', gifts=gifts, )


@gift_list.route('/gift_update/<int:id>', methods=['POST', 'GET'])
@login_required
def update(id):
    gift = Gift.query.get(id)
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            if os.path.isfile(f'{UPLOAD_FOLDER}\\{gift.image_path}'):
                os.remove(f'{UPLOAD_FOLDER}\\{gift.image_path}')
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            gift.image_path = filename
        gift.name = request.form['name']
        gift.price = request.form['price']
        gift.url = request.form['url']
        try:
            db.session.commit()
            flash('Товар успешно обновлен!')
            return redirect('/edit_wish_list')
        except:
            return 'При редактирование произошла ошибка'
    else:
        return render_template('gift_list/update_gift.html', gift=gift)


@gift_list.route('/gift_del/<int:id>')
@login_required
def gift_del(id):
    gift = Gift.query.get_or_404(id)
    if os.path.isfile(f'{UPLOAD_FOLDER}\\{gift.image_path}'):
        os.remove(f'{UPLOAD_FOLDER}\\{gift.image_path}')
    db.session.delete(gift)
    db.session.commit()
    return redirect(f'/edit_wish_list')
