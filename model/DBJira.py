from dataclasses import dataclass
import pandas as pd
import duckdb

@dataclass
class DBJira:
    
    def __init__(self, df: pd.DataFrame) -> None:
        self.df_tickets = df
        
    def consultarTodos(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("SELECT * FROM df ").df() 
    
    def obterProjetosDistintos(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("""select distinct 
                                left(c."Issue key", position('-' in c."Issue key")-1) as Projeto
                             from df c
                        """).df() 
        

    
    def obterQtdeTodos(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("""select 
                                count(*) as Quantidade
                            from df  c
                            """).df() 
        
    def obterQtdeIssueType(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("""select
                                c."Issue Type" ,
                                count(c."Issue Type") as Quantidade
                            from df c
                            group by c."Issue Type" 
                            order by c."Issue Type"
                            """).df()  
    
    def obterQtdeIssueType_Projeto(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("""select 
                                left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
                                c."Issue Type" ,
                                count(c."Issue Type") as Quantidade
                            from df c
                            group by left(c."Issue key", position('-' in c."Issue key")-1),
                            c."Issue Type" ,
                            order by "Issue Type" ,1
                            """).df()      
        
    def obterQtdeAssignee(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("""select
                                c.Assignee  ,
                                count(c.Assignee) as Quantidade
                            from df c
                            group by c.Assignee  
                            order by c.Assignee
                            """).df()  
    
    def obterQtdeAssignee_Projeto(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("""select 
                                left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
                                c."Assignee" ,
                                count(c."Assignee") as Quantidade
                            from df c
                            group by left(c."Issue key", position('-' in c."Issue key")-1),
                            c."Assignee" ,
                            order by "Assignee",1
                            """).df()                         
        
    def obterQtdeStatus(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("""select
                                c.Status  ,
                                count(c.Status) as Quantidade
                            from df c
                            group by c.Status  
                            order by c.Status  
                            """).df()  
    
    def obterQtdeStatus_Projeto(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("""select 
                                left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
                                c."Status" ,
                                count(c."Status") as Quantidade
                            from df c
                            group by left(c."Issue key", position('-' in c."Issue key")-1),
                            c."Status" ,
                            order by "Status",1
                            """).df()        
        
    def obterQtdeComponents(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("""select
                                c.Components  ,
                                count(c.Components) as Quantidade
                            from df c
                            group by c.Components  
                            order by c.Components    
                            """).df()  
    
    def obterQtdeComponents_Projeto(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("""select 
                                left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
                                c."Components" ,
                                count(c."Components") as Quantidade
                            from df c
                            group by left(c."Issue key", position('-' in c."Issue key")-1),
                            c."Components" ,
                            order by "Components",1
                            """).df()      
        
    def obterQtdeCustomerRequester(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("""select
                                c."Custom field (Customer Requester)"  as "Customer Requester",
                                count(c."Custom field (Customer Requester)") as Quantidade
                            from main.tickets_custom c
                            group by c."Custom field (Customer Requester)" 
                            order by c."Custom field (Customer Requester)"    
                            """).df()  
    
    def obterQtdeCustomerRequester_Projeto(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("""select 
                                left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
                                c."Custom field (Customer Requester)" as "Customer Requester",
                                count(c."Custom field (Customer Requester)") as Quantidade
                            from main.tickets_custom c
                            group by left(c."Issue key", position('-' in c."Issue key")-1),
                            c."Custom field (Customer Requester)" ,
                            order by "Customer Requester",1
                            """).df() 
        
    def obterQtdeMesAnoCriacao(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("""select
                                c.Created[4:6] as mes, 
                                concat('20',c.Created[8:10]) as ano,
                                count(*) as Quantidade
                            from main.tickets_custom c
                            group by c.Created[4:6], 
                                concat('20',c.Created[8:10]) 
                            order by ano    
                            """).df()  
    
    def obterQtdeMesAnoCriacao_Projeto(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("""select 
                                left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
                                c.Created[4:6] as mes, 
                                concat('20',c.Created[8:10]) as ano,
                                count(c.*) as Quantidade
                            from main.tickets_custom c
                            group by left(c."Issue key", position('-' in c."Issue key")-1),
                                c.Created[4:6], 
                                concat('20',c.Created[8:10])
                            order by ano,1
                            """).df()    
        
    def obterQtdeMesAnoAtualizacao(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("""select
                                c.Created[4:6] as mes, 
                                concat('20',c.Created[8:10]) as ano,
                                count(*) as Quantidade
                            from main.tickets_custom c
                            group by c.Created[4:6], 
                                concat('20',c.Created[8:10]) 
                            order by ano    
                            """).df()  
    
    def obterQtdeMesAnoAtualizacao_Projeto(self) -> pd.DataFrame:
        df  =pd.DataFrame(self.df_tickets)
        return duckdb.sql("""select 
                                left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
                                c.Created[4:6] as mes, 
                                concat('20',c.Created[8:10]) as ano,
                                count(c.*) as Quantidade
                            from main.tickets_custom c
                            group by left(c."Issue key", position('-' in c."Issue key")-1),
                                c.Created[4:6], 
                                concat('20',c.Created[8:10])
                            order by ano,1
                            """).df()                                    