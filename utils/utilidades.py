import datetime
import os
import shutil
import base64
import string
import streamlit as st
import time
import math
from datetime import datetime

global MESES_NOME
MESES_NOME = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

def moverListaArquivos(pasta_origem, pasta_destino, lista):
    for arquivo in lista:
        if not os.path.isfile(arquivo):
            origem = f'{pasta_origem}{arquivo}'
        else:
            origem = arquivo
            
        destino = arquivo.replace(pasta_origem, pasta_destino)
        try:
            shutil.move(origem, destino)
        except FileNotFoundError as error:
            print(f'{error}')
            
def moverArquivo(pasta_origem, pasta_destino, arquivo):
    if not os.path.isfile(arquivo):
        origem = f'{pasta_origem}{arquivo}'
    else:
        origem = arquivo
        
    destino = arquivo.replace(pasta_origem, pasta_destino)
    try:
        shutil.move(origem, destino)
    except FileNotFoundError as error:
        print(f'{error}')
        
def copiarArquivo(origem, destino):
    if os.path.isfile(origem):
        try:
            shutil.copyfile(origem, destino)
        except FileNotFoundError as error:
            print(f'{error}')        
        
def formatarMoedaReal(valor):
    return 'R$ {:,.2f}'.format(valor).replace(",", "X").replace(".", ",").replace("X", ".")

def formatarPorcentagem(valor):
    if math.isnan(valor):
        return "0,00%"
    return '{:,.2f}%'.format(valor).replace(",", "X").replace(".", ",").replace("X", ".")

def criarPasta(pasta):
    if not os.path.isdir(pasta):
        os.makedirs(pasta)
        

@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

def obterDataHoraCriacao(arquivo) -> string:
    try:
        ti_c = os.path.getctime(arquivo)
        return time.ctime(ti_c)
    except OSError:
        return datetime.now(tz=None)

def obterDataHoraModificacao(arquivo) -> string:
    try:
        ti_c = os.path.getmtime(arquivo)
        return time.ctime(ti_c)
    except OSError:
        return datetime.now(tz=None)
    
def obterNomeArquivo(arquivo) -> string:
    return os.path.basename(arquivo) if os.path.exists(arquivo) else ''

def formatarArquivoDataCriacao(arquivo) -> string:
    return f'{obterNomeArquivo(arquivo)} {obterDataHoraCriacao(arquivo)}'

def formatarArquivoDataModificacao(arquivo) -> string:
    return f'{obterNomeArquivo(arquivo)} {obterDataHoraModificacao(arquivo)}'

def tratarMoedaReal(valor: str)-> float:
    if isinstance(valor, str):
        try:
            if valor:
                valor = valor.replace("R$","").replace(",",".").replace(" ","")
                while valor.count(".") > 1:
                    valor = valor.replace(".","",1)
                return valor
            else:
                return 0.00
        except AttributeError:
            return 0.00
    else:
        if math.isnan(valor):
            return 0.00

        if isinstance(valor, float) or isinstance(valor, int):
            return valor
        
    
    
    

@st.cache_data
def get_base64_of_bin_file(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def build_markup_for_logo(
    png_file,
    background_position="50% 10%",
    margin_top="10%",
    image_width="60%",
    image_height="",
    ):
        binary_string = get_base64_of_bin_file(png_file)
        return """
                <style>
                    [data-testid="stSidebarNav"] {
                        background-image: url("data:image/png;base64,%s");
                        background-repeat: no-repeat;
                        background-position: %s;
                        margin-top: %s;
                        background-size: %s %s;
                    }
                </style>
                """ % (
            binary_string,
            background_position,
            margin_top,
            image_width,
            image_height,
        )


def adicionar_logo(png_file):
    logo_markup = build_markup_for_logo(png_file)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )
    
def add_logo2(imagem):
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: %s;
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """ % (imagem),
        unsafe_allow_html=True,
    )    
    
def tratarDiretorio(valor: str) -> str:
    if estarVazia(valor):
        return ""
    caracteres = ['/','\\']
    for caracter in caracteres:
        if caracter in valor and valor[-1] != caracter:
            return f'{valor}{caracter}'
    return valor

def inserirCaracterFinal(valor: str, caracter: str) -> str:
    return f'{valor}{caracter}' if valor and valor[-1] != caracter else valor

def estarVazia(valor: str) -> bool:
    return len(valor.strip()) == 0

def obterDataHorarioCompleta() -> str:
    return datetime.today().strftime('%d/%m/%Y %H:%M:%S')    

def obterDataDMY() -> str:
    return datetime.today().strftime('%d/%m/%Y')

def obterHorarioHMS() -> str:
    return datetime.today().strftime('%H:%M:%S')

def obterDataYMD() -> str:
    return datetime.today().strftime('%Y%m%d')

def obterTempoYMD() -> str:
    return datetime.today().strftime('%H%M%S')

def extrairAteCaracter(valor: str, caracter: str, posicao: int = 0) -> str:
    if estarVazia(valor):
        return ""
    nova = valor.split(caracter)
    return nova[posicao]

def categorizarColuna(valor: str, chave: str, fig_true: str,fig_false) -> str:
    try:
        if  valor.find(chave) >= 0:
            return fig_false
        else:
            return fig_true
    except AttributeError:
        return "n/a"
    
def extrairStringEntreCaracters(valor: str, sub1: str, sub2: str) -> str:
    idx1 = valor.index(sub1)
    idx2 = valor.index(sub2)
 
    resultado = ''
    for idx in range(idx1 + len(sub1) , idx2):
        resultado = resultado + valor[idx]
    return resultado

def teste(valor):
    st.write(valor)
