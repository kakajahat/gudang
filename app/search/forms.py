from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, \
    SubmitField, IntegerField, \
    BooleanField, DateField, RadioField
from wtforms.validators import DataRequired

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
        inventory = Inventory.query.group_by(Inventory.typebarang).all()

        for i in inventory:
            pair = (str(i.typebarang), str(i.typebarang))
            yield pair


class InventorySearchForm(FlaskForm):
    nama = StringField('Nama Barang')
    tgl_terima = DateField("Tgl Terima", id='datepick', format="%m/%d/%Y")
    typebarang = SelectField(choices=get_list_typebarang(), label="Type")
    serial = StringField("Serial")
    qty = StringField("Qty")
    kondisi = SelectField(choices=[('True', 'Baik'), ('False', 'Rusak')],
                          label="Kondisi")
    asal_barang = SelectField(choices=get_list_alamat(), label="Asal")
    consumable = BooleanField("Consumable")
    submit = SubmitField('Submit')


class InventoryDefaultForm(FlaskForm):
    keyword = StringField('')
    submit = SubmitField('Cari')
    showall = SubmitField('Show All')


class InventoryTglterimaForm(FlaskForm):
    keyword = DateField("", id='datepick', format="%m/%d/%Y")
    submit = SubmitField('Submit')
    showall = SubmitField('Show All')


class InventoryTypebarangForm(FlaskForm):
    keyword = SelectField(choices=get_list_typebarang(), label="")
    submit = SubmitField('Submit')
    showall = SubmitField('Show All')


class InventoryKondisiForm(FlaskForm):
    # keyword = SelectField(choices=[('True', 'Baik'), ('False', 'Rusak')],
    #                      label="Cari Berdasarkan Kondisi")
    keyword = BooleanField(" Centang kalo cari yang kondisinya Baik.")
    submit = SubmitField('Submit')
    showall = SubmitField('Show All')


class InventoryAsalForm(FlaskForm):
    keyword = SelectField(choices=get_list_alamat(), label="")
    submit = SubmitField('Submit')
    showall = SubmitField('Show All')


class InventoryConsumableForm(FlaskForm):
    keyword = BooleanField(" Centang kalo cari yang consumable")
    submit = SubmitField('Submit')
    showall = SubmitField('Show All')
