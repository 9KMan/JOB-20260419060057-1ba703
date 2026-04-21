from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.database import get_db
from backend.models import Event, EventType, User, Venue
from backend.routes.auth import get_current_user
from pydantic import BaseModel
from typing import Optional

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    event_type: EventType = EventType.CONCERT
    venue_id: int
    start_time: datetime
    end_time: datetime
    expected_attendees: Optional[int] = None
    ticket_price: Optional[float] = None

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[EventType] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    expected_attendees: Optional[int] = None
    ticket_price: Optional[float] = None
    is_published: Optional[bool] = None

class EventResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    event_type: EventType
    venue_id: int
    organizer_id: int
    start_time: datetime
    end_time: datetime
    expected_attendees: Optional[int]
    ticket_price: Optional[float]
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True

router = APIRouter()

@router.post("/", response_model=EventResponse)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    venue = db.query(Venue).filter(Venue.id == event.venue_id).first()
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    db_event = Event(
        title=event.title,
        description=event.description,
        event_type=event.event_type,
        venue_id=event.venue_id,
        organizer_id=current_user.id,
        start_time=event.start_time,
        end_time=event.end_time,
        expected_attendees=event.expected_attendees,
        ticket_price=event.ticket_price
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/", response_model=list[EventResponse])
def list_events(
    skip: int = 0,
    limit: int = 100,
    venue_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Event)
    if venue_id:
        query = query.filter(Event.venue_id == venue_id)
    events = query.offset(skip).limit(limit).all()
    return events

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    event_update: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    update_data = event_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted successfully"}
