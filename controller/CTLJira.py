from utils import pandas_files as pf
import pandas as pd
from model import DBJira as db
from dataclasses import dataclass, field


@dataclass
class CTLJira():
    
    df_tickets : pd.DataFrame = field(default_factory = pd.DataFrame)
    
    def __init__(self, arquivo):
        self.df_tickets = self.importarDF(arquivo)
        
    def importarDF(self, arquivo) ->pd.DataFrame:
        df = pf.lerCsv(arquivo)
        return df

    def consultarTodos(self) -> pd.DataFrame:
        return db.DBJira(self.df_tickets).consultarTodos()