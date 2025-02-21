# Definindo valores padrão
link_agenda ?= ""
nome_evento ?= ""

# Alvo padrão
help:
	@echo "Uso: make teste link_agenda=<link_agenda> nome_evento=<nome_evento>"
	@echo "Parâmetros:"
	@echo "  link_agenda     - link da sua agenda do google (necessário que ela esteja liberada ao público)"
	@echo "  nome_evento     - nome do evento que deseja fazer o cálculo de horas semanais"

# Alvo para rodar o script Python
teste:
	@echo "Iniciando o processo com os seguintes parâmetros:"
	@echo "link_agenda: $(link_agenda)"
	@echo "nome_evento: $(nome_evento)"

	@PYTHONDONTWRITEBYTECODE=1 python3 google_agenda.py "$(link_agenda)" "$(nome_evento)"