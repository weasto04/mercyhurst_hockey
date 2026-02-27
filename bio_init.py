from sqlmodel import Session
from models import engine
from bio_data import load_bios_from_roster

with Session(engine) as session:
    bios = load_bios_from_roster()
    session.add_all(bios)
    session.commit()