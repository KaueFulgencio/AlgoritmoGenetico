import matplotlib.pyplot as plt
import numpy as np
from deap import creator, base, tools, algorithms
import random

NUM_PERIODOS = 4
TAMANHO_PERIODO = 5
NUM_DISCIPLINAS = 8

disciplinas = {
    'Calculo 1': {'horario': 'segunda 08:00-10:00', 'pre_requisitos': []},
    'Algoritmos': {'horario': 'segunda 10:00-12:00', 'pre_requisitos': ['Calculo 1']},
    'Fundamentos de Sistemas Inteligentes': {'horario': 'terça 08:00-10:00', 'pre_requisitos': ['Algoritmos']},
    'Redes de Computadores': {'horario': 'quarta 14:00-16:00', 'pre_requisitos': ['Algoritmos']},
    'Banco de Dados': {'horario': 'quinta 08:00-10:00', 'pre_requisitos': ['Calculo 1']},
    'Estruturas de Dados': {'horario': 'sexta 10:00-12:00', 'pre_requisitos': ['Algoritmos']},
    'Inteligência Artificial': {'horario': 'quarta 08:00-10:00', 'pre_requisitos': ['Fundamentos de Sistemas Inteligentes']},
    'Sistemas Operacionais': {'horario': 'terça 14:00-16:00', 'pre_requisitos': ['Algoritmos']},
}

def gerar_horario():
    return [random.randint(1, NUM_DISCIPLINAS) for _ in range(TAMANHO_PERIODO * NUM_PERIODOS)]

def calcular_media_desvio(lista):
    mean = np.mean(lista)
    std = np.std(lista)
    return mean, std

def gerar_horario_aleatorio():
    horarios = []
    disciplinas_disponiveis = list(disciplinas.keys())
    for _ in range(NUM_PERIODOS):
        horario_periodo = []
        for _ in range(TAMANHO_PERIODO):
            horario_periodo.append(random.choice(disciplinas_disponiveis))
        horarios.append(horario_periodo)
    return horarios

def gerar_horario_manual():
    horarios = []
    for periodo in range(NUM_PERIODOS):
        horario = []
        for disciplina in range(TAMANHO_PERIODO):
            horario.append(input(f"Disciplina para o período {periodo} - horário {disciplina}: "))
        horarios.append(horario)
    return horarios

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
    im = ax.imshow(data, cmap='plasma', interpolation='nearest')

    # Definir rótulos e títulos
    ax.set_xticks(np.arange(days))
    ax.set_yticks(np.arange(periods))
    ax.set_xticklabels(['Seg', 'Ter', 'Qua', 'Qui', 'Sex'])  # Dias da semana
    ax.set_yticklabels(np.arange(1, periods + 1))  # Períodos

    # Barra de cores
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.set_label('Disciplina Alocada')
    
    # Título do gráfico
    plt.title(f'Alocação de Disciplinas - {label}')

    # Rótulos dos eixos
    plt.xlabel('Dias da Semana')
    plt.ylabel('Períodos')
    
    # Salvar a imagem antes de mostrar
    if otimizacao == 'antes':
        plt.savefig('saida/antes_otimizacao.png')
    elif otimizacao == 'depois':
        plt.savefig('saida/depois_otimizacao.png')
    
    # Mostrar o gráfico
    plt.show()
    plt.close()


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
            conflitos += 1  # Se a disciplina não existir, conta como conflito

    return conflitos,


def inicializar_populacao(pop_size):
    populacao = []
    for _ in range(pop_size):
        # Criação de um indivíduo 
        individuo = gerar_horario_aleatorio()  
        populacao.append(individuo)
    
    return populacao

#Seleção é a própria seleção natural que vai eliminar os mais fracos
def selecao(populacao, n):
    return tools.selRoulette(populacao, n)

#Cruzamento é a mistura entre dois individuos 
def crossover(individuo1, individuo2):
    return tools.cxUniform(individuo1, individuo2, indpb=0.5)  

#Surgimento de novas caracteristicas
def mutacao(individuo, indpb=0.05):
    return tools.mutShuffleIndexes(individuo, indpb)

def diversity(population):
    unique_individuals = set(map(tuple, population))
    return len(unique_individuals) / len(population)

def algoritmo_genetico(pop_size=100, n_gen=500):
    #NEVALS é o numero de avaliações na ultima geração
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    stats.register("diversity", diversity)
    
    # Inicialização personalizada da população
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
toolbox.register("mate", crossover)  
toolbox.register("mutate", mutacao)  
toolbox.register("select", selecao)

def imprimir_populacao(populacao, mensagem=""):
    print(mensagem)
    for ind in populacao:
        print(ind)
        
def acompanhar_estatisticas(logbook):
    for gen in logbook:
        print(f"Geração {gen['gen']} - Melhor Fitness: {gen['min']}")

def acompanhar_estatisticas_geracao(logbook, geracao):
    gen = logbook[geracao]
    print(f"Geração {gen['gen']} - Melhor Fitness: {gen['min']}")


def sucesso():
    # Número de conflitos de horário na solução inicial
    print("Número de conflitos de horário na solução inicial:", len(horarios_iniciais))

    # Número de conflitos de horário na solução otimizada
    print("Número de conflitos de horário na solução otimizada:", len(horarios_otimizados_depois))

    # Cálculo de média e desvio padrão para as estatísticas
    media_inicial, desvio_inicial = calcular_media_desvio(fit_mins)
    print("Média de conflitos de horário mínima:", media_inicial)
    print("Desvio padrão de conflitos de horário mínima:", desvio_inicial)

    media_media, desvio_media = calcular_media_desvio(fit_avgs)
    print("Média de conflitos de horário média:", media_media)
    print("Desvio padrão de conflitos de horário média:", desvio_media)

    media_maxima, desvio_maxima = calcular_media_desvio(fit_maxs)
    print("Média de conflitos de horário máxima:", media_maxima)
    print("Desvio padrão de conflitos de horário máxima:", desvio_maxima)

def grafico():
    gen = range(1, len(fit_avgs) + 1)  

    plt.figure(figsize=(8, 6))
    plt.plot(gen, fit_avgs, label='Média de Conflitos')
    plt.title('Evolução da Média de Conflitos ao Longo das Gerações')
    plt.xlabel('Geração')
    plt.ylabel('Média de Conflitos')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    horarios_iniciais = gerar_horario_inicial()
    plot_horarios(horarios_iniciais, 'Inicial', 'antes')

    pop_final, logbook = algoritmo_genetico(n_gen=500)

    gen = logbook.select("gen")
    fit_mins = logbook.select("min")
    fit_avgs = logbook.select("avg")
    fit_maxs = logbook.select("max")
    diversity = logbook.select("diversity")
    
    #Horários otimizados pós algoritmo genético
    horarios_otimizados_depois = criar_cromossomo(disciplinas, NUM_PERIODOS, TAMANHO_PERIODO)
    plot_horarios(horarios_otimizados_depois, 'Otimizado', 'depois')
     
    num_periodos = 4
    tamanho_periodo = 5
    horarios_finais = criar_cromossomo(disciplinas, num_periodos, tamanho_periodo)
    imprimir_horarios_finais(horarios_finais)
    for periodo in horarios_finais:
        print(periodo)
        
