import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

from database import db, create_document, get_documents
from schemas import Appointment, Consultation

app = FastAPI(title="Dentistry API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Dentistry API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Connected & Working"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# Appointment endpoints
@app.post("/api/appointments", status_code=201)
def create_appointment(payload: Appointment):
    try:
        inserted_id = create_document("appointment", payload)
        return {"id": inserted_id, "message": "Appointment request received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/appointments")
def list_appointments(service: Optional[str] = None, date_on: Optional[date] = None, limit: int = 50):
    try:
        filter_dict = {}
        if service:
            filter_dict["service"] = service
        if date_on:
            filter_dict["appointment_date"] = str(date_on)
        docs = get_documents("appointment", filter_dict=filter_dict, limit=limit)
        # Convert ObjectId to string if present
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Consultation endpoints
@app.post("/api/consultations", status_code=201)
def create_consultation(payload: Consultation):
    try:
        inserted_id = create_document("consultation", payload)
        return {"id": inserted_id, "message": "Consultation request received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/consultations")
def list_consultations(limit: int = 50):
    try:
        docs = get_documents("consultation", limit=limit)
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
