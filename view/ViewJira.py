from dataclasses import dataclass, field
import streamlit as st
import streamlit_shadcn_ui as ui
from controller import CTLJira as ctl
from utils import constantes as co
from utils import utilidades as ut
import plotly_express as px    
import pandas as pd


#locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
@dataclass
class ViewJira():
    
        
    def criar(self):
        arquivoCarregado = st.sidebar.file_uploader("Carregar arquivo csv", accept_multiple_files=False, type=["csv"])
        
        if arquivoCarregado:
            ctlJira = ctl.CTLJira(arquivoCarregado)
                        
            cmbCampos = st.sidebar.multiselect(f"Campos",
                ctlJira.obterListaCampos(),            
                ctlJira.obterListaCamposInicial(),
                placeholder=co.LST_SELECIONE)
            
            lstProjetos = ctlJira.obterListaProjetos()
            cmbProjetos = st.sidebar.multiselect(f"Projetos",
                lstProjetos,            
                lstProjetos,
                placeholder=co.LST_SELECIONE)
            
            chkPorcentagem = st.sidebar.checkbox("Mostrar percentual", value=True)
            
            df_filtrado = ctlJira.filtrarProjetos(cmbProjetos) if len(cmbCampos)> 0 else ctlJira.df_tickets
           
                    
            with st.container():
                nCol = len(cmbCampos)
                wCol = 2
                altura = 380
                colunas = st.columns(wCol)           
                
                
                tab_analise, tab_dados = st.tabs([":clipboard: Análise", ":books: Dados"])
                with tab_analise:
                    tab_analise.subheader(f"Análise Quantitativa dos {len(df_filtrado.index)} registros")                     
                    k=0
                    for i in range(nCol):
                        
                        if i%wCol == 0:
                            colunas = st.columns(wCol)                                
                            k=0                    
                        coluna = colunas[k%wCol]
                        k +=1
                        with coluna:
                            df = ctlJira.agruparCampo(df_filtrado, [cmbCampos[i]], chkPorcentagem)
                            coluna.subheader(cmbCampos[i])
                            coluna.container(height=altura).dataframe(df, hide_index=True, use_container_width=True )
                with tab_dados:
                    r_da1 = st.columns(1)            
            
                    r_da1[0].subheader(f"Valores originais. Total de registros: {len(ctlJira.df_tickets.index)}")
                    r_da1[0].dataframe(ctlJira.df_tickets)
                
            
        
    