from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import  declarative_base
engine = create_engine("mysql://root:123456@10.7.243.110:3306/UIAUTO?charset=utf8",
                                    encoding='utf-8', echo=True,convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))



Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import  app.models
    Base.metadata.create_all(bind=engine)
