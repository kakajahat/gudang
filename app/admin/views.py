from datetime import datetime
from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required

from . import admin
from .forms import InventoryForm, AlamatForm
from .. import db
from ..models import Inventory, TypeBarang, Alamat, Pengguna


def check_admin():
    if not current_user.is_admin:
        abort(403)


def alamat_info(alamat_id, detail=False):
    if detail:
        # disini buat nampilkan detail alamatnya
        pass
    else:
        # sumari sahaja disini
        a = Alamat.query.filter_by(id=alamat_id).first()
        info = str(a.nama_pic) + " ( " + str(a.alamat)[:12] + "... )"
    return info


@admin.route('/inventory', methods=['GET'])
@login_required
def list_inventory():
    check_admin()

    inventory_mod = []
    inventory = Inventory.query.all()
    for i in inventory:
        ii = i
        ii.asal = alamat_info(i.asal)
        inventory_mod.append(ii)

    return render_template('admin/inventory/list_inventory.html',
                           inventory=inventory_mod, title='Inventory')


@admin.route('/inventory/add', methods=['GET', 'POST'])
@login_required
def add_inventory():
    check_admin()

    add_inventory = True

    form = InventoryForm()

    # if form.validate_on_submit():  #gak kompatibel sama field 'asal' QuerySelectField
    if form.submit.data:
        isgood = False
        if form.kondisi.data == 'True':
            isgood = True

        inventory = Inventory(nama=form.nama.data,
                              # tgl_terima = datetime(int(tt_y), int(tt_m), int(tt_d))#,
                              tgl_terima=form.tgl_terima.data,
                              is_consumable=form.consumable.data,
                              typebarang=form.typebarang.data,
                              serial=form.serial.data,
                              qty=form.qty.data,
                              is_good=isgood,
                              #asal = int(form.asal_barang.data)
                              asal=form.asal_barang.data
                              )

        try:
            db.session.add(inventory)
            db.session.commit()
            flash('Inventory baru telah di tambahkan.')
        except Exception as e:
            flash('Dear Human,<br/>' + str(e))
            #flash('barang ini sudah ada, silahkan di edit sahaja.')
            return redirect(url_for('admin.list_inventory'))

    return render_template('admin/inventory/inventory.html', action='Add',
                           add_inventory=add_inventory, form=form,
                           title='Tambah Inventory')


@admin.route('/inventory/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_inventory(id):
    check_admin()

    add_inventory = False

    inventory = Inventory.query.get_or_404(id)
    form = InventoryForm(obj=inventory)
    # if form.validate_on_submit():
    if form.submit.data:
        isgood = False
        if form.kondisi.data == 'True':
            isgood = True

        inventory.nama = form.nama.data
        inventory.tlg_terima = form.tgl_terima.data
        inventory.is_consumable = form.consumable.data
        inventory.typebarang = form.typebarang.data
        inventory.serial = form.serial.data
        inventory.qty = form.qty.data
        inventory.is_good = isgood
        inventory.asal = form.asal_barang.data

        db.session.commit()
        flash('Data telah di edit.')

        return redirect(url_for('admin.list_inventory'))

    form.nama.data = inventory.nama
    form.tgl_terima.data = inventory.tgl_terima
    form.consumable.data = inventory.is_consumable
    form.typebarang.data = inventory.typebarang
    form.serial.data = inventory.serial
    form.qty.data = inventory.qty
    form.kondisi.data = inventory.is_good
    form.asal_barang.data = inventory.asal
    return render_template('admin/inventory/inventory.html', action='Edit',
                           add_inventory=add_inventory, form=form,
                           inventory=inventory, title='Edit Inventory')


@admin.route('/inventory/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_inventory(id):
    check_admin()

    inventory = Inventory.query.get_or_404(id)
    db.session.delete(inventory)
    db.session.commit()
    flash('inventory berhasil di hapus.')

    return redirect(url_for('admin.list_inventory'))


@admin.route('/alamat', methods=['GET'])
@login_required
def list_alamat():
    check_admin()

    alamat = Alamat.query.all()
    return render_template('admin/alamat/list_alamat.html',
                           alamat=alamat, title='Alamat')


@admin.route('/alamat/add', methods=['GET', 'POST'])
@login_required
def add_alamat():
    check_admin()

    add_alamat = True

    form = AlamatForm()
    if form.validate_on_submit():
        alamat = Alamat(nama_pic=form.nama_pic.data,
                        alamat=form.alamat.data,
                        keterangan=form.keterangan.data)

        try:
            db.session.add(alamat)
            db.session.commit()
            flash('Alamat baru telah di tambahkan.')
        except:
            flash('Alamat ini sudah ada, di lahkan di edit sahaja.')
        return redirect(url_for('admin.list_alamat'))

    return render_template('admin/alamat/alamat.html', action='Add',
                           add_alamat=add_alamat, form=form,
                           title='Tambah Alamat')


@admin.route('/alamat/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_alamat(id):
    check_admin()

    add_alamat = False

    alamat = Alamat.query.get_or_404(id)
    form = AlamatForm(obj=alamat)
    if form.validate_on_submit():
        alamat.nama_pic = form.nama_pic.data
        alamat.alamat = form.alamat.data
        alamat.keterangan = form.keterangan.data

        db.session.commit()
        flash('Data telah di edit.')

        return redirect(url_for('admin.list_alamat'))

    form.nama_pic.data = alamat.nama_pic
    form.alamat.data = alamat.alamat
    form.keterangan.data = alamat.keterangan

    return render_template('admin/alamat/alamat.html', action='Edit',
                           add_alamat=add_alamat, form=form,
                           alamat=alamat, title='Edit Alamat')


@admin.route('/alamat/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_alamat(id):
    check_admin()

    alamat = Alamat.query.get_or_404(id)
    db.session.delete(alamat)
    db.session.commit()
    flash('alamat berhasil di hapus.')

    return redirect(url_for('admin.list_alamat'))


@admin.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    check_admin()
    debug = []
    users = Pengguna.query.filter(Pengguna.is_admin == False).all()
    if request.form.get("update_users"):
        del_users = request.form.getlist('delete_user')
        active_users = request.form.getlist('active_user')

        for user in users:
            if str(user.id) in del_users:
                db.session.delete(user)
            else:
                if user.is_active == False:
                    if str(user.id) in active_users:
                        user.is_active = True
                else:
                    if str(user.id) not in active_users:
                        user.is_active = False

        db.session.commit()
        users = Pengguna.query.filter(Pengguna.is_admin == False).all()

    return render_template('admin/users.html', users=users,
                           debug=debug,
                           title="Users Manage")
