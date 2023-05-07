
from .db import Column, PkModel, db

class Products(PkModel):

    __tablename__ = "products"
    
    item_id = Column(db.String(), nullable=True, default='', unique=True)
    item_name = Column(db.String(), nullable=True, default='', unique=True)
    quantity = Column(db.Integer(), default=0)
    description = Column(db.String(), nullable=True, default='')

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

class db_product_query(object):
    @staticmethod
    def get_product_item_name(item_name):
        product = Products.query.filter(Products.item_name == item_name).first()
        return product
    
    @staticmethod
    def get_all_item():
        product = Products.query.all()
        return product
    
    @staticmethod
    def get_product_item_id(item_id):
        product = Products.query.filter(Products.item_id == item_id).first()
        return product
    
    @staticmethod
    def update_product(kwargs):
        product = Products.query.filter(
            Products.item_name == kwargs['item_query_name']
            ).first().update(
                item_name=kwargs['item_name'],
                quantity=kwargs['quantity'],
                description=kwargs['description']
            )
        return product
    
    @staticmethod
    def delete_product(item_name):
        product = Products.query.filter(Products.item_name == item_name).first().delete()
        return product