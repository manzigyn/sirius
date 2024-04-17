import pandas as pd

def lerListaExcel(lista) -> pd.DataFrame:
    df = pd.concat(map(pd.read_excel, lista))
    #df = df.rename(str.lower, axis='columns')
    return df.dropna(how='all', axis=1)

def lerExcel(lista) -> pd.DataFrame:
    df = pd.read_excel(lista)
    #df = df.rename(str.lower, axis='columns')
    return df.dropna(how='all', axis=1)

def lerExcelTipado(lista, tipos) -> pd.DataFrame:
    df = pd.read_excel(lista, header=0, converters=tipos)
    #df = df.rename(str.lower, axis='columns')
    return df.dropna(how='all', axis=1)

def lerCsv(lista, delimitador: str=',', enconder: str = 'utf-8') -> pd.DataFrame:
    df = pd.read_csv(filepath_or_buffer=lista, delimiter=delimitador, encoding=enconder)
    #df = df.rename(str.lower, axis='columns')
    return df.dropna(how='all', axis=1)
