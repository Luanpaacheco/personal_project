from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from plyer import notification
import time


url = 'https://intranet.blanchospital.com.br/minha-intra/helpdesk/grupo/1'  #link do intranet
u =85406805053 #input("E-mail ou CPF:")  
s ='Macacos21@' #input("Senha:")  
dashboard_url = 'https://intranet.blanchospital.com.br/minha-intra/helpdesk/grupo/1'  #link do intranet depois do login
elemento_xpath = '//*[@id="list-group-each"]/li/a/span' #XPATH do elemento que muda de acordo com os chamados
estadoElemento=["-1"]
prioridadeMensagem1="testeLuan"
elementoPrioridade_xpath= '//*[@id="helpdesk"]/div[3]/div[2]/div[2]/div[3]/div/table/tbody/tr[1]/td[8]/span'
#elementoSetor=""


opcoes = webdriver.ChromeOptions()
#opcoes.add_argument('--headless=new') 
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service,options=opcoes)



def login():
   
        driver.get(url)
        driver.find_element(By.ID, 'username').send_keys(u)
        driver.find_element(By.XPATH, '//*[@id="user-login"]/div[2]/button').click() 
        time.sleep(2)
        driver.find_element(By.ID, 'password').send_keys(s)
        time.sleep(8)
        driver.find_element(By.XPATH, '//*[@id="user-login"]/div[4]/div[2]/button').click()
        
        
        
    


def check_element_change():
    driver.get(dashboard_url)
    time.sleep(5) 

   
    elemento = driver.find_element(By.XPATH, elemento_xpath)

    
    
    valorAtual =int(elemento.text)

     
    valorAnterior = int(estadoElemento[0])

    #   if(current_value=="0"):
    #      current_value="1"
    #     return False    

   
    if valorAnterior!=-1 and valorAnterior < valorAtual:
        estadoElemento[0] = valorAtual
        return True
    else:
        estadoElemento[0] = valorAtual
        return False
    

    



login()

  


while True:
    if check_element_change():
        #setor=(driver.find_element(By.ID, elementoSetor)).text
        prioridadeMensagem1=(driver.find_element(By.XPATH, elementoPrioridade_xpath)).text
        notification.notify(
            title='NOVO CHAMADO DE NUMERO '+ str(estadoElemento[0]),
            message= 'Equipe de TI acaba de receber um chamado novo de prioridade '+str.lower(prioridadeMensagem1),
              
            timeout=10,  
        )
    
    time.sleep(10)  


driver.quit()
