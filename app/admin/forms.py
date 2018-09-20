from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, IntegerField, BooleanField, DateField
from wtforms.validators import DataRequired


class InventoryForm(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    tgl_terima = DateField("Tgl Terima")
    consumable = BooleanField("Consumable")
    typebarang = SelectField(label="Type Barang", choices=[])
    serial = StringField("Serial")
    qty = IntegerField("Qty")
    kondisi = SelectField(choices = [('True', 'Baik'), ('False', 'Rusak')] , label="Kondisi")
    asal_barang = SelectField(label="Asal", choices=[])
    submit = SubmitField('Submit')


class AlamatForm(FlaskForm):
    nama_pic = StringField('Nama', validators=[DataRequired()])
    alamat = StringField('Alamat', validators=[DataRequired()])
    kota = StringField('Kota')
    propinsi = StringField('Propinsi')
    negara = StringField('Negara', default='Indonesia')
    keterangan = StringField('Keteranan')
