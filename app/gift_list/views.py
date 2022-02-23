import os
from flask import render_template, request, url_for, redirect, send_from_directory, flash
from flask_login import login_required, current_user
from sqlalchemy import exc
from werkzeug.utils import secure_filename
from instance.config import UPLOAD_FOLDER
from . import gift_list
from ..__init___ import ALLOWED_EXTENSIONS, db
from app.models import Gift, User
from .forms import CreateGift


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def file_verification(user_id, filename):
    i = 0
    while i < 100:
        name = f'{user_id}_{i}_{filename}'
        path = os.path.join(UPLOAD_FOLDER, name)
        if not os.path.exists(path):
            return name
        else:
            i += 1
            continue
    return False


@gift_list.route('/')
def index():
    return redirect(f'/user_id:{current_user.id}/gift_list') \
        if current_user.is_authenticated \
        else render_template('gift_list/index.html')


@gift_list.route('/user_id:<int:id>/gift_list')
def gifts_list(id):
    user = User.query.get(id)
    gifts = Gift.query.filter_by(user_id=id).order_by(Gift.date.desc()).all()
    return render_template('gift_list/gift_list.html', gifts=gifts, user=user, id=id)


@gift_list.route('/create', methods=['GET', 'POST'])
@login_required
def create_gift():
    form = CreateGift()
    filename = None
    if form.validate_on_submit() or request.method == 'POST':
        if form.img.data and allowed_file(form.img.data.filename):
            f = form.img.data
            filename = file_verification(current_user.id, secure_filename(f.filename))
            if filename:
                f.save(os.path.join(UPLOAD_FOLDER, filename))
            else:
                filename = None

        name = form.name.data
        price = form.price.data
        url = form.url.data
        gift = Gift(image_path=filename, name=name, price=price, url=url, user_id=current_user.id)
        try:
            db.session.add(gift)
            db.session.commit()
            return redirect(f'/user_id:{current_user.id}/gift_list')
        except:
            db.session.rollback()
            flash('При создании произошла ошибка', 'danger')
            return render_template('gift_list/create.html', form=form)
    else:
        return render_template('gift_list/create.html', form=form)


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
    form = CreateGift()
    if request.method == 'POST':
        file = form.img.data
        if file:
            if allowed_file(file.filename):
                if os.path.isfile(f'{UPLOAD_FOLDER}\\{gift.image_path}'):
                    os.remove(f'{UPLOAD_FOLDER}\\{gift.image_path}')
                filename = file_verification(current_user.id, secure_filename(file.filename))
                if filename:
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    gift.image_path = filename
                else:
                    gift.image_path = None
            else:
                flash('Недопустимый формат! ', 'danger')
                form.img.data = None
                return render_template('gift_list/update_gift.html', form=form)
        gift.name = form.name.data
        gift.price = form.price.data
        gift.url = form.url.data
        try:
            db.session.commit()
            flash('Товар успешно обновлен!')
            return redirect('/edit_wish_list')
        except:
            flash('При редактирование произошла ошибка', 'danger')
            return render_template('gift_list/update_gift.html', form=form)
    else:
        form.img.data = gift.image_path
        form.name.data = gift.name
        form.price.data = gift.price
        form.url.data = gift.url
        return render_template('gift_list/update_gift.html', form=form)


@gift_list.route('/gift_del/<int:id>')
@login_required
def gift_del(id):
    gift = Gift.query.get_or_404(id)
    if os.path.isfile(f'{UPLOAD_FOLDER}\\{gift.image_path}'):
        os.remove(f'{UPLOAD_FOLDER}\\{gift.image_path}')
    db.session.delete(gift)
    db.session.commit()
    return redirect(f'/edit_wish_list')
