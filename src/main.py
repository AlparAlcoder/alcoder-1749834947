from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Event(BaseModel):
    id: int
    name: str
    location: str
    date: str


events = []


@app.get("/events/", response_model=List[Event])
async def read_events():
    """Return a list of all events"""
    return events


@app.get("/events/{event_id}", response_model=Event)
async def read_event(event_id: int):
    """Return a single event by id"""
    for event in events:
        if event.id == event_id:
            return event
    raise HTTPException(status_code=404, detail="Event not found")


@app.post("/events/", response_model=Event)
async def create_event(event: Event):
    """Create a new event"""
    events.append(event)
    return event


@app.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    """Update an existing event"""
    for index, stored_event in enumerate(events):
        if stored_event.id == event_id:
            events[index] = event
            return event
    raise HTTPException(status_code=404, detail="Event not found")


@app.delete("/events/{event_id}")
async def delete_event(event_id: int):
    """Delete an event"""
    for index, event in enumerate(events):
        if event.id == event_id:
            events.pop(index)
            return {"message": "Event has been deleted successfully."}
    raise HTTPException(status_code=404, detail="Event not found")