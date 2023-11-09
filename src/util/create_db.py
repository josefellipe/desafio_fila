from fastapi import APIRouter, HTTPException
from ..database.connection import DatabaseManager

create_db_route = APIRouter()

@create_db_route.get("/create_tables_db/")
async def create_attendant():
    try:
        db_manager = DatabaseManager()
        db_manager.create_tables()
        return {"message": "Tables created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
