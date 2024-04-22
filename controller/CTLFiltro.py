import pandas as pd


def filtrar(df: pd.DataFrame, campos: list[str], filtro: list) -> pd.DataFrame:
    for campo in campos:
        df = df[df[campo].isin(filtro)]
    return df