from dataclasses import dataclass
import pandas as pd
import duckdb

@dataclass
class DBJira:
    
    def __init__(self, df: pd.DataFrame) -> None:
        self.df_tickets = df
        
    def consultarTodos(self) -> pd.DataFrame:
        return duckdb.sql("SELECT * FROM self.df_tickets ").df() 