from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, \
    SubmitField, IntegerField, \
    BooleanField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from sqlalchemy import func

from ..models import Alamat, Inventory


class get_list_alamat(object):
    def __iter__(self):
        alamat = Alamat.query.all()
        list_alamat = []

        for a in alamat:
            #list_alamat.append((a.id, str(a.alamat)[:12]))
            pair = (a.id, str(a.nama_pic) + " ( " +
                    str(a.alamat)[:12] + "... )")
            yield pair


class get_list_typebarang(object):
    def __iter__(self):
        inventory = Inventory.query.group_by(typebarang).all()

        for i in inventory:
            pair = (str(i.typebarang), str(i.typebarang))
            yield pair


class InventorySearchForm(FlaskForm):
    nama = StringField('Nama Barang', validators=[DataRequired()])
    tgl_terima = DateField("Tgl Terima", id='datepick', format="%m/%d/%Y")
    typebarang = SelectField(choices=get_list_typebarang(), label="Type")
    serial = StringField("Serial")
    qty = StringField("Qty")
    kondisi = SelectField(choices=[('True', 'Baik'), ('False', 'Rusak')],
                          label="Kondisi")
    asal_barang = SelectField(choices=get_list_alamat(), label="Asal")
    consumable = BooleanField("Consumable")
    submit = SubmitField('Submit')
