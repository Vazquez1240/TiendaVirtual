from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('''sqlite:///database/tienda.db''', connect_args={'check_same_thread':False})

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()