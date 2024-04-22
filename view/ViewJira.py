from dataclasses import dataclass, field
import streamlit as st
from controller import CTLJira as ctlJira
from controller import CTLCoffeeCup as ctlCof
from utils import constantes as co


#locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
@dataclass
class ViewJira():
    
    OPT_JIRA = "Jira"        
    OPT_COFFEECUP = "CoffeeCup"
    
    def criar(self):
        st.sidebar.subheader("V.1.4",help="Incluído o processamento de CoffeeCup")
        opcao = st.sidebar.radio("Tipo de arquivo", [self.OPT_JIRA, self.OPT_COFFEECUP])
        arquivoCarregado = st.sidebar.file_uploader("Carregar arquivo csv", accept_multiple_files=False, type=["csv"])
        delimitador = st.sidebar.text_input(label="Delimitador dos campos",value=",")
        enconder = st.sidebar.selectbox(label="Codificação", options=["utf-8","latin-1"])
        desconsiderar = st.sidebar.text_input(label="Valores a serem desconsiderados separados por virgula", value="#&~ço$*'\"/\|;:{]requester,Requester-123456,BBB")
        
        listaDesconsiderar =[]        
        if len(desconsiderar) > 0:
            listaDesconsiderar = desconsiderar.split(",")
        if arquivoCarregado:
            
            try:
                            
                ctlOpcao = ctlJira.CTLJira(arquivoCarregado, delimitador, enconder) if opcao == "Jira" else ctlCof.CTLCoffeeCup(arquivoCarregado, delimitador, enconder)
                            
                cmbCampos = st.sidebar.multiselect(f"Campos",
                    ctlOpcao.obterListaCampos(),            
                    ctlOpcao.obterListaCamposInicial(),
                    placeholder=co.LST_SELECIONE)
                
                lstProjetos = []
                
                if opcao == self.OPT_JIRA:
                    optProjetos = st.radio("Grupo de projetos", options=["Todos","Brasil","LATAM"])
                    if optProjetos == "Todos":
                        lstProjetos = ctlOpcao.obterListaProjetos()
                    elif opcao == self.OPT_JIRA:
                        if optProjetos == "Brasil":
                            lstProjetos = ctlOpcao.obterProjetoBrasil()
                        else:
                            lstProjetos = ctlOpcao.obterProjetoLATAM()    
                elif opcao == self.OPT_COFFEECUP:
                    optProjetos = st.radio("Grupo de projetos", options=["Padrão","Internal Management & Presales","Internal Support Management","Product Management", "Todos exceto Internal project","Todos"])
                    lstTasks = ctlOpcao.obterListaTask()                    
                    if optProjetos == "Padrão":
                        lstProjetos = ctlOpcao.obterProjetoPadrao()
                        lstTasksConfiguradas = lstTasks
                    elif optProjetos == "Todos":
                        lstProjetos = ctlOpcao.obterListaProjetos()
                        lstTasksConfiguradas = lstTasks
                    elif "Presales" in optProjetos:
                        lstTasksConfiguradas = ctlOpcao.obterListaTaskPresales(lstTasks)
                        lstProjetos = ctlOpcao.obterProjetoPresales()
                    elif "Support" in optProjetos:
                        lstTasksConfiguradas = lstTasks                                                
                        lstProjetos = ctlOpcao.obterProjetoSupport()
                    elif "Product" in optProjetos:
                        lstTasksConfiguradas = ctlOpcao.obterListaTaskProduct(lstTasks)
                        lstProjetos = ctlOpcao.obterProjetoProduct()
                    else:                                            
                        lstTasksConfiguradas = lstTasks                                                
                        lstProjetos = ctlOpcao.obterProjetoTodosExcetoInteralProject()
                        
                cmbProjetos = st.multiselect(f"Projetos",
                    lstProjetos,            
                    lstProjetos,
                    placeholder=co.LST_SELECIONE)
                
                if opcao == self.OPT_COFFEECUP:                    
                    cmbTask = st.multiselect(f"Task",
                        lstTasks,            
                        lstTasksConfiguradas,
                        placeholder=co.LST_SELECIONE)
                    cmbProjetos = cmbProjetos + cmbTask

                            
                chkPorcentagem = st.sidebar.checkbox("Mostrar percentual", value=True)
                
                
                df_filtrado = ctlOpcao.filtrar(cmbProjetos) if len(cmbCampos)> 0 else ctlOpcao._df_tickets
            
                        
                with st.container():
                    nCol = len(cmbCampos)                    
                    altura = 380
                                        
                    
                    tab_analise, tab_dados = st.tabs([":clipboard: Análise", ":books: Dados"])
                    with tab_analise:                        
                        tab_analise.subheader(f"Análise Quantitativa dos {len(df_filtrado.index)} registros")                     
                        tab_analise.text(f"Arquivo {arquivoCarregado.name}")                     
                        k=0
                        for i in range(nCol):
                            
                            wCol = 1 if opcao == self.OPT_COFFEECUP and (cmbCampos[i] == "Project" or cmbCampos[i] == "Reference ID")  else 2
                            idColuna2 = wCol-1
                            campoProjeto = "Project" if opcao == self.OPT_COFFEECUP else "Projeto"
                            coluna = st.columns(wCol)                                
                            if len(listaDesconsiderar) > 0:
                                df_filtrado = df_filtrado[~df_filtrado[cmbCampos[i]].isin(listaDesconsiderar)]

                            with coluna[0]:
                                df = ctlOpcao.agruparCampo(df_filtrado, [cmbCampos[i]], chkPorcentagem)
                                coluna[0].subheader(cmbCampos[i])
                                coluna[0].container(height=altura).dataframe(df, hide_index=True, use_container_width=True )
                                
                            if  cmbCampos[i] != campoProjeto:
                                with coluna[idColuna2]:
                                    df = ctlOpcao.agruparCampo(df_filtrado, [campoProjeto, cmbCampos[i]], chkPorcentagem)
                                    coluna[idColuna2].subheader(f"{campoProjeto} -> {cmbCampos[i]}")
                                    coluna[idColuna2].container(height=altura).dataframe(df, hide_index=True, use_container_width=True )  
                                                        
                    with tab_dados:
                        r_da1 = st.columns(1)            
                
                        r_da1[0].subheader(f"Valores originais. Total de registros: {len(ctlOpcao._df_tickets.index)}")
                        r_da1[0].dataframe(ctlOpcao._df_tickets)
            except  UnicodeDecodeError as e:
                st.error(f"Falha no processamento do arquivo. Verifique o delimitador e o enconding apropriado. Mensagem {e}")       
            except LookupError as e:
                st.error(f"Falha no processamento do arquivo. Verifique o enconding apropriado ou o tipo de arquivo. Mensagem {e}")       
            except Exception as e:
                st.error(f"Falha no processamento do arquivo. Verifique o delimitador e o enconding apropriado. Mensagem {e}")       
        
    