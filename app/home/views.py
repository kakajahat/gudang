from datetime import datetime
from flask import render_template, flash, request
from flask_login import login_required, current_user

from . import home
from ..models import TmpReqBarang, Inventory, ReqBarang
from .. import db
from sqlalchemy import and_


@home.route('/', methods=['GET'])
def homepage():
    return render_template('home/index.html', title="Selamat Datang.!")


@home.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('home/dashboard.html', title="Dashboard")


@home.route('/admin/dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html')


@home.route('/reqbarang', methods=['GET', 'POST'])
@login_required
def req_barang():
    debug = []

    # handling list tmp request barang
    view_tmp_req_barang = []
    view_req_barang = []
    view_done_req_barang = []
    tmp_reqs = TmpReqBarang.query.filter_by(pengguna_id=current_user.id).all()

    if request.form.get("update_request") and current_user.is_active:
        remove_items = request.form.getlist('remove_item')
        for remove_item in remove_items:
            remove_req_barang = TmpReqBarang.query.filter(and_(TmpReqBarang.pengguna_id == current_user.id,
                                                               TmpReqBarang.barang_id == remove_item)).first()
            db.session.delete(remove_req_barang)
            db.session.commit()

        for tmp_req in tmp_reqs:
            if str(tmp_req.barang_id) not in remove_items:
                updated_qty = int(request.form.get('qty_req_' + str(tmp_req.barang_id)))

                inventory = Inventory.query.filter_by(id=str(tmp_req.barang_id)).first()

                if int(inventory.qty) < updated_qty:
                    updated_qty = inventory.qty

                update_req_barang = TmpReqBarang.query.filter(and_(TmpReqBarang.pengguna_id == current_user.id,
                                                                   TmpReqBarang.barang_id == tmp_req.barang_id)).first()
                update_req_barang.qty = updated_qty
                db.session.commit()

        tmp_reqs = TmpReqBarang.query.filter_by(pengguna_id=current_user.id).all()

    # Handling pengajuan permintaan barang
    if request.form.get("send_request") and current_user.is_active:
        for tmp_req in tmp_reqs:
            req_barang = ReqBarang(pengguna_id=current_user.id,
                                   barang_id=tmp_req.barang_id,
                                   qty=tmp_req.qty,
                                   tgl_terima=datetime.now()
                                   )
            db.session.add(req_barang)
            db.session.commit()

            inventory = Inventory.query.filter_by(id=tmp_req.barang_id).first()
            inventory.qty = inventory.qty - int(tmp_req.qty)
            db.session.commit()

            db.session.delete(tmp_req)
            db.session.commit()

            tmp_reqs = TmpReqBarang.query.filter_by(pengguna_id=current_user.id).all()

    # handling form permintaan barang yang sudah di ajukan
    if current_user.is_admin:
        reqs = ReqBarang.query.all()
    else:
        reqs = ReqBarang.query.filter_by(pengguna_id=current_user.id).all()
    if request.form.get("batal_request") and current_user.is_active:
        batal_items = request.form.getlist('batal_item')
        for batal_item in batal_items:
            batal_req_barang = ReqBarang.query.filter(and_(ReqBarang.pengguna_id == current_user.id,
                                                           ReqBarang.barang_id == batal_item)).first()
            inventory = Inventory.query.filter_by(id=batal_item).first()
            inventory.qty = inventory.qty + int(batal_req_barang.qty)

            db.session.delete(batal_req_barang)
            db.session.commit()

        reqs = ReqBarang.query.filter_by(pengguna_id=current_user.id).all()

    if request.form.get("update_list_request") and current_user.is_admin:
        done_items = request.form.getlist('done_item')
        for done_item in done_items:
            done_req_barang = ReqBarang.query.filter(ReqBarang.barang_id == done_item).first()
            done_req_barang.tgl_selesai = datetime.now()
            done_req_barang.is_done = True

        for req in reqs:
            if request.form.get('ket_' + str(req.barang_id)):
                req.keterangan = str(request.form.get('ket_' + str(req.barang_id)))

        db.session.commit()
        reqs = ReqBarang.query.filter_by(is_done=False).all()

    # Buat list untuk tampilan
    for tmp_req in tmp_reqs:
        item = {}
        inventory = Inventory.query.filter_by(id=tmp_req.barang_id).first()
        item['id'] = inventory.id
        item['nama'] = inventory.nama
        item['typebarang'] = inventory.typebarang
        item['serial'] = inventory.serial
        item['qty'] = inventory.qty
        item['is_good'] = inventory.is_good
        item['qty_req'] = tmp_req.qty
        view_tmp_req_barang.append(item)

    for req in reqs:
        req_item = {}
        inventory = Inventory.query.filter_by(id=req.barang_id).first()
        req_item['id'] = inventory.id
        req_item['pengguna'] = req.pengguna_id
        req_item['nama'] = inventory.nama
        req_item['typebarang'] = inventory.typebarang
        req_item['serial'] = inventory.serial
        req_item['qty'] = req.qty
        req_item['tgl_terima'] = req.tgl_terima
        req_item['tgl_selesai'] = req.tgl_selesai
        req_item['keterangan'] = req.keterangan
        if req.is_done:
            view_done_req_barang.append(req_item)
        else:
            view_req_barang.append(req_item)

    if request.form.get("doned_request"):
        return render_template('home/done_req_barang.html',
                               done_req_barang=view_done_req_barang,
                               title="Request Barang")
    else:
        return render_template('home/req_barang.html',
                               tmp_req_barang=view_tmp_req_barang,
                               req_barang=view_req_barang,
                               done_req_barang=view_done_req_barang,
                               # debug=debug,
                               title="Request Barang")
