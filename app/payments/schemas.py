from pydantic import BaseModel, Field, field_validator
import re

class Payer(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    document: str = Field(min_length=11, max_length=14) 

    @field_validator("document")
    @classmethod
    def document_digits_only(cls, v: str) -> str:
        digits = re.sub(r"\D+", "", v)
        if len(digits) not in (11, 14):
            raise ValueError("document must have 11 (CPF) or 14 (CNPJ) digits")
        return digits


class PaymentCreate(BaseModel):
    amount_cents: int = Field(gt=0, lt=10_000_000)  
    currency: str = Field(min_length=3, max_length=3)
    payer: Payer
    description: str | None = Field(default=None, max_length=140)
    idempotency_key: str = Field(min_length=8, max_length=120)

    @field_validator("currency")
    @classmethod
    def currency_upper(cls, v: str) -> str:
        return v.upper()
