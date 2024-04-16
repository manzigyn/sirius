from utils import pandas_files as pf
import pandas as pd
from model import DBJira as db
from dataclasses import dataclass, field
from utils import utilidades as ut
import math

@dataclass
class CTLJira():
    
    df_tickets : pd.DataFrame = field(default_factory = pd.DataFrame)
    dbJira : db.DBJira = field(default_factory=db.DBJira)
    
    def __init__(self, arquivo):
        self.df_tickets = self.importarDF(arquivo)
        self.tratarDF()
        self.dbJira = db.DBJira(self.df_tickets)
        
    def importarDF(self, arquivo) ->pd.DataFrame:
        df = pf.lerCsv(arquivo)
        return df
    
    def tratarDF(self): 
        self.df_tickets["Projeto"] = self.df_tickets["Issue key"].apply(lambda x: ut.extrairAteCaracter(x, "-"))
        self.df_tickets["Created Mes"] = self.df_tickets["Created"].apply(lambda x: ut.extrairAteCaracter(x, "/",1))
        self.df_tickets["Created Ano"] = self.df_tickets["Created"].apply(lambda x: ut.extrairAno(ut.extrairAteCaracter(x, "/",2)))
        self.df_tickets["Updated Mes"] = self.df_tickets["Updated"].apply(lambda x: ut.extrairAteCaracter(x, "/",1))
        self.df_tickets["Updated Ano"] = self.df_tickets["Updated"].apply(lambda x: ut.extrairAno(ut.extrairAteCaracter(x, "/",2)))
        self.df_tickets["Time to first response"] = self.df_tickets["Custom field (Time to first response)"].apply(lambda x: ut.categorizarColuna(x,"-","✅","❌"))
        self.df_tickets["Time to resolution"] = self.df_tickets["Custom field (Time to resolution)"].apply(lambda x: ut.categorizarColuna(x,"-","✅","❌"))
        self.df_tickets["Internal priority"] = self.df_tickets["Custom field (Internal priority)"].apply(lambda x: " " if math.isnan(x) else x)

    def obterListaProjetos(self) -> list:
        return self.df_tickets["Projeto"].unique()
    
    def obterListaCampos(self) -> list:
        lista =self.df_tickets.columns.tolist()
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
        lista.remove("Components_1")
        lista.remove("Components_2")
        lista.remove("Issue id")
        lista.remove("Summary")
        lista.remove("Assignee Id")
        return lista
    
    def __agrupar(self, df: pd.DataFrame, coluna: list[str], porcentagem: bool = True) -> pd.DataFrame:
        registros = len(df.index)
        df_resultado = df.groupby(coluna).size().reset_index(name='Quantidade')
        if porcentagem:
            df_resultado["%"] = (df_resultado["Quantidade"] / registros) *100
            df_resultado["%"] = df_resultado["%"].apply(lambda x: ut.formatarPorcentagem(x))
        
        return df_resultado
    
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
                
                
        return self.__agrupar(df, lista, porcentagem)
    
    def filtrarProjetos(self, filtro: list) -> pd.DataFrame:
        df = self.df_tickets[self.df_tickets["Projeto"].isin(filtro)]
        return df
    
    def obterProjetoBrasil(self) -> list:
        return ["MERZBRA","KSSTORZBR","SCHUTZBR","TURCKBR"]
    
    def obterProjetoLATAM(self) -> list:
        return ["MERZMXBR","MERZARG","MERZCOL","SCHUTZMX","KLUBERCHEM","SIGMX","OERLIKONMX"]

    def consultarTodos(self) -> pd.DataFrame:
        return self.dbJira.consultarTodos()
    
    def consultarQtdeTodos(self) -> pd.DataFrame:
        return self.dbJira.obterQtdeTodos()
    
    def consultarQtdeIssueType(self) -> pd.DataFrame:
        return self.dbJira.obterQtdeIssueType()
    
    def consultarQtdeIssueType_Projeto(self) -> pd.DataFrame:
        return self.dbJira.obterQtdeIssueType_Projeto()