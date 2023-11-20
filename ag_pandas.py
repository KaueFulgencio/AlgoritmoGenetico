import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
from deap import creator, base, tools, algorithms

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

def gerar_horario():
    return [random.randint(1, NUM_DISCIPLINAS) for _ in range(TAMANHO_PERIODO * NUM_PERIODOS)]

def plot_horarios_pandas(cromossomo, label):
    periods = len(cromossomo)
    days = len(cromossomo[0])

    data = np.zeros((periods, days))

    for i in range(periods):
        for j in range(days):
            if cromossomo[i][j] != '':
                data[i][j] = 1

    df = pd.DataFrame(data, columns=['Seg', 'Ter', 'Qua', 'Qui', 'Sex'])
    df.index = np.arange(1, periods + 1)

    plt.figure(figsize=(8, 6))
    plt.imshow(df, cmap='viridis', interpolation='nearest')

    plt.colorbar(label='Disciplina Alocada')
    plt.title(f'Alocação de Disciplinas - {label}')
    plt.xlabel('Dias da Semana')
    plt.ylabel('Períodos')

    plt.savefig(f'saida/alocacao_pandas_{label.lower()}.png')
    plt.show()
    plt.close()

    # Exportar para CSV
    df.to_csv(f'saida/alocacao_{label.lower()}.csv')

def criar_cromossomo(disciplinas, num_periodos, tamanho_periodo):
    cromossomo = [['' for _ in range(tamanho_periodo)] for _ in range(num_periodos)]
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


def display_horarios(cromossomo):
    periods = len(cromossomo)
    days = len(cromossomo[0])

    # Criar uma matriz para representar os horários
    horarios = [['' for _ in range(days)] for _ in range(periods)]

    # Preencher a matriz com as disciplinas alocadas
    for i in range(periods):
        for j in range(days):
            horarios[i][j] = cromossomo[i][j]

    # Criar um DataFrame do Pandas para exibir a tabela
    df = pd.DataFrame(horarios, columns=['Seg', 'Ter', 'Qua', 'Qui', 'Sex'], index=range(1, periods + 1))
    print(df)

def avaliar_horario(individuo):
    conflitos = 0
    # Dicionário para armazenar horários ocupados por disciplinas
    horarios_ocupados = {dia: set() for dia in ['segunda', 'terça', 'quarta', 'quinta', 'sexta']}

    # Verifica cada período no cromossomo
    for disciplina in individuo:
        if disciplina in disciplinas:  # Verifica se a disciplina existe no dicionário
            # Obtém o horário da disciplina
            horario = disciplinas[disciplina]['horario']
            dia, intervalo = horario.split()
            horario_inicio, horario_fim = map(int, intervalo.split('-'))

            # Verifica se há conflito com horários ocupados
            conflito_encontrado = False
            for horario_ocupado in horarios_ocupados[dia]:
                if horario_inicio < horario_ocupado[1] and horario_fim > horario_ocupado[0]:
                    conflitos += 1  # Conflito de horário detectado
                    conflito_encontrado = True
                    break

            if not conflito_encontrado:
                # Atualiza os horários ocupados para o dia atual
                horarios_ocupados[dia].add((horario_inicio, horario_fim))
        else:
            conflitos += 1  # Se a disciplina não existir, cont+1 conflito

    return conflitos,

def algoritmo_genetico(pop_size=100, n_gen=500):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual, gerar_horario)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", avaliar_horario)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutUniformInt, low=1, up=NUM_DISCIPLINAS, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    # Registrar a função de diversidade corretamente
    stats.register("diversity", diversity)

    # Inicialização personalizada da população usando criar_cromossomo
    pop = [toolbox.individual() for _ in range(pop_size)]

    # Avaliação inicial da população
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # Registro das funções e execução do algoritmo genético
    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.2, ngen=n_gen, stats=stats)

    # Horários otimizados depois do algoritmo genético
    horarios_otimizados_depois = criar_cromossomo(disciplinas, NUM_PERIODOS, TAMANHO_PERIODO)
    plot_horarios_pandas(horarios_otimizados_depois, 'Otimizado')

    # Exibir estatísticas adicionais
    gen = logbook.select("gen")
    fit_mins = logbook.select("min")
    fit_avgs = logbook.select("avg")
    fit_maxs = logbook.select("max")
    diversity = logbook.select("diversity")

    # Exportar horários otimizados para CSV
    periods = len(horarios_otimizados_depois)
    days = len(horarios_otimizados_depois[0])
    data = np.zeros((periods, days))

    for i in range(periods):
        for j in range(days):
            if horarios_otimizados_depois[i][j] != '':
                data[i][j] = 1

    df = pd.DataFrame(data, columns=['Seg', 'Ter', 'Qua', 'Qui', 'Sex'])
    df.index = np.arange(1, periods + 1)
    df.to_csv('saida/alocacao_otimizada.csv')

    return pop, logbook


def gerar_horario_inicial():
    return criar_cromossomo(disciplinas, NUM_PERIODOS, TAMANHO_PERIODO)

if __name__ == "__main__":
    horarios_otimizados_depois = criar_cromossomo(disciplinas, NUM_PERIODOS, TAMANHO_PERIODO)
    display_horarios(horarios_otimizados_depois)
    
    horarios_iniciais = gerar_horario_inicial()
    plot_horarios_pandas(horarios_iniciais, 'Inicial')
    
    pop_final, logbook = algoritmo_genetico(n_gen=500)

    # Exibindo estatísticas adicionais
    gen = logbook.select("gen")
    fit_mins = logbook.select("min")
    fit_avgs = logbook.select("avg")
    fit_maxs = logbook.select("max")
    diversity = logbook.select("diversity")

    # horários otimizados depois do algoritmo genético
    horarios_otimizados_depois = criar_cromossomo(disciplinas, NUM_PERIODOS, TAMANHO_PERIODO)
    plot_horarios_pandas(horarios_otimizados_depois, 'Otimizado')
