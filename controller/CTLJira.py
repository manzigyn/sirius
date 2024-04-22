from utils import pandas_files as pf
import pandas as pd
from model import DBJira as db
from dataclasses import dataclass, field
from utils import utilidades as ut
import math
from controller import CTLApoio

@dataclass
class CTLJira():
    
    _df_tickets : pd.DataFrame = field(default_factory = pd.DataFrame)
    _dbJira : db.DBJira = field(default_factory=db.DBJira)
    
    def __init__(self, arquivo, delimitador: str=',', enconder: str = 'utf-8'):
        self._delimitador = delimitador
        self._enconder = enconder
        self._df_tickets = self.importarDF(arquivo)
        self.tratarDF()
        self._dbJira = db.DBJira(self._df_tickets)
        
    def importarDF(self, arquivo) ->pd.DataFrame:
        df = pf.lerCsv(arquivo, self._delimitador, self._enconder)
        return df
    
    def tratarDF(self): 
        self._df_tickets["Projeto"] = self._df_tickets["Issue key"].apply(lambda x: ut.extrairAteCaracter(x, "-"))
        self._df_tickets["Created Mes"] = self._df_tickets["Created"].apply(lambda x: ut.extrairAteCaracter(x, "/",1))
        self._df_tickets["Created Ano"] = self._df_tickets["Created"].apply(lambda x: ut.extrairAno(ut.extrairAteCaracter(x, "/",2)))
        self._df_tickets["Updated Mes"] = self._df_tickets["Updated"].apply(lambda x: ut.extrairAteCaracter(x, "/",1))
        self._df_tickets["Updated Ano"] = self._df_tickets["Updated"].apply(lambda x: ut.extrairAno(ut.extrairAteCaracter(x, "/",2)))
        self._df_tickets["Time to first response"] = self._df_tickets["Custom field (Time to first response)"].apply(lambda x: ut.categorizarColuna(x,"-","✅","❌"))
        self._df_tickets["Time to resolution"] = self._df_tickets["Custom field (Time to resolution)"].apply(lambda x: ut.categorizarColuna(x,"-","✅","❌"))
        self._df_tickets["Internal priority"] = self._df_tickets["Custom field (Internal priority)"].apply(lambda x: " " if math.isnan(x) else x)

    def obterListaProjetos(self) -> list:
        return self._df_tickets["Projeto"].unique()
    
    def obterListaCampos(self) -> list:
        lista =self._df_tickets.columns.tolist()
        lista.remove("Created Mes")
        lista.remove("Created Ano")
        lista.remove("Updated Mes")
        lista.remove("Updated Ano")
        lista.remove("Time to first response")
        lista.remove("Time to resolution")
        lista.remove("Internal priority")
        return lista

    
    def obterListaCamposInicial(self) -> list:
        lista = self.obterListaCampos()
        remover = ["Components_1","Components.1","Components_2","Components.2", "Issue id", "Summary", "Assignee Id"]
        return CTLApoio.removerLista(remover, lista)
    
    
    
    def agruparCampo(self, df: pd.DataFrame, campos: list[str], porcentagem: bool = True) -> pd.DataFrame:
        lista = campos
        for valor in ["Created","Updated"]:
            if valor in campos:
                campos.extend([f"{valor} Mes", f"{valor} Ano"])
                campos.remove(valor)
        
        for valor in ["Custom field (Time to first response)","Custom field (Time to resolution)","Custom field (Internal priority)"]:
            if valor in campos:
                campos.extend([ut.extrairStringEntreCaracters(valor,"(",")")])
                campos.remove(valor)
                
                
        return CTLApoio.agrupar(df, lista, porcentagem)
    
    def filtrar(self, filtro: list) -> pd.DataFrame:        
        return CTLApoio.filtrar(self._df_tickets, campos=["Projeto"], filtro=filtro)
    
    def obterProjetoBrasil(self) -> list:
        return ["MERZBRA","KSSTORZBR","SCHUTZBR","TURCKBR"]
    
    def obterProjetoLATAM(self) -> list:
        return ["MERZMXBR","MERZARG","MERZCOL","SCHUTZMX","KLUBERCHEM","SIGMX","OERLIKONMX"]

    def consultarTodos(self) -> pd.DataFrame:
        return self._dbJira.consultarTodos()
    
    def consultarQtdeTodos(self) -> pd.DataFrame:
        return self._dbJira.obterQtdeTodos()
    
    def consultarQtdeIssueType(self) -> pd.DataFrame:
        return self._dbJira.obterQtdeIssueType()
    
    def consultarQtdeIssueType_Projeto(self) -> pd.DataFrame:
        return self._dbJira.obterQtdeIssueType_Projeto()