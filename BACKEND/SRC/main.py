from fastapi import FastAPI,HTTPException,status
from schema import Movie,Movie_Response,Booking,Booking_Response,Status,Update,BOOK
import json
import uuid
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime,date,timedelta
from typing import Optional

app = FastAPI()

path = "C:/Users/YBravish/Desktop/Assessment_02/BACKEND/RESPONSE/response.json"
path1 = "C:/Users/YBravish/Desktop/Assessment_02/BACKEND/RESPONSE/response1.json"
path2 = "C:/Users/YBravish/Desktop/Assessment_02/BACKEND/RESPONSE/response2.json"



def create_response_json(unique_id, data_dict, file_location):
    """
    Method to write responses to json file
    """
    try:
        with open(file_location, 'r') as file:
            existing_data = json.load(file)
    except Exception:
        existing_data = {}
    existing_data[unique_id] = data_dict
    try:
        with open(file_location, 'w') as file:
            json.dump(existing_data, file, indent=4)
        print(f"Data for unique ID {unique_id} has been written to {file_location}")
    except Exception as e:
        print(f"An error occurred while writing to {file_location}: {e}")
    return existing_data


@app.post("/movie-details/",response_model=Movie_Response,tags=["Movie Details"])
async def Movie_Details(details : Movie):
    data = jsonable_encoder(details)
    for i in range(len(data["seats"])):
        data["seats"][i]["status"] = "booked"
    data["duration"] = 120
    data["Id"] = str(uuid.uuid4())[0:5]
    d1 = date(2023,12,22)
    d2 = date.today()
    diff = d2 - d1
    data["Days_After_Release"] = diff.days
    data["release_date"] = "2023-12-22"
    create_response_json(data["Id"],data,path)
    return data
    
@app.post("/customer-booking/",response_model=Booking_Response,tags=["Customer Booking"])
async def Customer_Booking(details : Booking):
    data = jsonable_encoder(details)
    data["Id"] = str(uuid.uuid4())[0:5]
    data["payment_status"] = "confirmed"
    create_response_json(data["Id"],data,path1)
    return data 

@app.get("/get-all-movies/",tags=["Movie Details"])
async def get_all_movies():
    try:
        with open(path,"r") as file:
            data = json.load(file)
            return data
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="File Not Found")

@app.get("/get-seat-by-id/{id}",tags=["Customer Booking"])
async def get_seat_number_by_id(id : str):
    try :
        with open(path1,"r") as file:
            data = json.load(file)
            if id in data:
                seat_no = data[id]["seat_no"]
                return {"Seat Number" : seat_no}
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content="ID not Found")
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="File Not Found")
    
@app.delete("/delete-by-seat/{seat}",tags=["Customer Booking"])
async def delete_by_seat(seat : str):
    try :
        with open(path1,"r") as file:
            data = json.load(file)
            for key,value in data.items():
                if  seat in value["seat_no"]:
                    data.pop(key)
                    with open(path1,"w") as f1:
                        json.dump(data,f1,indent=4)  
                    return {"Data" : "Deleted Successfully"}
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content="ID not found")               
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="File Not Found")
                    
@app.get("/get-seat-id/{seat_id}",tags=["Customer Booking"])
async def get_by_seat_id(seat_id : str):
    try:
        with open(path1,"r") as file:
            data = json.load(file)
            if seat_id in data:
                return data[seat_id]
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content="ID not found")
    except Exception :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="File Not Found")
    

@app.get("/get-by-list/",tags=["Movie Details"])
async def get_by_list(STATUS : Status,Title : Optional[str] = None,Seat_no : Optional[str] = None,
                      offset : Optional[int] = None,limit : Optional[int] = 10):
    if offset is not None and offset<0:
        raise HTTPException(status_code=400,detail="offset cannot be negative")
    if limit is not None and limit<0:
        raise HTTPException(status_code=400,detail="limit cannot be negative")
    if offset is None:
        offset=0
    if limit is None:
        limit=0
    try:
        with open(path,"r") as file:
            data=json.load(file)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="file not found")
    exc_data=[]
    for key,value in data.items():
        json_title = value.get("title")
        for i in range(len(value.get("seats"))):
            json_seat = value.get("seats")[i]["seat_no"]

        if (Title == json_title or Title == None) and (Seat_no == json_seat or Seat_no == None) and (STATUS == "booked"):
            extracted = {
                "title" : value.get("title"),
                "genre" : value.get("genre"),
                "current_date" : value.get("current_date"),
                "seats" : value.get("seats"),
                "duration" : value.get("duration"),
                "Id" : value.get("Id"),
                "Days_After_Release" : value.get("Days_After_Release"),
                "release_date" : value.get("release_date")
            }
            exc_data.append(extracted)
    response=exc_data[offset:offset+limit]
    if not response or not exc_data:
        raise HTTPException(status_code=404,detail="no matching record found")
    return response


@app.patch("/update/{id}",tags=["Customer Booking"])
async def update_items(Id : str, details : Update):
    try:
        with open(path1,"r") as file:
            data = json.load(file)
            if Id in data:
                conv = jsonable_encoder(details)
                conv["Id"] = Id
                jname = data[Id]["name"]
                jpayment = data[Id]["payment_method"]
                jprice = data[Id]["price"]
                jpstatus = data[Id]["payment_status"]
                data[Id] = conv

                if data[Id]["name"] == None:
                    data[Id]["name"] = jname
                if data[Id]["payment_method"] == None:
                    data[Id]["payment_method"] == jpayment
                if data[Id]["price"] == None:
                    data[Id]["price"] = jprice
                if data[Id]["payment_status"] == None:
                    data[Id]["payment_status"] = jpstatus
                with open(path1,"w") as f1:
                    json.dump(data,f1,indent=4)
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content="ID not found")
        return data[Id]
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="File not Found")



@app.post("/create-book-data",tags=["Book Data"])
async def create_book_data(details : BOOK):
    data = jsonable_encoder(details)
    data["Id"] = str(uuid.uuid4())[0:5]
    create_response_json(data["Id"],data,path2)
    return data

@app.get("/get-by-id/{item_id}",tags=["Book Data"])
async def get_by_id(item_id : str):
    try:
        with open(path2,"r") as file:
            data = json.load(file)
            if item_id in data:
                return data[item_id]
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content="ID not found")
    except Exception :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="File Not Found")
    
@app.delete("/delete-by-id/{item_id}",tags=["Book Data"])
async def delete_by_id(item_id : str):
    try:
        with open(path2,"r") as file:
            data = json.load(file)
            if item_id in data:
                data.pop(item_id)
                with open(path2,"w") as f1:
                    json.dump(data,f1,indent=4)
                return {"Data" : "Deleted Successfully"}
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content="ID not found")
    except Exception :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="File Not Found")   
    
@app.get("/demo")
async def demo():
    pass
