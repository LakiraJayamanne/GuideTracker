import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from pydantic import BaseModel
from backend.database import create_db_and_tables, get_session
from backend.models import Position
from backend.geofence import haversine
from backend.checkins import checkin_zones



#app stuff
app = FastAPI()
class PositionIn(BaseModel):
    latitude: float
    longitude: float

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def home():
    return {"message": "Welcome to the GuideTracker!"}

@app.get("/checkin")
def checkin():
    return {"message": "This is where guides will check in."}

@app.post("/api/positions")
def create_position(position: PositionIn, session: Session = Depends(get_session)):
    # Default state
    state = "TRAVELLING"
    zone_name = None

    # Check against all zones
    for zone in checkin_zones:
        dist = haversine(position.latitude, position.longitude, zone["latitude"], zone["longitude"])
        if dist <= zone["radius_m"]:
            state = "AWAITING_CHECKIN"
            zone_name = zone["name"]
            break

    pos = Position(
        latitude=position.latitude,
        longitude=position.longitude,
        state=state
    )
    session.add(pos)
    session.commit()
    session.refresh(pos)

    return {
        "id": pos.id,
        "latitude": pos.latitude,
        "longitude": pos.longitude,
        "timestamp": pos.timestamp,
        "state": pos.state,
        "zone": zone_name
    }
    
@app.get("/api/positions/latest")
def get_latest_position(session: Session = Depends(get_session)):
    statement = select(Position).order_by(Position.id.desc()).limit(1)
    result = session.exec(statement).first()
    return result

@app.get("/map")
def get_map():
    path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    return FileResponse(os.path.abspath(path))

@app.post("/api/checkin")
def checkin(session: Session = Depends(get_session)):
    statement = select(Position).order_by(Position.id.desc()).limit(1)
    pos = session.exec(statement).first()
    
    if not pos:
        raise HTTPException(status_code=400, detail="No position found to check in.")
    
    if pos.state != "AWAITING_CHECKIN":
        raise HTTPException(status_code=400, detail="Position not in a check-in zone.")
    
    pos.state = "CHECKED_IN"
    session.add(pos)
    session.commit()
    session.refresh(pos)
    
    return {
        "message": "Successfully checked in.",
        "position_id": pos.id,
        "timestamp": pos.timestamp
    }
    
