from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base  = declarative_base()

class Client(Base):
    __tablename__ = 'client'
    id  = Column(Integer, primary_key=True, index=True) 
    name = Column(String)
    age = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

class ShiftReport(Base):
    __tablename__ = 'shiftreport'
    id = Column(Integer, primary_key=True)
    client_name = Column(String)
    date = Column(String)
    support_provider = Column(String)
    participants_welfare = Column(String)
    activity = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class Invoice(Base):
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True)
    shiftreport_id = Column(Integer)
    client = Column(String)
    employee = Column(String)
    date = Column(String)
    hours = Column(Float)
    travel_time = Column(Float)
    travel_km = Column(Integer)
    remittance = Column(Float)
    invoice_num = Column(String)
    serviceType = Column(String)
    notes = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

class Payrun(Base):
    __tablename__ = 'payrun'
    id = Column(Integer, primary_key=True)
    employee = Column(String)
    total_hours = Column(Float)
    total_km = Column(Integer)
    total_remittance = Column(Float)
    date = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())



