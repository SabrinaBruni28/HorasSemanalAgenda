from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium import webdriver
import time, sys
from selenium.common.exceptions import NoSuchElementException

def horas_evento_semanal(link_agenda, nome_evento, dia, mes):
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



    while True:
        total = timedelta()

        time.sleep(1)
        try:
            driver.find_element(By.XPATH, f'//h2[contains(@class, "hI2jVc") and contains(@aria-label, "{dia} de {mes.lower()}")]')
            break  # se encontrou, sai do loop
        except NoSuchElementException:
            # se não encontrou, clica no botão para ir para a semana anterior
            driver.find_element(By.XPATH, '//button[@aria-label="Semana anterior"]').click()

        time.sleep(2)
        # Selecionar os eventos da semana
        eventos = driver.find_elements(By.CLASS_NAME, 'Jcb6qd')
        print("Eventos selecionados!")

        faltando = timedelta(hours=0, minutes=0)

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
                inicio, fim = horario.text.split(" – ")

                # Converter para objetos datetime
                formato = "%H:%M"
                hora_inicio = datetime.strptime(inicio, formato)
                hora_fim = datetime.strptime(fim, formato)

                # Calcular a diferença
                total += (hora_fim - hora_inicio)

                time.sleep(2)

                # Fecha as informações
                botao_x = driver.find_element(By.XPATH, "//*//button[@aria-label='Fechar']")
                botao_x.click()

                time.sleep(2)

        # Extrai horas e minutos de total
        total_minutos = int(total.total_seconds() // 60)
        horas_trabalhadas, minutos_trabalhados = divmod(total_minutos, 60)

        # Meta fixa de 30 horas
        meta = timedelta(hours=30)

        # Diferença entre meta e total
        faltando_semana = meta - total

        # Extrai total de minutos do saldo (pode ser negativo)
        faltando_minutos = int(faltando_semana.total_seconds() // 60)
        sinal = ""
        if faltando_minutos < 0:
            sinal = "-"
            faltando_minutos = abs(faltando_minutos)

        faltando_horas, faltando_minutos = divmod(faltando_minutos, 60)

        # Imprime resultado
        print(f"Horas trabalhadas na semana: {horas_trabalhadas}h e {minutos_trabalhados}min")

        if sinal == "-":
            faltando -= timedelta(hours=faltando_horas, minutes=faltando_minutos)
            print(f"Excedeu {faltando_horas}h e {faltando_minutos}min além das 30h")
        else:
            print(f"Faltando {faltando_horas}h e {faltando_minutos}min para completar 30h")
            faltando += timedelta(hours=faltando_horas, minutes=faltando_minutos)
    
    # Exibir o tempo total em horas e minutos
    horas, minutos = divmod(faltando.total_seconds() // 60, 60)
    print(f"\nTotal de horas faltando do '{nome_evento}' até essa semana: {horas}h e {minutos}min")

    # Fechar o navegador
    driver.quit()

    return horas, minutos


# Captura os parâmetros da linha de comando
if __name__ == "__main__":
    link_agenda = sys.argv[1]
    nome_evento = sys.argv[2]

    horas_evento_semanal(link_agenda, nome_evento)