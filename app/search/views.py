from flask import render_template, flash, request
from flask_login import login_required, current_user

from .forms import InventoryDefaultForm, InventoryTypebarangForm,\
    InventoryKondisiForm, InventoryTglterimaForm,\
    InventoryAsalForm, InventoryConsumableForm
from . import search
from ..models import Inventory, Alamat, TmpReqBarang
from .. import db
from sqlalchemy import and_


def alamat_info(alamat_id, detail=False):
    if detail:
        # disini buat nampilkan detail alamatnya
        pass
    else:
        # sumari sahaja disini
        a = Alamat.query.filter_by(id=alamat_id).first()
        info = str(a.nama_pic) + " ( " + str(a.alamat)[:12] + "... )"
    return info


def tamper_inventory_result(inventory):
    inventory_mod = []
    for i in inventory:
        ii = i
        ii.asal = alamat_info(i.asal)
        inventory_mod.append(ii)
    return inventory_mod


@search.route('/search/inventory/', methods=['GET', 'POST'])
def inventory():
    #list_request = []
    form_caption = {'nama': 'Nama Barang',
                    'serial': 'Serial Number',
                    'tglterima': 'Tanggal Terima',
                    'typebarang': 'Type Barang',
                    'qty': 'Quantity',
                    'kondisi': 'Kondisi Barang',
                    'asalbarang': 'Asal Barang',
                    'consumable': 'Consulmable ?',
                    'ALL': 'Show All Data.'}
    search_by = request.args.get('by')

    # set default search type
    if search_by not in form_caption:
        search_by = 'nama'

    # masukan barang yang di cari ke dalam daftar permintaan
    if request.form.get("add_request") and current_user.is_active:
        for item in request.form.getlist('ask_item'):
            if item is not None:
                tmp_req_barang = TmpReqBarang.query.filter(and_(TmpReqBarang.pengguna_id == current_user.id,
                                                                TmpReqBarang.barang_id == int(item))).first()
                if tmp_req_barang is None:
                    tmp_req = TmpReqBarang(pengguna_id=current_user.id,
                                           barang_id=int(item))
                    db.session.add(tmp_req)
                    db.session.commit()
                    flash("Barang telah di tambahkan ke daftar permintaan.")

    # set form yang di pakai sesuai type search
    if search_by == 'typebarang':
        form = InventoryTypebarangForm()
    elif search_by == 'kondisi':
        form = InventoryKondisiForm()
    elif search_by == 'tglterima':
        form = InventoryTglterimaForm()
    elif search_by == 'asalbarang':
        form = InventoryAsalForm()
    elif search_by == 'consumable':
        form = InventoryConsumableForm()
    else:
        form = InventoryDefaultForm()

    # action kalo tombol ShowAll diklik
    if form.showall.data:
        inventory = Inventory.query.all()
        return render_template('search/inventory.html', form=form,
                               # list_request=list_request,
                               form_caption=form_caption[search_by],
                               # inventory=tamper_inventory_result(inventory),
                               inventory=inventory,
                               title='Inventory Search Result')

    # action saat tombol cari diklik
    # set query filter berdasarkan search type
    if form.search_this.data:
        if search_by == 'nama':
            query_filter = Inventory.nama.like('%'+str(form.keyword.data)+'%')
        elif search_by == 'serial':
            query_filter = Inventory.serial.like('%'+str(form.keyword.data)+'%')
        elif search_by == 'qty':
            query_filter = Inventory.qty.is_(str(form.keyword.data))
        elif search_by == 'TypeBarang':
            query_filter = Inventory.typebarang.is_(form.keyword.data)
        elif search_by == 'kondisi':
            query_filter = Inventory.is_good.is_(form.keyword.data)
        elif search_by == 'tglterima':
            query_filter = Inventory.tgl_terima.is_(form.keyword.data)
        elif search_by == 'consumable':
            query_filter = Inventory.is_consumable.is_(form.keyword.data)
        elif search_by == 'asalbarang':
            query_filter = Inventory.typebarang.is_(form.keyword.data)

        # pencarian
        if current_user.is_authenticated:
            if current_user.is_admin:
                inventory = Inventory.query.filter(query_filter).all()
            else:
                inventory = Inventory.query.filter(query_filter, Inventory.qty >= 1).all()
        else:
            inventory = Inventory.query.filter(query_filter, Inventory.qty >= 1).all()

        if len(inventory) == 0:
            flash(str(form.keyword.data) + ' tidak ditemukan.')
            return render_template('search/inventory.html',
                                   form=form, title="Selamat mencari.!")

        return render_template('search/inventory.html', form=form,
                               form_caption=form_caption[search_by],
                               # list_request=list_request,
                               inventory=inventory,
                               title='Inventory Search')
    # default page pencarian
    else:
        return render_template('search/inventory.html',
                               # list_request=list_request,
                               form_caption=form_caption[search_by], form=form,
                               title="Selamat mencari.!")
