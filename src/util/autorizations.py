from fastapi import HTTPException, Header
from decouple import config



def verify_key_and_user(key: str = Header(None), userId: str = Header(None)):
    valid_key = config('API_PASSWORD')
    valid_user_id = config('API_USER')
    if key != valid_key or userId != valid_user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return key, userId
