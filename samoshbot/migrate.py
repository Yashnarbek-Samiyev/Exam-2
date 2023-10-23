from db import Base
from db import engine
Base.metadata.create_all(engine)
