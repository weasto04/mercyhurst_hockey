from sqlmodel import Session
from models import Engine
from bio_data import load_bios_from_roster

with Session(Engine) as session:
    bios = load_bios_from_roster()
    session.add_all(bios)
    session.commit()