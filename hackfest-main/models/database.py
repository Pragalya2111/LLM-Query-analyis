from langchain.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain.utilities import SQLDatabase
 


import lancedb
import pyarrow as pa
import os



def get_connection():
    
    uri = "data/lancedb"
    db = lancedb.connect(uri)

    schema = pa.schema([
        # pa.field("id", pa.int64()),
        # pa.field("data", pa.string()),
        pa.field("vector", pa.list_(pa.float32(),384))
    ])
    
    if not os.path.exists(f"{uri}/sample.lance"):
        collection = db.create_table("sample", schema=schema)
    else:
        collection = db.open_table("sample")
    

    return collection
 
class Database:
    def __init__(self,db_path):

       self.db = SQLDatabase.from_uri(f"sqlite:///{db_path}", sample_rows_in_table_info=3)

    def get_db(self):
    
        return self.db