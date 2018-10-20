from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, \
    SubmitField, IntegerField, \
    BooleanField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from ..models import Alamat


class get_list_alamat(object):
    def __iter__(self):
        alamat = Alamat.query.all()
        list_alamat = []

        for a in alamat:
            #list_alamat.append((a.id, str(a.alamat)[:12]))
            pair = (a.id, str(a.nama_pic) + " ( " + str(a.alamat)[:12] + "... )")
            yield pair


class InventoryForm(FlaskForm):

    nama = StringField('Nama Barang', validators=[DataRequired()])
    tgl_terima = DateField("Tgl Terima", id='datepick', format="%m/%d/%Y")
    #typebarang = SelectField(label="Type Barang", choices=[])
    typebarang = StringField(label="Type Barang")
    serial = StringField("Serial")
    qty = IntegerField("Qty")
    kondisi = SelectField(choices=[('True', 'Baik'), ('False', 'Rusak')], label="Kondisi")
    asal_barang = SelectField(choices=get_list_alamat(), label="Asal")
    # asal_barang = QuerySelectField(query_factory=lambda:Alamat.query.all(),
    #                              get_label="nama_pic")
    #asal_barang = QuerySelectField(query_factory=lambda:Alamat.query.all(), get_label="nama_pic")
    consumable = BooleanField("Consumable")
    submit = SubmitField('Submit')


class AlamatForm(FlaskForm):
    nama_pic = StringField('Nama', validators=[DataRequired()])
    alamat = StringField('Alamat', validators=[DataRequired()])
    #kota = StringField('Kota')
    #propinsi = StringField('Propinsi')
    #negara = StringField('Negara', default='Indonesia')
    keterangan = StringField('Keteranan')
    submit = SubmitField('Submit')


class AlamatSelectForm(FlaskForm):
    keyword = SelectField(choices=get_list_alamat(), label="Pilih alamat tujuan ")
    as_submit = SubmitField('Next >> ')
