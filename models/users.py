
from .db import Column, PkModel, db

class Users(PkModel):

    __tablename__ = "users"
    
    user_id = Column(db.String(), nullable=True, default='', unique=True)
    name = Column(db.String(), nullable=True, default='')
    email_address = Column(db.String(), nullable=True, default='')
    phone_number = Column(db.String(), nullable=True, default='')
    username = Column(db.String(), nullable=True, default='', unique=True)
    password = Column(db.String(), nullable=True, default='')
    type_user = Column(db.String(), nullable=True, default='')

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if commit:
            return self.save()
        return self

    def save(self, commit=True):
        """Save the record."""
        try:
            db.session.add(self)
            if commit:
                db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return None
        return self
    
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def delete(self, commit: bool = True) -> None:
        """Remove the record from the database."""
        try:
            db.session.delete(self)
            if commit:
                return db.session.commit()
        except Exception:
            db.session.rollback()
        return
    
    def __repr__(self):
        """Represent instance as a unique string."""
        return f"{self.id}"

class db_users_query(object):
    @staticmethod
    def get_user_data(username):
        order = Users.query.filter(Users.username == username).first()
        return order