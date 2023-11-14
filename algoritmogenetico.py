import matplotlib.pyplot as plt
import numpy as np
from deap import creator, base, tools, algorithms
from def_AG import criar_cromossomo, disciplinas, NUM_PERIODOS, TAMANHO_PERIODO, NUM_DISCIPLINAS
import random

def gerar_horario():
    return [random.randint(1, NUM_DISCIPLINAS) for _ in range(TAMANHO_PERIODO * NUM_PERIODOS)]

# Função de avaliação (fitness)
def avaliar_horario(individuo):
    conflitos = 0
    # Dicionário para armazenar horários ocupados por disciplinas
    horarios_ocupados = {}

    # Inicializa horários para cada dia da semana
    for dia in ['segunda', 'terça', 'quarta', 'quinta', 'sexta']:
        horarios_ocupados[dia] = []

    # Verifica cada período no cromossomo
    for disciplina in individuo:
        if disciplina in disciplinas:  # Verifica se a disciplina existe no dicionário
            # Obtém o horário da disciplina
            horario = disciplinas[disciplina]['horario']
            dia, intervalo = horario.split()
            horario_inicio, horario_fim = map(int, intervalo.split('-'))

            # Verifica se há conflito com horários ocupados
            for horario_ocupado in horarios_ocupados[dia]:
                if (horario_inicio < horario_ocupado[1] and horario_fim > horario_ocupado[0]):
                    conflitos += 1  # Conflito de horário detectado
                    break

            # Atualiza os horários ocupados para o dia atual
            horarios_ocupados[dia].append((horario_inicio, horario_fim))
        else:
            conflitos += 1 # Se a disciplina não existir, cont+1 conflito

    return (conflitos,)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, gerar_horario)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", avaliar_horario)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=1, up=NUM_DISCIPLINAS, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

def plot_horarios(cromossomo):
    periods = len(cromossomo)
    days = len(cromossomo[0])

    # Criar uma matriz com zeros representando os horários vazios
    data = np.zeros((periods, days))

    # Preencher a matriz com os índices das disciplinas alocadas
    for i in range(periods):
        for j in range(days):
            if cromossomo[i][j] != '':
                data[i][j] = 1  # Para marcar a alocação de uma disciplina

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(data, cmap='viridis', interpolation='nearest')

    # Definir rótulos e títulos
    ax.set_xticks(np.arange(days))
    ax.set_yticks(np.arange(periods))
    ax.set_xticklabels(['Seg', 'Ter', 'Qua', 'Qui', 'Sex'])  # Dias da semana
    ax.set_yticklabels(np.arange(1, periods + 1))  # Períodos

    # Adicionar barra de cores
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.set_label('Disciplina Alocada')

    # Mostrar o gráfico
    plt.title('Alocação de Disciplinas nos Horários')
    plt.xlabel('Dias da Semana')
    plt.ylabel('Períodos')
    plt.savefig(f'saida/algoritmogenetico.png')
    plt.show()

def selecao(populacao):
    return tools.selRouletteWheel(populacao, len(populacao))

def crossover(individuo1, individuo2):
    return tools.cxUniform(individuo1, individuo2)

def mutacao(individuo, indpb=0.05):
    return tools.mutShuffle(individuo, indpb)

# Algoritmo genético principal
def algoritmo_genetico(pop_size=100, n_gen=500):
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop = toolbox.population(n=pop_size)
    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.2, ngen=n_gen, stats=stats)

    # Obtém os dados estatísticos
    gen = logbook.select("gen")
    avg = logbook.select("avg")
    min_fit = logbook.select("min")
    max_fit = logbook.select("max")

    # Criação do gráfico
    '''''
    plt.figure(figsize=(10, 6))
    plt.plot(gen, avg, label="Média")
    plt.plot(gen, min_fit, label="Mínimo")
    plt.plot(gen, max_fit, label="Máximo")
    plt.xlabel("Geração")
    plt.ylabel("Fitness")
    plt.title("Evolução do Fitness ao Longo das Gerações")
    plt.legend()
    plt.grid(True)
    
    plt.savefig(f'saida/evolucao_fitness.png')
    plt.show()
    '''
    return pop, logbook

if __name__ == "__main__":
    horarios = criar_cromossomo(disciplinas, NUM_PERIODOS, TAMANHO_PERIODO)
    plot_horarios(horarios)  # Chamada para plotar os horários iniciais
    
    algoritmo_genetico(n_gen=500)  # Chamada do algoritmo genético

    # Chamada para plotar os horários otimizados após o algoritmo genético
    plot_horarios(horarios)
