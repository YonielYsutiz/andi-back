from db_config import db

class Company(db.Model):
    __tablename__ = 'company'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nit = db.Column(db.String)
    name_company = db.Column(db.String)
    sector = db.Column(db.String)
    def __resp__(self):
        return "<Company %r>" % self.nit