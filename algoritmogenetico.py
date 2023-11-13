import random
from deap import creator, base, tools, algorithms

NUM_PERIODOS = 4
NUM_DISCIPLINAS = 8
TAMANHO_PERIODO = 5  # Número de dias da semana

# Função para gerar um indivíduo aleatório (horário)
def gerar_horario():
    return [random.randint(1, NUM_DISCIPLINAS) for _ in range(TAMANHO_PERIODO * NUM_PERIODOS)]

# Função de avaliação (fitness)
def avaliar_horario(individuo):
    # Implemente a lógica para avaliar a qualidade do horário
    # Considere conflitos de horários, pré-requisitos, etc.
    # Retorne uma tupla com o valor de aptidão (quanto menor, melhor)
    return (random.random(),)

# Configuração da biblioteca DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, gerar_horario)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", avaliar_horario)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=1, up=NUM_DISCIPLINAS, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# Criação da população
populacao = toolbox.population(n=100)

# Execução do algoritmo genético
algoritmo_genetico = algorithms.eaSimple(populacao, toolbox, cxpb=0.7, mutpb=0.2, ngen=50, stats=None, halloffame=None, verbose=True)

# Obtém o melhor indivíduo encontrado
melhor_horario = tools.selBest(populacao, k=1)[0]

# Imprime o melhor horário
print("Melhor Horário Encontrado:")
print(melhor_horario)
