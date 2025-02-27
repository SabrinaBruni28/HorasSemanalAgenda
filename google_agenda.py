from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium import webdriver
import time, sys

def horas_evento_semanal(link_agenda, nome_evento):
    # Configuração do WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Maximiza a janela
    driver = webdriver.Chrome(options=options)

    # Acessar a Google Agenda
    driver.get(link_agenda)

    time.sleep(1) 

    print("Google Agenda Acessado!")

    # Filtrar para Semana
    driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[1]/header/div/div[2]/nav/div[1]/div[1]/div/button/span[5]').click()

    time.sleep(1)

    driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[1]/header/div/div[2]/nav/div[1]/div[2]/div/div/ul/li[2]').click()

    time.sleep(10)

    print("Modo Semana ativado!")

    # Selecionar os eventos da semana
    eventos = driver.find_elements(By.CLASS_NAME, 'Jcb6qd')
    print("Eventos selecionados!")

    time.sleep(1)

    total = timedelta()

    # Percorrer a lista de eventos
    for evento in eventos:
        # Selecionar o nome do evento
        nome = evento.find_element(By.CLASS_NAME, 'I0UMhf')

        # Conferir se é o evento desejado
        if nome_evento in nome.text:
            nome.click()

            time.sleep(1)

            # Selecionar as informações do evento
            texto = driver.find_element(By.CLASS_NAME, 'LTczme')

            # Selecionar o horário do evento
            horario = texto.find_elements(By.TAG_NAME, 'span')[2]

            print(nome.text, horario.text)

            time.sleep(1)

            # Separar os horários
            inicio, fim = horario.text.split(" até ")

            # Converter para objetos datetime
            formato = "%H:%M"
            hora_inicio = datetime.strptime(inicio, formato)
            hora_fim = datetime.strptime(fim, formato)

            # Calcular a diferença
            total += (hora_fim - hora_inicio)

    # Exibir o tempo total em horas e minutos
    horas, minutos = divmod(total.total_seconds() // 60, 60)

    print(f"\nTotal de horas do evento '{nome_evento}' nesta semana: {horas}h e {minutos}min")

    # Fechar o navegador
    driver.quit()

    return horas, minutos


# Captura os parâmetros da linha de comando
if __name__ == "__main__":
    link_agenda = sys.argv[1]
    nome_evento = sys.argv[2]

    horas_evento_semanal(link_agenda, nome_evento)