import pandas as pd
from io import StringIO
import streamlit as st
from controller import CTLJira as ctl

def main():
    arquivo = st.file_uploader("Carregar arquivo csv", accept_multiple_files=False, type=["csv"])
    if arquivo is not None:
        # To read file as bytes:
        bytes_data = arquivo.getvalue()
        ctlJira = ctl.CTLJira(arquivo)
        tab_dados, tab_todos = st.tabs(["Dados", "Todos"])
        with st.container():
            with tab_dados:
                st.dataframe(ctlJira.df_tickets)
            with tab_todos:
                st.dataframe(ctlJira.consultarTodos())
                st.dataframe(ctlJira.consultarQtdeTodos())
                st.dataframe(ctlJira.consultarQtdeIssueType())
                st.dataframe(ctlJira.consultarQtdeIssueType_Projeto())
        
        
        
if __name__ == "__main__":
    main()

            

    
