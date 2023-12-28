import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import Client as SchemaClient
from schema import Employee as SchemaEmployee
from schema import ShiftReport as SchemaShiftReport
from schema import Invoice as SchemaInvoice
from schema import Payrun as SchemaPayrun
from schema import PayrunRecord as SchemaPayrunRecord


from models import Client as ModelClient
from models import Employee as ModelEmployee
from models import ShiftReport as ModelShiftReport
from models import Invoice as ModelInvoice
from models import Payrun as ModelPayrun

import os
from dotenv import load_dotenv
from typing import List
from sqlalchemy import desc, cast, DateTime
from sqlalchemy.sql import func
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime

load_dotenv('.env')


app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "hello world"}

# Client
@app.post('/client/', response_model=SchemaClient, tags=["Client"])
async def client(client: SchemaClient):
    db_client = ModelClient(name=client.name, age=client.age)
    db.session.add(db_client)
    db.session.commit()
    return db_client

@app.get('/client/', tags=["Client"])
async def client():
    all_client = db.session.query(ModelClient).all()
    return all_client


# Employee
@app.post('/employee/', response_model=SchemaEmployee, tags=["Employee"])
async def employee(employee:SchemaEmployee):
    db_employee = ModelEmployee(name=employee.name, age=employee.age)
    db.session.add(db_employee)
    db.session.commit()
    return db_employee

@app.get('/employee/', tags=["Employee"])
async def author():
    all_employee = db.session.query(ModelEmployee).all()
    return all_employee

# ShiftReport
@app.post('/shiftreport/', response_model=SchemaShiftReport, tags=["ShiftReport"])
async def shiftreport(shiftreport: SchemaShiftReport):
    db_shiftreport = ModelShiftReport(date = shiftreport.date, client_name = shiftreport.client_name, support_provider = shiftreport.support_provider,
                                       participants_welfare = shiftreport.participants_welfare, activity=shiftreport.activity)
    db.session.add(db_shiftreport)
    db.session.commit()
    return db_shiftreport

@app.get('/shiftreport/{report_id}', tags=['ShiftReport'])
async def single_shiftreport(report_id: int):
    report = db.session.query(ModelShiftReport).filter(ModelShiftReport.id == report_id).first()

    if report is None:
        raise HTTPException(status_code=404, detail="Shift report not found")

    result_dict = {
        "id": report.id,
        "date": report.date,
        "support_provider": report.support_provider,
        "client_name": report.client_name,
        "participants_welfare": report.participants_welfare,
        "activity": report.activity
    }

    return JSONResponse(content=result_dict)

@app.get('/shiftreport/all', tags=["ShiftReport"])
async def all_shiftreport():
    query = (
    db.session.query(ModelShiftReport.id, ModelShiftReport.client_name, ModelShiftReport.date, ModelShiftReport.support_provider)
    .order_by(desc(ModelShiftReport.time_created))
    )

    shift_reports = query.all()

    # Convert the results to a list of dictionaries for the response
    result_list = [
        {
            "id": report.id,
            "date": report.date,
            "support_provider": report.support_provider,
            "client": report.client_name,
        }
        for report in shift_reports
    ]

    total_count = db.session.query(func.count()).select_from(ModelShiftReport).scalar()

    return JSONResponse(content={"total": total_count, "results": result_list})

PAGE_SIZE = 30

@app.get("/page/shift_reports/", response_model=List[dict], tags=["ShiftReport"])
async def get_shift_reports(
    page: int = Query(1, ge=1),
    page_size: int = Query(PAGE_SIZE, ge=1),
):
    start_index = (page-1) * page_size
    end_index = start_index + page_size

    query = (
        db.session.query(ModelShiftReport.id, ModelShiftReport.client_name, ModelShiftReport.date, ModelShiftReport.support_provider)
        .order_by(desc(ModelShiftReport.time_created))
        .offset(start_index)
        .limit(page_size)
    )

    shift_reports = query.all()

    # Convert the results to a list of dictionaries for the response
    result_list = [
        {
            "id": report.id,
            "date": report.date,
            "support_provider": report.support_provider,
            "client": report.client_name,
        }
        for report in shift_reports
    ]

    total_count = db.session.query(func.count()).select_from(ModelShiftReport).scalar()

    return JSONResponse(content={"total": total_count, "results": result_list})





# Invoice
@app.post('/invoice/', response_model=SchemaInvoice, tags=["Invoice"])
async def invoice(invoice: SchemaInvoice):
    db_invoice = ModelInvoice(client = invoice.client, employee = invoice.employee, date = invoice.date, hours = invoice.hours,
                              travel_time = invoice.travel_time, travel_km = invoice.travel_km, remittance = invoice.remittance, invoice_num = invoice.invoice_num)
    db.session.add(db_invoice)
    db.session.commit()
    return db_invoice

@app.get('/invoice/', tags=["Invoice"])
async def invoice():
    all_invoice = db.session.query(ModelInvoice).all()
    return all_invoice

