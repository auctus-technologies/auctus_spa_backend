from ninja import Schema
from typing import Optional


class AddressSchema(Schema):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None


class BankDetailsSchema(Schema):
    account_number: Optional[str] = None
    bank_name: Optional[str] = None
    ifsc_code: Optional[str] = None
