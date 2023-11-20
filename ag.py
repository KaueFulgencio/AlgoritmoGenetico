import matplotlib.pyplot as plt
import numpy as np
from deap import creator, base, tools, algorithms
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

def gerar_horario():
    return [random.randint(1, NUM_DISCIPLINAS) for _ in range(TAMANHO_PERIODO * NUM_PERIODOS)]

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

def inicializar_populacao(pop_size):
    # Lógica para inicialização personalizada da população
    populacao = []
    for _ in range(pop_size):
        # Criar indivíduos com uma distribuição preferencial de disciplinas
        # Aqui você pode aplicar sua heurística de escolha ou preferência
        # Por exemplo, distribuição uniforme de disciplinas ou outras regras específicas

        # Criação de um indivíduo fictício como exemplo
        individuo = random.sample(disciplinas.keys(), len(disciplinas.keys()))
        populacao.append(individuo)
    
    return populacao

def plot_horarios(cromossomo, label, otimizacao):
    periods = len(cromossomo)
    days = len(cromossomo[0])

    # Criar uma matriz com zeros representando os horários vazios
    data = np.zeros((periods, days))

    # Preencher a matriz com os índices das disciplinas alocadas
    for i in range(periods):
        for j in range(days):
            if cromossomo[i][j] != '':
                data[i][j] = 1  

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(data, cmap='viridis', interpolation='nearest')

    # Definir rótulos e títulos
    ax.set_xticks(np.arange(days))
    ax.set_yticks(np.arange(periods))
    ax.set_xticklabels(['Seg', 'Ter', 'Qua', 'Qui', 'Sex'])  # Dias da semana
    ax.set_yticklabels(np.arange(1, periods + 1))  # Períodos

    # Barra de cores
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.set_label('Disciplina Alocada')

    # Salvar a imagem antes de mostrar
    if otimizacao == 'antes':
        plt.savefig('saida/antes_otimizacao.png')
    elif otimizacao == 'depois':
        plt.savefig('saida/depois_otimizacao.png')

    # Mostrar o gráfico
    plt.title(f'Alocação de Disciplinas - {label}')
    plt.xlabel('Dias da Semana')
    plt.ylabel('Períodos')
    plt.show()
    plt.close();
    
    
def selecao(populacao):
    return tools.selRouletteWheel(populacao, len(populacao))

def crossover(individuo1, individuo2):
    return tools.cxUniform(individuo1, individuo2)

def mutacao(individuo, indpb=0.05):
    return tools.mutShuffle(individuo, indpb)

def diversity(population):
    unique_individuals = set(map(tuple, population))
    return len(unique_individuals) / len(population)

def algoritmo_genetico(pop_size=100, n_gen=500):
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

    return pop, logbook

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

def imprimir_horarios_finais(horarios_finais):
    for periodo, horario in enumerate(horarios_finais, start=1):
        print(f"Período {periodo}: {horario}")

def gerar_horario_inicial():
    return criar_cromossomo(disciplinas, NUM_PERIODOS, TAMANHO_PERIODO)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, gerar_horario)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", avaliar_horario)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutUniformInt, low=1, up=NUM_DISCIPLINAS, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

if __name__ == "__main__":
    horarios_iniciais = gerar_horario_inicial()
    plot_horarios(horarios_iniciais, 'Inicial', None)

    pop_final, logbook = algoritmo_genetico(n_gen=500)  

    # estatísticas adicionais
    gen = logbook.select("gen")
    fit_mins = logbook.select("min")
    fit_avgs = logbook.select("avg")
    fit_maxs = logbook.select("max")
    diversity = logbook.select("diversity")
    
    # horários otimizados pós algoritmo genético
    horarios_otimizados_depois = criar_cromossomo(disciplinas, NUM_PERIODOS, TAMANHO_PERIODO)
    plot_horarios(horarios_otimizados_depois, 'Otimizado', 'depois')
        
    num_periodos = 4
    tamanho_periodo = 5
    horarios_finais = criar_cromossomo(disciplinas, num_periodos, tamanho_periodo)
    imprimir_horarios_finais(horarios_finais)
    for periodo in horarios_finais:
        print(periodo)
