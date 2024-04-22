from utils import pandas_files as pf
import pandas as pd
from model import DBJira as db
from dataclasses import dataclass, field
from utils import utilidades as ut
import math
from controller import CTLApoio

@dataclass
class CTLCoffeeCup():
    
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
        #self._df_tickets["Projeto"] = self._df_tickets["Project"].apply(lambda x: ut.extrairAteCaracter(x, "-"))
        self._df_tickets["Date Ano"] = self._df_tickets["Date"].apply(lambda x: ut.extrairAteCaracter(x, "-",1))
        self._df_tickets["Date Mes"] = self._df_tickets["Date"].apply(lambda x: ut.extrairAno(ut.extrairAteCaracter(x, "-",2)))

    def obterListaProjetos(self) -> list:
        return self._df_tickets["Project"].apply(lambda x: str(x).strip()).unique()
    
    def obterListaTask(self) -> list:
        return self._df_tickets["Task"].unique()

    def obterListaCampos(self) -> list:
        lista =self._df_tickets.columns.tolist()
        lista.remove("Date Mes")
        lista.remove("Date Ano")
        return lista

    def obterListaTaskPresales(self, lista: list) -> list:
        manter = ["Pre-Sales Activities"]
        return CTLApoio.manterLista(manter, lista)
    
    def obterListaTaskProduct(self, lista: list) -> list:
        manter = ["PROD - TAX ONE"]
        return CTLApoio.manterLista(manter, lista)
    
    def obterListaCamposInicial(self) -> list:
        lista = self.obterListaCampos()
        manter = ["Project","Staff","Reference ID"]
        return CTLApoio.manterLista(manter, lista)
   
    
    def agruparCampo(self, df: pd.DataFrame, campos: list[str], porcentagem: bool = True) -> pd.DataFrame:
        lista = campos
        for valor in ["Date"]:
            if valor in campos:
                campos.extend([f"{valor} Mes", f"{valor} Ano"])
                campos.remove(valor)
        
                
        return CTLApoio.agrupar(df, lista, porcentagem)
    
    def filtrar(self, filtro: list) -> pd.DataFrame:
        return CTLApoio.filtrar(self._df_tickets, campos=["Project","Task"], filtro=filtro)
    
    def obterProjetoPresales(self) -> list:
        return ["Internal Management & Presales"]
    
    def obterProjetoProduct(self) -> list:
        return ["Product Management"]

    def obterProjetoSupport(self) -> list:
        return ["Internal Support Management"]

    def obterProjetoPadrao(self) -> list:
        return ["Internal Support Management","Schütz - Brazil Ongoing Support","Turck - Brazil Support","Merz - Brazil Support","STORZ Brazil Support","Brazil (BRI) Dunning Process","Brazil (BRI) New Company Code - Merz Hauz","Merz - Argentina Support","Oerlikon Support Mexico","Merz - Colombia Support","Schütz - Mexico Ongoing Support","Merz - Mexico Support","Product Management","Klüber/Chemtrend Mex Support","Sig (BRI) Mexico Support"]
    
    def obterProjetoTodosExcetoInteralProject(self) -> list:
        lista = self.obterListaProjetos()
        remover = self.obterProjetoPresales() + self.obterProjetoProduct() + self.obterProjetoSupport()
        return CTLApoio.removerLista(remover, lista)

    def consultarTodos(self) -> pd.DataFrame:
        return self._dbJira.consultarTodos()
    
    def consultarQtdeTodos(self) -> pd.DataFrame:
        return self._dbJira.obterQtdeTodos()
    
    def consultarQtdeIssueType(self) -> pd.DataFrame:
        return self._dbJira.obterQtdeIssueType()
    
    def consultarQtdeIssueType_Projeto(self) -> pd.DataFrame:
        return self._dbJira.obterQtdeIssueType_Projeto()