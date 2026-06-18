from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from datetime import datetime, timedelta

import json

from app.database import engine, get_db
from app.models import Base, URL
from app.schemas import URLRequest
from app.utils import encode_base62
from app.cache import redis_client


app = FastAPI(
    title="Scalable URL Shortener",
    version="1.0.0"
)

# ---------- CORS ----------

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

# ---------- Create tables ----------

Base.metadata.create_all(bind=engine)


# ---------- Home ----------

@app.get("/")

def home():

    return {

        "message":

        "Scalable URL Shortener API Running 🚀"

    }


# ---------- Shorten URL ----------

@app.post("/shorten")

def shorten_url(

    data: URLRequest,

    db: Session = Depends(get_db)

):

    # Duplicate URL detection

    existing = db.query(URL).filter(

        URL.original_url == str(data.url)

    ).first()

    if existing:

        return {

            "message":

            "URL already exists",

            "short_url":

            f"http://127.0.0.1:8000/{existing.short_code}"

        }

    expiry = None

    if data.expiry_days:

        expiry = datetime.utcnow() + timedelta(

            days=data.expiry_days

        )

    new_url = URL(

        original_url=str(data.url),

        expires_at=expiry

    )

    db.add(new_url)

    db.commit()

    db.refresh(new_url)

    # Custom Alias

    if data.custom_alias:

        alias_exists = db.query(URL).filter(

            URL.short_code == data.custom_alias

        ).first()

        if alias_exists:

            return {

                "message":

                "Custom alias already exists"

            }

        short_code = data.custom_alias

        new_url.is_custom = True

    else:

        short_code = encode_base62(

            new_url.id

        )

    new_url.short_code = short_code

    db.commit()

    return {

        "short_url":

        f"http://127.0.0.1:8000/{short_code}"

    }


# ---------- Redirect ----------

@app.get("/{short_code}")

def redirect_url(

    short_code: str,

    db: Session = Depends(get_db)

):

    url = db.query(URL).filter(

        URL.short_code == short_code

    ).first()

    if not url:

        return {

            "message":

            "URL not found"

        }

    # Expiry check

    if url.expires_at:

        if datetime.utcnow() > url.expires_at:

            return {

                "message":

                "URL expired"

            }

    url.clicks += 1

    db.commit()

    return RedirectResponse(

        url.original_url

    )


# ---------- Analytics + Redis ----------

@app.get("/analytics/{short_code}")

def analytics(

    short_code: str,

    db: Session = Depends(get_db)

):

    cache_key = f"analytics:{short_code}"

    cached_data = redis_client.get(

        cache_key

    )

    # If data exists in Redis

    if cached_data:

        return json.loads(

            cached_data

        )

    # Otherwise fetch from PostgreSQL

    url = db.query(URL).filter(

        URL.short_code == short_code

    ).first()

    if not url:

        return {

            "message":

            "URL not found"

        }

    result = {

        "original_url":

        url.original_url,

        "short_code":

        url.short_code,

        "clicks":

        url.clicks,

        "created_at":

        str(url.created_at),

        "expires_at":

        str(url.expires_at)

        if url.expires_at

        else None

    }

    # Store in Redis for 5 minutes

    redis_client.setex(

        cache_key,

        300,

        json.dumps(result)

    )

    return result