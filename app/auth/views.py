from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import RegistrationForm,LoginForm
from ..__init___ import db
from ..models import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=form.password.data)

        try:
            # add user to the database
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегистрировались! Теперь вы можете войти на сайт!')
        except:
            flash('Во время регистрации произошла ошибка попробуйте еще раз ')

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            print(user.id)
            return redirect(f'/user_id:{user.id}/gift_list')

        else:
            flash('Неправильно введена почта!')
    else:
        return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы!')
    return redirect(url_for('auth.login'))

