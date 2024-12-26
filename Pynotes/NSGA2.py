import numpy as np
import random
import matplotlib.pyplot as plt
import csv
import os

class NSGA:
    def __init__(self, pop_size, mutation_rate):
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate

class Individual:
    def __init__(self, x):
        self.x = x
        self.objectives = objective_functions(x)
        self.rank = None
        self.crowding_distance = 0

def initialize_population(pop_size, xMax, xMin, decimal):
    population = []
    for _ in range(pop_size):
        x = np.random.uniform(xMax, xMin)
        x = np.array([round(x[i], decimal[i]) for i in range(len(x))])
        individual = Individual(x)
        population.append(individual)
    return population

def evaluate_population(population):
    for individual in population:
        individual.objectives = objective_functions(individual.x)

def non_dominated_sort(population):
    fronts = [[]]
    for p in population:
        p.domination_count = 0
        p.dominated_solutions = []
        for q in population:
            if dominates(p, q):
                p.dominated_solutions.append(q)
            elif dominates(q, p):
                p.domination_count += 1
        if p.domination_count == 0:
            p.rank = 0
            fronts[0].append(p)
    
    i = 0
    while len(fronts[i]) > 0:
        next_front = []
        for p in fronts[i]:
            for q in p.dominated_solutions:
                q.domination_count -= 1
                if q.domination_count == 0:
                    q.rank = i + 1
                    next_front.append(q)
        i += 1
        fronts.append(next_front)
    
    return fronts[:-1]

def dominates(p, q):
    return all(p_i <= q_i for p_i, q_i in zip(p.objectives, q.objectives)) and any(p_i < q_i for p_i, q_i in zip(p.objectives, q.objectives))

def calculate_crowding_distance(front):
    if len(front) == 0:
        return
    num_objectives = len(front[0].objectives)
    for individual in front:
        individual.crowding_distance = 0
    for m in range(num_objectives):
        front.sort(key=lambda x: x.objectives[m])
        front[0].crowding_distance = float('inf')
        front[-1].crowding_distance = float('inf')
        
        min_obj = min(front, key=lambda x: x.objectives[m]).objectives[m]
        max_obj = max(front, key=lambda x: x.objectives[m]).objectives[m]

        if max_obj == min_obj:
            for i in range(1, len(front) - 1):
                front[i].crowding_distance = 0
        else:
            for i in range(1, len(front) - 1):
                front[i].crowding_distance += (front[i + 1].objectives[m] - front[i - 1].objectives[m]) / (max_obj - min_obj)

def selection(population, fronts):
    mating_pool = []
    for front in fronts:
        calculate_crowding_distance(front)
        front.sort(key=lambda x: (x.rank, -x.crowding_distance))
        mating_pool.extend(front)
    return mating_pool

def crossover_and_mutation(mating_pool, pop_size, mutation_rate, xMax, xMin, decimal):
    offspring = []
    while len(offspring) < pop_size:
        parent1 = random.choice(mating_pool)
        parent2 = random.choice(mating_pool)
        child_x = (parent1.x + parent2.x) / 2  
        if random.random() < mutation_rate:  
            child_x += np.random.uniform(-0.5, 0.5)
        child_x = np.array([min(max(child_x[i], xMin[i]), xMax[i]) for i in range(len(child_x))])
        child_x = np.array([round(child_x[i], decimal[i]) for i in range(len(child_x))])
        offspring.append(Individual(child_x))
    return offspring

def Record(n, params, score, name, wbpath, data_label):
    value = [n] + list(params) + [score]
    if os.path.isfile(wbpath):
        with open(name, 'a+', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(value)
    else:
        with open(name, 'a+', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data_label)
            writer.writerow(value)


def optimize(n_iterations, xMax, xMin, decimal, objective_function, model, csvfile_name, wbpath, data_label):
    global objective_functions
    pareto_wbpath = csvfile_name + '_Pareto.csv'
    csvfile_name += '_all_data.csv'
    wbpath += '_all_data.csv'
    objective_functions = objective_function
    pop_size = model.pop_size
    mutation_rate = model.mutation_rate
    population = initialize_population(pop_size, xMax, xMin, decimal)
    evaluate_population(population)
    print('-----------------------------------------')
    print("Initialization complete.")
    
    for gen in range(n_iterations):
        fronts = non_dominated_sort(population)
        mating_pool = selection(population, fronts)
        offspring = crossover_and_mutation(mating_pool, pop_size, mutation_rate, xMax, xMin, decimal)
        evaluate_population(offspring)
        combined_population = population + offspring
        fronts = non_dominated_sort(combined_population)
        new_population = []
        for front in fronts:
            if len(new_population) + len(front) <= pop_size:
                new_population.extend(front)
            else:
                front.sort(key=lambda x: x.crowding_distance, reverse=True)
                new_population.extend(front[:pop_size - len(new_population)])
                break
        population = new_population
        for individual in population:
            Record(gen, individual.x, individual.objectives, csvfile_name, wbpath, data_label)
        print('-----------------------------------------')
        print(f"Current generation: {gen}")
    
    recording_pareto(pareto_wbpath, population)

def recording_pareto(pareto_wbpath, population):
    num_objectives = len(population[0].objectives)
    data_label = ['Input ' + str(i+1) for i in range(len(population[0].x))] + ['Objective ' + str(i+1) for i in range(num_objectives)]

    with open(pareto_wbpath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_label)
        for individual in population:
            row = list(individual.x) + individual.objectives
            writer.writerow(row)