from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.database import get_db
from backend.models import Booking, BookingStatus, User, Venue
from backend.routes.auth import get_current_user
from pydantic import BaseModel
from typing import Optional

class BookingCreate(BaseModel):
    artist_id: int
    venue_id: int
    event_id: Optional[int] = None
    start_time: datetime
    end_time: datetime
    price: float
    notes: Optional[str] = None

class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[BookingStatus] = None
    price: Optional[float] = None
    notes: Optional[str] = None

class BookingResponse(BaseModel):
    id: int
    artist_id: int
    venue_id: int
    event_id: Optional[int]
    start_time: datetime
    end_time: datetime
    status: BookingStatus
    price: float
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

router = APIRouter()

@router.post("/", response_model=BookingResponse)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    venue = db.query(Venue).filter(Venue.id == booking.venue_id).first()
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    db_booking = Booking(
        artist_id=booking.artist_id,
        venue_id=booking.venue_id,
        event_id=booking.event_id,
        start_time=booking.start_time,
        end_time=booking.end_time,
        price=booking.price,
        notes=booking.notes
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.get("/", response_model=list[BookingResponse])
def list_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bookings = db.query(Booking).offset(skip).limit(limit).all()
    return bookings

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking_id: int,
    booking_update: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    update_data = booking_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_booking, field, value)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db_booking.status = BookingStatus.CANCELLED
    db.commit()
    return {"message": "Booking cancelled successfully"}
