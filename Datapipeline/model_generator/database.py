from sqlalchemy import BigInteger, Column, Numeric, String, text , Table ,create_engine
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

class invest(object):
    def __init__(self):
        self.Base = declarative_base()
        self.MetaData = self.Base.metadata
        self.engine = create_engine("sqlite:///myexample.db")

    def create_table(self,Variable_tableName):
        # If table don't exist, Create.
        if not self.engine.dialect.has_table(self.engine,Variable_tableName):
            metadata = self.MetaData(self.engine)
            Table(Variable_tableName, metadata,
                    Column('id', BigInteger, primary_key=True, server_default=text("nextval('company_id_seq'::regclass)")),
                    Column('country', String(50), nullable=False),
                    Column('date', TIMESTAMP(precision=6), nullable=False),
                    Column('price', Numeric(10, 5), nullable=False),
                    Column('open', Numeric(10, 5), nullable=False),
                    Column('high', Numeric(10, 5), nullable=False),
                    Column('low', Numeric(10, 5), nullable=False),
                    Column('volume', BigInteger, nullable=False),
                    Column('change', Numeric(5, 4), nullable=False))
            # Implement the creation
            metadata.create_all()

