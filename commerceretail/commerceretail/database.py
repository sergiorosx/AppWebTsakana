from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////tmp/commerceretail5.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import commerceretail.models
    from commerceretail.models import Category
    from commerceretail.models import PaymentMethod
    Base.metadata.create_all(bind=engine)

    db_session.add(Category('Camisas'))
    db_session.commit()
    db_session.add(Category('Corbatas'))
    db_session.commit()
    db_session.add(Category('Pantalones'))
    db_session.commit()
    db_session.add(Category('Ropa Interior'))
    db_session.commit()
    db_session.add(Category('Zapatos'))
    db_session.commit()

    db_session.add(PaymentMethod('EFECTIVO'))
    db_session.commit()
    db_session.add(PaymentMethod('VISA'))
    db_session.commit()
    db_session.add(PaymentMethod('MASTERCARD'))
    db_session.commit()