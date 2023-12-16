from fastapi import FastAPI, HTTPException, Body
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import os

# Configuration de la base de données PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


# Configuration de la table
class Film(Base):
    __tablename__ = "film"

    film_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    release_year = Column(Integer)
    language_id = Column(Integer, default=1)
    rental_duration = Column(Integer, default=3)
    rental_rate = Column(Float, default=4.99)
    length = Column(Integer)
    replacement_cost = Column(Float, default=19.99)
    last_update = Column(DateTime, default=func.now())
    special_features = Column(String)
    fulltext = Column(String)


app = FastAPI()


@app.get("/films")
async def get_films(skip: int = 0, limit: int = 10):
    # Création d'une session local relier au moteur instancié (engine)
    db = SessionLocal()
    # Query pour récupérer tous les films avec la class Film
    films = db.query(Film).offset(skip).limit(limit).all()
    # Fermeture de la session après l'éxécution de la requête
    db.close()
    return films


@app.get("/films/{film_id}")
async def get_film(film_id: int):
    db = SessionLocal()
    film = db.query(Film).filter(Film.film_id == film_id).first()
    db.close()
    if film is None:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    return film


@app.post("/films/")
async def create_film(payload: dict = Body(...)):
    db = SessionLocal()
    try:
        film = Film(
            title=payload.get("name"),
            description=payload.get("description"),
        )
        db.add(film)
        db.commit()
        db.refresh(film)
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Erreur lors de l'ajout du film")
    finally:
        db.close()
    return film
