import streamlit as st
from utils import utilidades as ut
import locale

def criar(definirLocale: bool = False):
    if definirLocale:
        locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
        #pd.options.display.float_format = 'R${:, .2f}'.format

    st.set_page_config(
        page_title="Análise de dados Sirius",
        page_icon=":chart_with_upwards_trend:",
        layout="wide"
    )
    #ut.adicionar_logo('img/logo.png')