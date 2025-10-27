from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from backend.database import create_db_and_tables, get_session
from backend.models import Position
from pydantic import BaseModel
from backend.geofence import haversine
import os

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
    last = session.exec(
        select(Position).order_by(Position.timestamp.desc()).limit(1)
    ).first()
    
    #default to AWAITING_CHECKIN if no previous position
    state = "AWAITING_CHECKIN"
    distance = 0.0
    
    if last:
        distance = haversine(last.latitude, last.longitude, position.latitude, position.longitude)
        if distance > 50: #meters
            state = "TRAVELLING"
        
    #create new position with computed state
    pos = Position(
        latitude = position.latitude,
        longitude = position.longitude,
        state=state #calculate later
    )
    session.add(pos)
    session.commit()
    session.refresh(pos)
    
    #return extra info
    return {
        "id": pos.id,
        "latitude": pos.latitude,
        "longitude": pos.longitude,
        "timestamp": pos.timestamp,
        "state": pos.state,
        "distance_from_last": round(distance, 2)
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