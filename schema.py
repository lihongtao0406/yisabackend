# build a schema using pydantic
from pydantic import BaseModel
from typing import List

class Client(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True

class Employee(BaseModel):
    name:str
    age: int

    class Config:
        orm_mode = True

class ShiftReport(BaseModel):
    date: str
    client_name: str
    support_provider: str
    participants_welfare: str
    activity: str

    class Config:
        orm_mode = True

class Invoice(BaseModel):
    shiftreport_id: int
    client: str 
    employee: str 
    date: str 
    hours: float 
    travel_time: float 
    travel_km: int 
    remittance: float
    invoice_num: str 
    serviceType:str
    notes:str
    class Config:
        orm_mode = True

class Payrun(BaseModel):
    employee: str
    total_hours: float
    total_km: int
    total_remittance: float
    date: str
    class Config:
        orm_mode = True

class PayrunRecord(BaseModel):
    records: List[Payrun]