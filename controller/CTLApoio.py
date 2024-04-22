import pandas as pd
from utils import utilidades as ut

def filtrar(df: pd.DataFrame, campos: list[str], filtro: list) -> pd.DataFrame:
    for campo in campos:
        df = df[df[campo].apply(lambda x: str(x).lower()).isin(list(map(lambda x: str(x).lower(), filtro)))]
    return df

def removerLista(remover: list, lista: list) -> list:
    lista = list(filter(lambda x: x not in remover, lista))
    return lista

def manterLista(manter: list, lista: list) -> list:
    lista = list(filter(lambda x: x in manter, lista))
    return lista

def agrupar(df: pd.DataFrame, coluna: list[str], porcentagem: bool = True) -> pd.DataFrame:
        registros = len(df.index)
        df_resultado = df.groupby(coluna).size().reset_index(name='Quantidade')
        df_resultado = df_resultado.sort_values('Quantidade',ascending=False) 
        if porcentagem:
            df_resultado["%"] = (df_resultado["Quantidade"] / registros) *100
            df_resultado["%"] = df_resultado["%"].apply(lambda x: ut.formatarPorcentagem(x))
        
        return df_resultado