@app.get('/invoices', tags=["Invoice"])
def get_invoices(start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
                 end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
                 client: str = Query(None, description="Filter by client")):
    try:
        query = db.session.query(ModelInvoice).filter(
            ModelInvoice.date.between(start_date, end_date)
        )

        if client:
            query = query.filter(ModelInvoice.client == client)

        invoices = query.all()

        result = []
        for invoice in invoices:
            result.append({
                'id': invoice.id,
                'client': invoice.client,
                'employee': invoice.employee,
                'date': invoice.date,
                'hours': invoice.hours,
                'travel_time': invoice.travel_time,
                'travel_km': invoice.travel_km,
                'remittance': invoice.remittance,
                'shiftreport_id': invoice.shiftreport_id,
                'invoice_num': invoice.invoice_num,
            })

        return result

    except Exception as e:
        return {'error': str(e)}
    
@app.get('/invoices/employee', tags=["Invoice"])
def get_invoices_byemployee(start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
                 end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
                 employee: str = Query(None, description="Filter by employee")):
    try:
        query = db.session.query(ModelInvoice).filter(
            ModelInvoice.date.between(start_date, end_date)
        )

        if employee:
            query = query.filter(ModelInvoice.employee == employee)

        
        # Add an order_by clause to sort by date in ascending order
        query = query.order_by(ModelInvoice.date.asc())

        invoices = query.all()

        result = []
        for invoice in invoices:
            result.append({
                'id': invoice.id,
                'client': invoice.client,
                'employee': invoice.employee,
                'date': invoice.date,
                'hours': invoice.hours,
                'travel_time': invoice.travel_time,
                'travel_km': invoice.travel_km,
                'remittance': invoice.remittance,
                'shiftreport_id': invoice.shiftreport_id,
                'invoice_num': invoice.invoice_num,
            })

        return result

    except Exception as e:
        return {'error': str(e)}

# Payrun
@app.post('/payrun/', response_model=SchemaPayrun, tags=["Payrun"])
async def payrun(payrun: SchemaPayrun):
    db_payrun = ModelPayrun(employee = payrun.employee, total_hours = payrun.total_hours, total_km = payrun.total_km, date = payrun.date)
    db.session.add(db_payrun)
    db.session.commit()
    return db_payrun


@app.post("/store_payrun_data", tags=["Payrun"])
async def store_payrun_data(records: SchemaPayrunRecord):
    try:
        for record in records.records:
            db_record = ModelPayrun(
                employee=record.employee,
                date=record.date,
                total_hours=record.total_hours,
                total_km=record.total_km,
                total_remittance=record.total_remittance,
            )
            db.session.add(db_record)
        db.session.commit()
        return {"message": "Payrun data stored successfully"}
    except Exception as e:
        db.session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.session.close()

@app.get('/payrun/', tags=["Payrun"])
async def payrun():
    all_payrun = db.session.query(ModelPayrun).all()
    return all_payrun


@app.get('/payruns', tags=["Payrun"])
def get_payruns(start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
                 end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
                 employee: str = Query(None, description="Filter by client")):
    try:
        query = db.session.query(ModelPayrun).filter(
            ModelPayrun.date.between(start_date, end_date)
        )

        if employee:
            query = query.filter(ModelPayrun.employee == employee)

        payruns = query.all()

        result = []
        for payrun in payruns:
            result.append({
                'id': payrun.id,
                'employee': payrun.employee,
                'date': payrun.date,
                'total_hours': payrun.total_hours,
                'total_km': payrun.total_km,
            })

        return result

    except Exception as e:
        return {'error': str(e)}

class DataResponse(BaseModel):
    rows: List[dict]
    totalRows: int

fake_data = [
    {"id": i, "client": f"Client {i}", "date": f"12/{i % 12 + 1}/23", "support_provider": f"Provider {i}"}
    for i in range(1, 101)
]
@app.get("/api/data/", response_model=DataResponse)
async def get_data(
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=100),
):
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    total_rows = len(fake_data)
    data_for_page = fake_data[start_idx:end_idx]

    return {"rows": data_for_page, "totalRows": total_rows}


# Shift & Incoive insert toegther
@app.post('/api/shift_invoice', tags=["Shift Report+Incoive"])
async def create_report_and_incoive(shiftreport: SchemaShiftReport, invoice:SchemaInvoice):
        try:
            #Create data in Shift Report
            db_shiftreport = ModelShiftReport(date = shiftreport.date, client_name = shiftreport.client_name, support_provider = shiftreport.support_provider,
                                        participants_welfare = shiftreport.participants_welfare, activity=shiftreport.activity)
            db.session.add(db_shiftreport)
            db.session.commit()
            db.session.refresh(db_shiftreport)

            #Create data in Incoive 
            db_invoice = ModelInvoice(client = invoice.client, employee = invoice.employee, date = invoice.date, hours = invoice.hours,
                              travel_time = invoice.travel_time, travel_km = invoice.travel_km,
                                remittance = invoice.remittance, invoice_num = invoice.invoice_num, shiftreport_id = db_shiftreport.id)
            db.session.add(db_invoice)
            db.session.commit()
            db.session.refresh(db_invoice)
        except Exception as e:
            db.session.rollback()
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

        finally:
            db.session.close()

        return {"message": "Data created successfully"}
# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)


