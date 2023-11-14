import random

NUM_PERIODOS = 4
TAMANHO_PERIODO = 5
NUM_DISCIPLINAS = 8

disciplinas = {
    'Calculo 1': {'horario': 'segunda 08:00-10:00', 'pre_requisitos': []},
    'Algoritmos': {'horario': 'segunda 10:00-12:00', 'pre_requisitos': ['Matemática']},
    'Fundamentos de Sistemas Inteligentes': {'horario': 'terça 08:00-10:00', 'pre_requisitos': ['Algoritmos']},
    'Redes de Computadores': {'horario': 'quarta 14:00-16:00', 'pre_requisitos': ['Algoritmos']},
    'Banco de Dados': {'horario': 'quinta 08:00-10:00', 'pre_requisitos': ['Matemática']},
    'Estruturas de Dados': {'horario': 'sexta 10:00-12:00', 'pre_requisitos': ['Algoritmos']},
    'Inteligência Artificial': {'horario': 'quarta 08:00-10:00', 'pre_requisitos': ['Fundamentos de Sistemas Inteligentes']},
    'Sistemas Operacionais': {'horario': 'terça 14:00-16:00', 'pre_requisitos': ['Algoritmos']},
}

def criar_cromossomo(disciplinas, num_periodos, tamanho_periodo):
    cromossomo = [[''] * tamanho_periodo for _ in range(num_periodos)]
    disciplinas_disponiveis = list(disciplinas.keys())
    disciplinas_nao_alocadas = []

    for disciplina in disciplinas_disponiveis:
        pre_requisitos_atendidos = all(pre_req in disciplinas_nao_alocadas for pre_req in disciplinas[disciplina]['pre_requisitos'])
        if pre_requisitos_atendidos:
            alocado = False
            while not alocado:
                periodo = random.randint(0, num_periodos - 1)
                horario = random.randint(0, tamanho_periodo - 1)
                if cromossomo[periodo][horario] == '':
                    cromossomo[periodo][horario] = disciplina
                    alocado = True
        else:
            disciplinas_nao_alocadas.append(disciplina)

    return cromossomo

num_periodos = 4
tamanho_periodo = 5
horarios = criar_cromossomo(disciplinas, num_periodos, tamanho_periodo)
for periodo in horarios:
    print(periodo)
