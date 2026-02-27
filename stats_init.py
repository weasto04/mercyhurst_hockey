from sqlmodel import Session
from models import engine
from stats_data import load_stats_from_csv

with Session(engine) as session:
    stats = load_stats_from_csv()
    session.add_all(stats)
    session.commit()
