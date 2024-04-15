from utils import pandas_files as pf
import pandas as pd
from model import DBJira as db
from dataclasses import dataclass, field


@dataclass
class CTLJira():
    
    df_tickets : pd.DataFrame = field(default_factory = pd.DataFrame)
    dbJira : db.DBJira = field(default_factory=db.DBJira)
    
    def __init__(self, arquivo):
        self.df_tickets = self.importarDF(arquivo)
        self.dbJira = db.DBJira(self.df_tickets)
        
    def importarDF(self, arquivo) ->pd.DataFrame:
        df = pf.lerCsv(arquivo)
        return df

    def consultarTodos(self) -> pd.DataFrame:
        return self.dbJira.consultarTodos()
    
    def consultarQtdeTodos(self) -> pd.DataFrame:
        return self.dbJira.obterQtdeTodos()
    
    def consultarQtdeIssueType(self) -> pd.DataFrame:
        return self.dbJira.obterQtdeIssueType()
    
    def consultarQtdeIssueType_Projeto(self) -> pd.DataFrame:
        return self.dbJira.obterQtdeIssueType_Projeto()