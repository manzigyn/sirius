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

        totalPorcentagem = 0
        if porcentagem:
            df_resultado["%"] = (df_resultado["Quantidade"] / registros) *100
            totalPorcentagem = ut.formatarPorcentagem(df_resultado["%"].sum())
            df_resultado["%"] = df_resultado["%"].apply(lambda x: ut.formatarPorcentagem(x))
         
        if len(coluna) == 1:
            df_resumo = {coluna[0] :"Total geral","Quantidade" : df_resultado["Quantidade"].sum()} if not porcentagem  else {coluna[0] :"Total geral","Quantidade" : df_resultado["Quantidade"].sum(),"%": totalPorcentagem}
        else:
            df_resumo = {coluna[0] :"Total geral", coluna[1]: " ", "Quantidade" : df_resultado["Quantidade"].sum()} if not porcentagem  else {coluna[0] :"Total geral", coluna[1]: " ", "Quantidade" : df_resultado["Quantidade"].sum(),"%": totalPorcentagem}
        df_resultado.loc[len(df_resultado)] = df_resumo

        
        return df_resultado