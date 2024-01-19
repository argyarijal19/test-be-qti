import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

def db_conn():
    username = os.getenv('DB_USERNAME')
    password  = os.getenv('DB_PASSWORD')
    host = os.getenv("DB_HOST")
    port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    engine = create_engine(
        f'mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

