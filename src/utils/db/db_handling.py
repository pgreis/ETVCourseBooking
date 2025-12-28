import pandas as pd
from sqlalchemy import create_engine, exc

from logger import get_logger

class DatabaseHandler():
   
    def __init__(self, db_url:str, table_name:str="etv_courses", logger=None):
            self.table_name = table_name
            self.default_table_name = f"{self.table_name}_default_table"
            self.db_url = db_url
            self.engine = create_engine(self.db_url)
            self.logger = logger or get_logger(__name__)
        
            try:
                self.engine.connect()
                self.logger.info("Database engine initialised successfully.")
            except exc.SQLAlchemyError as err:
                self.logger.error("engine initialisation error: ", err)

    def create_default_table(self):
        default_table = pd.DataFrame({"weekday": ["Mo", "Di", "Mi", "Do", "Fr"] * 2,
                                      "person": ["X", "Y"] * 5,
                                      "orig_course_name": ["Kurs A", "Kurs B", "Kurs C", "Kurs D", "Kurs E"] * 2,
                                      "is_registration_active": True})
        self.post_table(table=default_table,
                        table_name=self.default_table_name)

        self.default_table = default_table

    def load_table(self,table_name:str):
        self.loaded_table = pd.read_sql(f"SELECT * FROM {table_name}", self.engine)
            
    def post_table(self, table:pd.DataFrame, table_name:str):
        table.to_sql(name=table_name, con=self.engine, if_exists='replace', index=False)


