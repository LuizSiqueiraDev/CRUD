from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Livros(Base):
    "Tabela Livros"
    __tablename__ = 'livros'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    autor = Column(String)
    sinopse = Column(String)
    ranking = Column(Integer)
    lido = Column(Boolean, default=False)
