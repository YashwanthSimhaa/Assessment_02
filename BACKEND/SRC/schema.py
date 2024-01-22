from pydantic import BaseModel,EmailStr
from datetime import datetime,date
from typing import Union
from enum import Enum

class Status(str,Enum):
    available = "available"
    booked = "booked"


class Seat(BaseModel):
    seat_no : str
    status : Status

class Movie(BaseModel):
    title : str
    genre : Union[str,None]
    current_date : date
    seats : list[Seat]


class Movie_Response(Movie):
    duration : int = 120
    Id : str 
    Days_After_Release : int 
    release_date : date = "2023-12-22"

class Payment(str,Enum):
    UPI = "UPI"
    CASH = "CASH"

class Booking(BaseModel):
    seat_no : str
    name : str
    email : EmailStr
    payment_method : Payment
    price : int 

class Update(BaseModel):
    seat_no : str
    name : Union[str,None] = None
    email : EmailStr
    payment_method : Union[Payment,None] = "UPI"
    price : Union[int,None] = None
    payment_status : Union[str,None] = None


class Booking_Response(Booking):
    Id : str
    payment_status : str = "confirmed"


class BOOK(BaseModel):
    isbn : int
    title : str
    author : str
    Publication_year : date
