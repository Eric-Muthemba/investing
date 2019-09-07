engine = create_engine("sqlite:///myexample.db")  # Access the DB Engine
if not engine.dialect.has_table(engine, Variable_tableName):  # If table don't exist, Create.
    metadata = MetaData(engine)
    # Create a table with the appropriate Columns
    Table(Variable_tableName, metadata,
          Column('Id', Integer, primary_key=True, nullable=False),
          Column('Date', Date), Column('Country', String),
          Column('Brand', String), Column('Price', Float),
    # Implement the creation
    metadata.create_all()

