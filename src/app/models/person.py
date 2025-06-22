import uuid

from pydantic import EmailStr
from sqlmodel import Field
from .common import SQLBase
from app.helpers.encrypt_decrypt import encrypt, decrypt, hmac_value


class PersonBase(SQLBase):
    name_first: str = Field(alias="first_name")
    name_last: str = Field(alias="last_name")
    e_mail: EmailStr = Field(alias="email", unique=True)
    first_name_hmac: str
    last_name_hmac: str
    email_hmac: str

    @property
    def first_name(self):
        return decrypt(self.name_first)

    @first_name.setter
    def first_name(self, value):
        self.name_first = encrypt(value)
        self.first_name_hmac = hmac_value(value)

    @property
    def last_name(self):
        return decrypt(self.name_last)

    @last_name.setter
    def last_name(self, value):
        self.name_last = encrypt(value)
        self.last_name_hmac = hmac_value(value)

    @property
    def email(self):
        return decrypt(self.e_mail)

    @email.setter
    def email(self, value):
        self.e_mail = encrypt(value)
        self.email_hmac = hmac_value(value)


class Person(PersonBase, table=True):
    __tablename__: str = 'person'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)


class PersonCreate(PersonBase):
    pass