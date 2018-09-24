from app.models import Pengguna
from app import db

p = Pengguna(nama='admin', email='admin@gudang.com',uname = 'admin', passwd='admin', is_admin=True)
db.session.add(p)
db.session.commit()
