from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
from .forms import LoginForm, RegistrationForm, UpdateInfoForm
from .. import db
from ..models import Pengguna


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        pengguna = Pengguna(email=form.email.data,
                            uname=form.uname.data,
                            nama=form.name.data,
                            passwd=form.passwd.data,
                            alamat=form.alamat.data)

        db.session.add(pengguna)
        db.session.commit()
        flash('Registrasi berhasil.')

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form,
                           caption='Registrasi Pengguna', title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pengguna = Pengguna.query.filter_by(email=form.email.data).first()
        if pengguna is not None and pengguna.verify_passwd(form.passwd.data):
            login_user(pengguna)

            if pengguna.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))
        else:
            flash('Email atau password anda salah.')

    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout dengan sukses.')
    return redirect(url_for('auth.login'))


@auth.route('/updateuser', methods=['GET', 'POST'])
@login_required
def update_user():
    debug = []
    user = Pengguna.query.filter_by(id=current_user.id).first()
    form = UpdateInfoForm(email=user.email,
                          nama=user.nama,
                          alamat=user.alamat)

    if form.submit.data:
        if user.verify_passwd(form.old_passwd.data):
            user.nama = form.nama.data
            user.email = form.email.data
            #user.uname = form.uname.data
            user.alamat = form.alamat.data
            if form.new_passwd.data is not '':
                user.passwd = form.new_passwd.data
                debug = form.new_passwd.data

            db.session.commit()
            flash('Info anda telah di update.')
        else:
            flash('Info tidak di update, Password yg di gunakan saat ini salah.')

    return render_template('auth/register.html', form=form,
                           # debug=debug,
                           caption='Update Info Pengguna', title='Register')
