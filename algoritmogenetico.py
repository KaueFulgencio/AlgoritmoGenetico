import random
from deap import creator, base, tools, algorithms
import matplotlib.pyplot as plt
import numpy as np
from def_AG import *

NUM_PERIODOS = 4
NUM_DISCIPLINAS = 8
TAMANHO_PERIODO = 5  

# Função para gerar um indivíduo aleatório (horário)
def gerar_horario():
    return [random.randint(1, NUM_DISCIPLINAS) for _ in range(TAMANHO_PERIODO * NUM_PERIODOS)]

# Função de avaliação (fitness)
def avaliar_horario(individuo):
    # Implemente a lógica para avaliar a qualidade do horário
    # Aqui, usamos uma abordagem simples contando o número de disciplinas duplicadas
    disciplinas_unicas = set(individuo)
    quantidade_duplicadas = len(individuo) - len(disciplinas_unicas)
    # Quanto menor a quantidade de disciplinas duplicadas, melhor
    return (quantidade_duplicadas,)

# Biblioteca DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, gerar_horario)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", avaliar_horario)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=1, up=NUM_DISCIPLINAS, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

def criar_histograma(dados, titulo_grafico, titulo_eixo_x, titulo_eixo_y, nome_arquivo_saida, bins=None):
    if not dados:
        print("Erro: Não há dados para criar o gráfico.")
        return

    bins = len(set(dados)) + 1  

    plt.figure(figsize=(10, 6))
    plt.hist(dados, bins=bins, density=True, alpha=0.7, edgecolor='k')

    plt.title(titulo_grafico)
    plt.xlabel(titulo_eixo_x)
    plt.ylabel(titulo_eixo_y)
    plt.grid(True)

    plt.savefig(f'saida/{nome_arquivo_saida}.png')
    plt.show()

def cria_histograma_automatico():
    
    dados = [1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 5]
    titulo_grafico = "Gráfico de Histograma"
    titulo_eixo_x = "Valores"
    titulo_eixo_y = "Frequência normalizada"
    nome_arquivo_saida = "histograma_predefinido"
    
    criar_histograma(dados, titulo_grafico, titulo_eixo_x, titulo_eixo_y, nome_arquivo_saida)


def main():
    # Criação da população
    populacao = toolbox.population(n=100)

    # Execução do algoritmo genético
    algoritmo_genetico = algorithms.eaSimple(populacao, toolbox, cxpb=0.7, mutpb=0.2, ngen=50, stats=None, halloffame=None, verbose=True)

    # Obtém o melhor indivíduo encontrado
    melhor_horario = tools.selBest(populacao, k=1)[0]

    # Imprime o melhor horário
    print("Melhor Horário Encontrado:")
    print(melhor_horario)

    cria_histograma_automatico()

if __name__ == "__main__":
    main()
