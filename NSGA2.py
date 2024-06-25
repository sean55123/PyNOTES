import numpy as np
import random
import matplotlib.pyplot as plt


class nsga2:
    def __init__(self, pop_size):
        self.pop_size = pop_size

    def initialize_population(self, xMax, xMin, decimal):
        population = np.array(list(map(lambda x, y, z: np.round(np.random.uniform(x, y, size=self.pop_size), z), xMax, xMin, decimal)))
        individual(population)
        return population

class individual:
    def __init__(self, x):
        self.x = x
        self.rank = None
        self.objective = 0
        self.crowding_distance = 0

def evaluate_population(objective_function, population):
    print(individual.x)
    for individual in population:
        individual.objectives = objective_function(individual.x)

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
        for i in range(1, len(front) - 1):
            front[i].crowding_distance += (front[i + 1].objectives[m] - front[i - 1].objectives[m]) / (max(front, key=lambda x: x.objectives[m]).objectives[m] - min(front, key=lambda x: x.objectives[m]).objectives[m])

def selection(population, fronts):
    mating_pool = []
    for front in fronts:
        calculate_crowding_distance(front)
        front.sort(key=lambda x: (x.rank, -x.crowding_distance))
        mating_pool.extend(front)
    return mating_pool

def crossover_and_mutation(mating_pool, pop_size, xMax, xMin):
    offspring = []
    while len(offspring) < pop_size:
        parent1 = random.choice(mating_pool)
        parent2 = random.choice(mating_pool)
        child_x = (parent1.x + parent2.x) / 2  # Simple crossover
        if random.random() < 0.1:  # Mutation probability
            child_x += random.uniform(-0.1, 0.1)
        child_x = np.clip(child_x, xMax, xMin)
        offspring.append(child_x)
    return offspring

def optimize(n_iterations, xMax, xMin, decimal, objective_function, model, name, wbpath, data_label):
    population = model.initialize_population(xMax, xMin, decimal)
    evaluate_population(objective_function, population)
    
    for gen in range(n_iterations):
        fronts = non_dominated_sort(population)
        mating_pool = selection(population, fronts)
        offspring = crossover_and_mutation(mating_pool, model.pop_size, xMax, xMin)
        evaluate_population(offspring)
        combined_population = population + offspring
        fronts = non_dominated_sort(combined_population)
        new_population = []
        for front in fronts:
            if len(new_population) + len(front) <= model.pop_size:
                new_population.extend(front)
            else:
                front.sort(key=lambda x: x.crowding_distance, reverse=True)
                new_population.extend(front[:model.pop_size - len(new_population)])
                break
        population = new_population
    
    f1_values = [ind.objectives[0] for ind in population]
    f2_values = [ind.objectives[1] for ind in population]
    plt.figure(figsize=(10, 6))
    plt.scatter(f1_values, f2_values, c='blue', marker='o')
    plt.title('NSGA-II Results: Objective Space')
    plt.xlabel('Objective 1 (f1)')
    plt.ylabel('Objective 2 (f2)')
    plt.grid(True)
    plt.show()


# for ind in final_population:
#     print(f"x: {ind.x}, f1: {ind.objectives[0]}, f2: {ind.objectives[1]}")
