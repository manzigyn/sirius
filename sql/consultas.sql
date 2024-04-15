INSTALL spatial; -- Only needed once per DuckDB connection
LOAD spatial; -- Only needed once per DuckDB connection

create table tickets_all as
select * from st_read('D:\pessoal\Sirius\sirius\All Open Tickets - all fields.csv', open_options = ['HEADERS=FORCE'])

create table tickets_custom as
select * from st_read('D:\pessoal\Sirius\sirius\All Open Tickets - custom fields.csv', open_options = ['HEADERS=FORCE'])

select * from main.tickets_all 

select * from main.tickets_custom 

-- Todos os chamados em aberto (qtde)
select * from main.tickets_custom c
order by c."Issue Type" 

select count(*) from main.tickets_custom  c

select 
    left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
	count(c."Issue key") as Quantidade
from main.tickets_custom c
group by left(c."Issue key", position('-' in c."Issue key")-1) 
order by "Issue key" 




-- qtde aberto por issue type (change request, incident, question, service request)
select
	c."Issue Type" ,
	count(c."Issue Type") as Quantidade
from main.tickets_custom c
group by c."Issue Type" 
order by c."Issue Type" 

select 
    left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
    c."Issue Type" ,
	count(c."Issue Type") as Quantidade
from main.tickets_custom c
group by left(c."Issue key", position('-' in c."Issue key")-1),
c."Issue Type" ,
order by "Issue Type" ,1


-- qtde aberto por assignee (por pessoa)

select
	c.Assignee  ,
	count(c.Assignee) as Quantidade
from main.tickets_custom c
group by c.Assignee  
order by c.Assignee

select 
    left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
    c."Assignee" ,
	count(c."Assignee") as Quantidade
from main.tickets_custom c
group by left(c."Issue key", position('-' in c."Issue key")-1),
c."Assignee" ,
order by "Assignee",1

-- qtde aberto por status (waiting hypercare) - WORKFLOW:
select
	c.Status  ,
	count(c.Status) as Quantidade
from main.tickets_custom c
group by c.Status  
order by c.Status  

select 
    left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
    c."Status" ,
	count(c."Status") as Quantidade
from main.tickets_custom c
group by left(c."Issue key", position('-' in c."Issue key")-1),
c."Status" ,
order by "Status",1


-- qtde chamados aberto por components
select
	c.Components  ,
	count(c.Components) as Quantidade
from main.tickets_custom c
group by c.Components  
order by c.Components  

select 
    left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
    c."Components" ,
	count(c."Components") as Quantidade
from main.tickets_custom c
group by left(c."Issue key", position('-' in c."Issue key")-1),
c."Components" ,
order by "Components",1

-- qtde chamados aberto por custormer requester
select
	c."Custom field (Customer Requester)"  as "Customer Requester",
	count(c."Custom field (Customer Requester)") as Quantidade
from main.tickets_custom c
group by c."Custom field (Customer Requester)" 
order by c."Custom field (Customer Requester)"

select 
    left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
    c."Custom field (Customer Requester)" as "Customer Requester",
	count(c."Custom field (Customer Requester)") as Quantidade
from main.tickets_custom c
group by left(c."Issue key", position('-' in c."Issue key")-1),
c."Custom field (Customer Requester)" ,
order by "Customer Requester",1

-- qtde chamados aberto por mes, ano (created)
select c.Created, c.Created[4:6] as mes, concat(c.Created[4:6], ' 20',c.Created[8:10]) 
from main.tickets_custom c

select * from main.tickets_custom c


select
	c.Created[4:6] as mes, 
	concat('20',c.Created[8:10]) as ano,
	count(*) as Quantidade
from main.tickets_custom c
group by c.Created[4:6], 
	concat('20',c.Created[8:10]) 
order by ano

select 
    left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
    c.Created[4:6] as mes, 
	concat('20',c.Created[8:10]) as ano,
	count(c.*) as Quantidade
from main.tickets_custom c
group by left(c."Issue key", position('-' in c."Issue key")-1),
	c.Created[4:6], 
	concat('20',c.Created[8:10])
order by ano,1

-- qtde chamados aberto por mes, ano (updated)
select
	c.Updated[4:6] as mes, 
	concat('20',c.Updated[8:10]) as ano,
	count(*) as Quantidade
from main.tickets_custom c
group by c.Updated[4:6], 
	concat('20',c.Updated[8:10]) 
order by ano

select 
    left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
    c.Updated[4:6] as mes, 
	concat('20',c.Updated[8:10]) as ano,
	count(c.*) as Quantidade
from main.tickets_custom c
group by left(c."Issue key", position('-' in c."Issue key")-1),
	c.Updated[4:6], 
	concat('20',c.Updated[8:10])
order by ano,1

-- qtde chamados aberto por Time to First response por cor
select
	contains(c."Custom field (Time to first response)",'-') as "Time to first response",  
	count(*) as Quantidade
from main.tickets_custom c
group by contains(c."Custom field (Time to first response)",'-') 
order by 1

select 
    left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
	contains(c."Custom field (Time to first response)",'-') as "Time to first response",
	count(c.*) as Quantidade
from main.tickets_custom c
group by left(c."Issue key", position('-' in c."Issue key")-1),
	contains(c."Custom field (Time to first response)",'-')
order by 2,1

-- qtde chamados aberto por Time to resolution por cor
select
	contains(c."Custom field (Time to resolution)" ,'-') as "Time to resolution",  
	count(*) as Quantidade
from main.tickets_custom c
group by contains(c."Custom field (Time to resolution)" ,'-') 
order by 1

select 
    left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
	contains(c."Custom field (Time to resolution)" ,'-') as "Time to resolution",
	count(c.*) as Quantidade
from main.tickets_custom c
group by left(c."Issue key", position('-' in c."Issue key")-1),
	contains(c."Custom field (Time to resolution)" ,'-')
order by 2,1

-- qtde chamados aberto por Internal priority por valor

select
	c."Custom field (Internal priority)" as "Internal priority",  
	count(*) as Quantidade
from main.tickets_custom c
group by c."Custom field (Internal priority)" 
order by 1

select 
    left(c."Issue key", position('-' in c."Issue key")-1) "Issue key",	
	c."Custom field (Internal priority)" as "Internal priority",
	count(c.*) as Quantidade
from main.tickets_custom c
group by left(c."Issue key", position('-' in c."Issue key")-1),
	c."Custom field (Internal priority)"
order by 2,1