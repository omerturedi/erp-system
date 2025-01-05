from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr

class CustomBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = None  # Her model kendi id'sini tanımlayacak

Base = declarative_base(cls=CustomBase) 