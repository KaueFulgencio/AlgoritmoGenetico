import random
from deap import creator, base, tools, algorithms
import matplotlib.pyplot as plt
import numpy as np
from def_AG import criar_cromossomo, disciplinas, NUM_PERIODOS, TAMANHO_PERIODO, NUM_DISCIPLINAS

# Função para gerar um indivíduo aleatório (horário)
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
    for periodo, disciplina in enumerate(individuo):
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
            # Se a disciplina não existir, conte como um conflito
            conflitos += 1

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

def selecao(populacao):
    return tools.selTournament(populacao, tournsize=3)

def crossover(individuo1, individuo2):
    return tools.cxTwoPoint(individuo1, individuo2)

def mutacao(individuo, indpb=0.05):
    return tools.mutUniformInt(individuo, low=1, up=NUM_DISCIPLINAS, indpb=indpb)[0]

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
    
    return pop, logbook

if __name__ == "__main__":
    horarios = criar_cromossomo(disciplinas, NUM_PERIODOS, TAMANHO_PERIODO)
    print(horarios)
    algoritmo_genetico(n_gen=500) #500 Iterações
