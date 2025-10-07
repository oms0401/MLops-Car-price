from datetime import timedelta,timezone,datetime
from jose import jwt,JWTError

from app.core.config import setting

def create_token(data:dict,expire_minutes=30):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=expire_minutes)
    to_encode.update({'exp':expire})
    return jwt.encode(
        to_encode,
        setting.JWT_SECRET_KEY,
        algorithm=setting.JWT_ALGORITHM
    )

def verify_token(token :str):
    try:
        payload = jwt.decode(
            token,
            setting.JWT_SECRET_KEY,
            algorithms=[setting.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None