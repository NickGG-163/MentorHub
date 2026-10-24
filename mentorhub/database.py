from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg:///mentorhub", echo=True)
