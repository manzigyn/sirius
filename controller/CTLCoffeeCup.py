from utils import pandas_files as pf
import pandas as pd
from model import DBJira as db
from dataclasses import dataclass, field
from utils import utilidades as ut
import math
from controller import CTLFiltro

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
        return self._df_tickets["Project"].unique()
    
    def obterListaTask(self) -> list:
        return self._df_tickets["Task"].unique()

    def obterListaCampos(self) -> list:
        lista =self._df_tickets.columns.tolist()
        lista.remove("Date Mes")
        lista.remove("Date Ano")
        return lista

    
    def obterListaCamposInicial(self) -> list:
        lista = self.obterListaCampos()
        manter = ["Project","Staff","Reference ID"]
        lista = list(filter(lambda x: x in manter, lista))
        
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
        for valor in ["Date"]:
            if valor in campos:
                campos.extend([f"{valor} Mes", f"{valor} Ano"])
                campos.remove(valor)
        
                
        return self.__agrupar(df, lista, porcentagem)
    
    def filtrar(self, filtro: list) -> pd.DataFrame:
        return CTLFiltro.filtrar(self._df_tickets, campos=["Project","Task"], filtro=filtro)
    
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