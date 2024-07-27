from database import Base
from sqlalchemy import Column,Integer,Date,String,Time,DateTime,Text,ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "Users"

    user_id = Column(Integer,primary_key = True)
    name = Column(String,nullable = False)
    email = Column(String, nullable = False)
    phone_number = Column(String, nullable = False)
    password = Column(String, nullable = False)
    registered_date = Column(DateTime, default = datetime.now(), nullable = False)
    role = Column(String, nullable = False, default = 'USER')

    events =  relationship('Event', back_populates = 'organizer')
    attendees = relationship('Attendee', back_populates = 'users')



class Event(Base):
    __tablename__ = "Events"

    event_id = Column(Integer, primary_key = True)
    event_name = Column(String, nullable = False)
    event_description = Column(Text, nullable = True)
    event_date = Column(Date, nullable = False)
    event_time = Column(Time, nullable = False)
    mode = Column(String, nullable = False)
    location = Column(Text, nullable = True)
    capacity = Column(Integer, nullable = False)
    status = Column(String, nullable = False, default = "PENDING")
    requested_timestamp = Column(DateTime, nullable = False, default=datetime.now())
    approved_timestamp = Column(DateTime, nullable = True)
    organizer_id = Column(Integer, ForeignKey('Users.user_id'), nullable = False)

    organizer = relationship('User', back_populates = 'events')
    event_attendees = relationship('Attendee', back_populates = 'events' )

class Attendee(Base):
    __tablename__ = "Attendees"

    attendee_id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable = False)
    attendee_name = Column(String, nullable = False)
    attendee_email = Column(String, nullable = False)
    attendee_phonenumber = Column(Integer, nullable = False)
    event_id =Column(Integer, ForeignKey("Events.event_id"), nullable = False)

    events = relationship('Event',back_populates = 'event_attendees')
    users = relationship('User', back_populates = 'attendees')
