from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


def replace_null(value):
    if value is None:
        ret_value = ''
    else:
        ret_value = value
    return ret_value


class Pengguna(UserMixin, db.Model):
    __tablename__ = 'pengguna'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(60), index=True)
    email = db.Column(db.String(60), index=True, unique=True)
    uname = db.Column(db.String(60), default='')
    passwd_hash = db.Column(db.String(128))
    alamat = db.Column(db.String(60))
    peran_id = db.Column(db.Integer, db.ForeignKey('peranan.id'))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)

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
    nama = db.Column(db.String(128), index=True)
    tgl_terima = db.Column(db.Date)
    is_consumable = db.Column(db.Boolean, default=False)
    #type_id = db.Column(db.Integer, db.ForeignKey('typebarang.id'))
    typebarang = db.Column(db.String(64))
    serial = db.Column(db.String(128), unique=True)
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

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': replace_null(self.id),
            'Nama': replace_null(self.nama),
            'Tgl Terima': replace_null(dump_datetime(self.tgl_terima)[0]),
            'Consumable': replace_null(self.is_consumable),
            'Type': replace_null(self.typebarang),
            'Serial': replace_null(self.serial),
            'Qty': replace_null(self.qty),
            'Kondisi': replace_null(self.is_good),
            'Penempatan': replace_null(self.penempatan),
            'Keterangan': replace_null(self.keterangan),
            'Asal': replace_null(self.asal),
            'Tujuan': replace_null(self.tujuan)
        }


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
    keterangan = db.Column(db.String(256), default='')

#    def __repr__(self):
#        return '<Alamat: {}>'.format(self.nama_pic)


class ReqBarang(db.Model):
    __tablename__ = 'reqbarang'

    id = db.Column(db.Integer, primary_key=True)
    pengguna_id = db.Column(db.Integer)
    barang_id = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    tgl_terima = db.Column(db.Date)
    tgl_selesai = db.Column(db.Date)
    is_done = db.Column(db.Boolean, default=False)
    keterangan = db.Column(db.String(256), default='')


class TmpReqBarang(db.Model):
    __tablename__ = 'tmpreqbarang'

    id = db.Column(db.Integer, primary_key=True)
    pengguna_id = db.Column(db.Integer)
    barang_id = db.Column(db.Integer)
    qty = db.Column(db.Integer, default=1)
