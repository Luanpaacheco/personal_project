import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# Solicitação de entrada de usuário
user = input("Email ou CPF: ")
senha = input("Senha: ")

# URL da página de helpdesk na intranet
pagina_url = 'https://intranet.blanchospital.com.br/minha-intra/helpdesk/grupo/1'

# XPath para elementos específicos na página
Xpath_elementoMuda = '//*[@id="list-group-each"]/li/a/span'
estadoElemento = ["-1"]
Xpath_prioridadeMensagem = '//*[@id="helpdesk"]/div[3]/div[2]/div[2]/div[3]/div/table/tbody/tr[1]/td[8]/span'
Xpath_elementoSetor = '//*[@id="panel-title"]'

# Configuração do WebDriver do Chrome
opcoes = webdriver.ChromeOptions()
opcoes.add_argument('--headless=new')
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=opcoes)

def login():
    """
    Realiza o login na página de intranet.

    Utiliza o Selenium para preencher os campos de usuário e senha,
    clicar nos botões de login e aguardar até que a página de destino
    carregue completamente.
    """
    try:
        driver.get(pagina_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(user)
        driver.find_element(By.XPATH, '//*[@id="user-login"]/div[2]/button').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(senha)
        driver.find_element(By.XPATH, '//*[@id="user-login"]/div[3]/div[2]/button').click()
        WebDriverWait(driver, 10).until(EC.url_contains('minha-intra'))
    except Exception as e:
        print(f"Erro ao fazer login: {e}")

def analisaChamado():
    """
    Verifica se há um novo chamado na fila de helpdesk.

    Utiliza Selenium para verificar se o número de chamados não lidos mudou.
    Se houver um novo chamado, atualiza o estadoElemento.
    """
    try:
        driver.get(pagina_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Xpath_elementoMuda)))
        elemento = driver.find_element(By.XPATH, Xpath_elementoMuda)
        valorAtual = int(elemento.text)
        valorAnterior = int(estadoElemento[0])
        
        if valorAnterior != -1 and valorAnterior < valorAtual:
            estadoElemento[0] = valorAtual
            return True
        else:
            estadoElemento[0] = valorAtual
            return False
    except Exception as e:
        print(f"Erro ao analisar chamado: {e}")
        return False

def enviarMensagemTeams(setor, prioridadeMensagem, chamado_url):
    """
    Envia uma mensagem formatada para o Microsoft Teams.

    Utiliza um webhook específico do Teams para enviar uma mensagem estruturada
    indicando um novo chamado, com link direto para acessá-lo.
    """
    try:
        webhook_url = 'https://blanchospital.webhook.office.com/webhookb2/15a060ba-8cec-4dc3-8c89-58e0d113c451@4009eacd-9f63-4a27-b85a-62e89ad7581b/IncomingWebhook/064c075f306a41b39b0afad3caed212d/271da7a3-8111-42f9-b7b6-0fbd02e6526d'

        mensagem = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "summary": "Novo Chamado Recebido",
            "sections": [
                {
                    "activityTitle": f"Novo Chamado - {str.upper(setor)}",
                    "activitySubtitle": f"Prioridade: {str.lower(prioridadeMensagem)}",
                    "activityText": "Clique no link abaixo para acessar o chamado:",
                    "potentialAction": [
                        {
                            "@type": "OpenUri",
                            "name": "Acessar Chamado",
                            "targets": [
                                {"os": "default", "uri": chamado_url}
                            ]
                        }
                    ]
                }
            ]
        }

        response = requests.post(webhook_url, json=mensagem)
        if response.status_code != 200:
            print(f"Erro ao enviar mensagem para o Teams: {response.status_code}, {response.text}")

    except Exception as e:
        print(f"Erro ao enviar mensagem para o Teams: {e}")

def main():
    """
    Função principal que executa o login, monitora novos chamados e envia notificações.

    Executa um loop contínuo onde verifica periodicamente se há novos chamados.
    Quando detecta um novo chamado, envia uma notificação formatada para o Microsoft Teams.
    """
    login()  # Realiza o login inicial
    
    while True:
        if analisaChamado():
            try:
                setor = driver.find_element(By.XPATH, Xpath_elementoSetor).text
                prioridadeMensagem = driver.find_element(By.XPATH, Xpath_prioridadeMensagem).text
                chamado_url = driver.current_url  # Obtém a URL atual do chamado
                
                enviarMensagemTeams(setor, prioridadeMensagem, chamado_url)

            except Exception as e:
                print(f"Erro ao notificar: {e}")
        
        time.sleep(10)  # Aguarda 10 segundos antes de verificar novamente


main()  # Inicia a execução do programa
