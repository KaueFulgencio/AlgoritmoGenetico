# Coleta de Dados e Modelagem
# Aqui você pode coletar os dados das disciplinas, pré-requisitos, horários dos professores
# e modelar o problema, representando as relações e restrições entre as disciplinas

import random

NUM_PERIODOS = 4
NUM_DISCIPLINAS = 8
TAMANHO_PERIODO = 5  

disciplinas = {
    'Calculo 1': {'horario': 'segunda 08:00-10:00', 'pre_requisitos': []},
    'Algoritmos': {'horario': 'segunda 10:00-12:00', 'pre_requisitos': ['Matemática']},
    'Fundamentos de Sistemas Inteligentes': {'horario': 'terça 08:00-10:00', 'pre_requisitos': ['Algoritmos']},
    'Redes de Computadores': {'horario': 'quarta 14:00-16:00', 'pre_requisitos': ['Algoritmos']},
    'Banco de Dados': {'horario': 'quinta 08:00-10:00', 'pre_requisitos': ['Matemática']},
}

def criar_cromossomo(disciplinas, num_periodos, tamanho_periodo):
    cromossomo = [] # Inicializa um cromossomo vazio

    for _ in range(num_periodos): # Itera sobre o número de períodos para criar a grade de horários
        # Disciplinas adicionadas de acordo com o tamanho do período
        periodo = random.sample(list(disciplinas.keys()), tamanho_periodo)
        cromossomo.extend(periodo)

    return cromossomo

num_periodos = 4
tamanho_periodo = 2
horarios = criar_cromossomo(disciplinas, num_periodos, tamanho_periodo)
print(horarios)