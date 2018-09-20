from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import InventoryForm
from .. import db
from ..models import Inventory, TypeBarang, Alamat, Kota, Propinsi, Negara



def check_admin():
    if not current_user.is_admin:
        abort(403)

@admin.route('/inventory', methods=['GET'])
@login_required
def list_inventory():
    check_admin()

    inventory = Inventory.query.all()
    return render_template('admin/inventory/list_inventory.html',
                            inventory=inventory, title='Inventory')


@admin.route('/inventory/add', methods=['GET', 'POST'])
@login_required
def add_inventory():
    check_admin()

    add_inventory = True

    form = InventoryForm()
    if form.validate_on_submit():
        inventory = Inventory(nama = form.nama.data,
                                tlg_terima = form.tgl_terima.data,
                                is_consumable = form.consumable.data,
                                typebarang = form.typebarang.data,
                                serial = form.serial.data,
                                qty = form.qty.data,
                                is_good = form.kondisi.data,
                                asal = form.asal_barang.data
                                )

        try:
            db.session.add(inventory)
            db.session.commit()
            flash('Inventory baru telah di tambahkan.')
        except:
            flash('barang ini sudah ada, di lahkan di edit sahaja.')
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
    if form.validate_on_submit():
        nama = form.nama.data
        tlg_terima = form.tgl_terima.data
        is_consumable = form.consumable.data
        typebarang = form.typebarang.data
        serial = form.serial.data
        qty = form.qty.data
        is_good = form.kondisi.data
        asal = form.asal_barang.data
        
        db.session.commit()
        flash('Data telah di edit.')
        
        return redirect(url_for('admin.list_inventory'))
        
    form.nama.data = inventory.nama
    form.tgl_terima.data = inventory.tlg_terima
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
    
    return render_template(title='Hapus inventory.')
    
    
    
@admin.route('/alamat', methods=['GET'])
@login_required
def list_alamat():
    check_admin()

    inventory = Alamat.query.all()
    return render_template('admin/alamat/list_alamat.html',
                            alamat=alamat, title='Alamat')


@admin.route('/alamat/add', methods=['GET', 'POST'])
@login_required
def add_alamat():
    check_admin()

    add_alamat = True

    form = AlamatForm()
    if form.validate_on_submit():
        ## set formasi untuk insert relasional data ini dipasang di forms
        #propinsi = Propinsi.query.all()
        #kota = Kota.query.all()
        #negara = Negara.query.all()
        kota = Kota.query.filter_by(id=form.kota.data).first()
        if not kota.id:
            kota = Kota(nama=form.kota.data,
                        propinsi=form.propinsi.data)
            db.session.add(kota)
            db.session.commit()
            kota = Kota.query.filter_by(nama=form.kota.data).first()
        
        alamat = Alamat(nama_pic=form.nama_pic.data,
                        alamat=form.alamat.data,
                        kota=kota.id,
                        propinsi=form.propinsi.data,
                        negara=form.negara.data,
                        keterangan=form.keterangan.data )

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
        kota = Kota.query.filter_by(id=form.kota.data).first()
        if not kota.id:
            kota = Kota(nama=form.kota.data,
                        propinsi=form.propinsi.data)
            db.session.add(kota)
            db.session.commit()
            kota = Kota.query.filter_by(nama=form.kota.data).first()
            
        nama_pic=form.nama_pic.data
        alamat=form.alamat.data
        kota=kota.id
        propinsi=form.propinsi.data
        negara=form.negara.data
        keterangan=form.keterangan.data
        
        db.session.commit()
        flash('Data telah di edit.')
        
        return redirect(url_for('admin.list_inventory'))
    
    form.nama_pic.data = alamat.nama_pic
    form.alamat.data = alamat.alamat
    kota.id = alamat.kota
    form.propinsi.data = alamat.propinsi
    form.negara.data = alamat.negara
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
    
    return render_template(title='Hapus alamat.')
