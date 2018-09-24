"""
Th, [15.09.18 03:02]
::Barang masuk
No, Tanggal Diterima, consumable?, Part Type, Part Name, Serial Number, Quantity, Pengirim, Stat, Penempatan, Keterangan,  tersedia asal_barang, Tujuan_barang,

:: alamat
nama_pic alamat kota propinsi telpon Keterangan


::Request_barang
peminta(user) barang Qty Approved Approve_by done

:: user
uname pass level(1,2,3)  email
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Pengguna(UserMixin, db.Model):
    __tablename__ = 'pengguna'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(60), index=True)
    email = db.Column(db.String(60), index=True, unique=True)
    uname = db.Column(db.String(60), index=True, unique=True)
    passwd_hash = db.Column(db.String(128))
    peran_id = db.Column(db.Integer, db.ForeignKey('peranan.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def passwd(self):
        raise AttributeError('Password bukan untuk di pamerkan.')

    @passwd.setter
    def passwd(self, passwd):
        self.passwd_hash = generate_password_hash(passwd)

    def verify_passwd(self, passwd):
        return check_password_hash(self.passwd_hash, passwd)

    def __repr__(self):
        return '<Pengguna: {}>'.format(self.uname)


@login_manager.user_loader
def load_user(user_id):
    return Pengguna.query.get(int(user_id))


class Peran(db.Model):
    __tablename__ = 'peranan'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(60), unique=True)
    level = db.Column(db.Integer)
    deskripsi = db.Column(db.String(200))
    pengguna = db.relationship('Pengguna', backref='peran', lazy='dynamic')

    def __repr__(self):
        return '<Peran: {}>'.format(self.nama)


class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(128), index=True, unique=True)
    tgl_terima = db.Column(db.Date)
    is_consumable = db.Column(db.Boolean, default=False)
    #type_id = db.Column(db.Integer, db.ForeignKey('typebarang.id'))
    typebarang = db.Column(db.String(64))
    serial = db.Column(db.String(128))
    qty = db.Column(db.Integer)
    is_good = db.Column(db.Boolean, default=True)
    penempatan = db.Column(db.String(128))
    keterangan = db.Column(db.String(256))
    asal = db.Column(db.Integer)
    tujuan = db.Column(db.Integer)
#    asal = db.Column(db.Integer, db.ForeignKey('alamat.id'))
    #tujuan = db.Column(db.Integer, db.ForeignKey('alamat.id'))

    def __repr__(self):
        return '<Inventory: {}>'.format(self.nama)


class TypeBarang(db.Model):
    __tablename__ = 'typebarang'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(60))
    keterangan = db.Column(db.String(256))
    #inventory = db.relationship('Inventory', backref='typebarang', lazy='dynamic')

    def __repr__(self):
        return '<TypeBarang: {}>'.format(self.nama)


class Alamat(db.Model):
    __tablename__ = 'alamat'

    id = db.Column(db.Integer, primary_key=True)
    nama_pic = db.Column(db.String(60))
    alamat = db.Column(db.String(60))
#    inventory_ref = db.relationship('Inventory', backref='alamat', lazy='dynamic')
#    kota_id = db.Column(db.Integer, db.ForeignKey('kota.id'))
#    propinsi = db.Column(db.String(60))
#    negara = db.Column(db.String(60))
    keterangan = db.Column(db.String(60))

#    def __repr__(self):
#        return '<Alamat: {}>'.format(self.nama_pic)
        

#class Kota(db.Model):
#    __tablename__ = 'kota'
#    
#    id = db.Column(db.Integer, primary_key=True)
#    nama = db.Column(db.String(60))
#    alamat = db.relationship('Alamat', backref='kota', lazy='dynamic')
#    propinsi_id = db.Column(db.Integer, db.ForeignKey('propinsi.id'))
    
    
#class Propinsi(db.Model):
#    __tablename__ = 'propinsi'
#    
#    id = db.Column(db.Integer, primary_key=True)
#    nama = db.Column(db.String(60))
#    kota = db.relationship('Kota', backref='propinsi', lazy='dynamic')
#    negara_id = db.Column(db.Integer, db.ForeignKey('negara.id'))
    
    
#class Negara(db.Model):
#    __tablename__ = 'negara'
#    
#    id = db.Column(db.Integer, primary_key=True)
#    nama = db.Column(db.String(60))
#    propinsi = db.relationship('Propinsi', backref='negara', lazy='dynamic')
    
    

