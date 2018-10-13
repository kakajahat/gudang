from flask import render_template, flash, request
from flask_login import login_required, current_user

from .forms import InventoryDefaultForm, InventoryTypebarangForm,\
    InventoryKondisiForm, InventoryTglterimaForm,\
    InventoryAsalForm, InventoryConsumableForm
from . import search
from ..models import Inventory, Alamat


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

    if search_by not in form_caption:
        search_by = 'nama'

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

    if form.showall.data:
        inventory = Inventory.query.all()
        return render_template('search/inventory.html', form=form,
                               form_caption=form_caption[search_by],
                               inventory=tamper_inventory_result(inventory),
                               title='Inventory Search Result')

    if form.submit.data:
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

        inventory = Inventory.query.filter(query_filter).all()

        if len(inventory) == 0:
            flash(str(form.keyword.data) + ' tidak ditemukan.')
            return render_template('search/inventory.html',
                                   form=form, title="Selamat mencari.!")

        return render_template('search/inventory.html', form=form,
                               form_caption=form_caption[search_by],
                               inventory=tamper_inventory_result(inventory),
                               title='Inventory Search')
    else:
        return render_template('search/inventory.html',
                               form_caption=form_caption[search_by], form=form,
                               title="Selamat mencari.!")
