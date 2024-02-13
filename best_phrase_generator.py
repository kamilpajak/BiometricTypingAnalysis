import random
from itertools import product

# Simplified genetic algorithm parameters
population_size = 100
number_of_generations = 1000
mutation_rate = 0.1
PAIRS_PER_SOLUTION = (
    5  # Set the number of adjective-noun pairs per solution as a constant
)


# Define adjectives and nouns lists
adjectives = [
    "Quick",
    "Dark",
    "Bright",
    "Silent",
    "Ancient",
    "Mighty",
    "Gentle",
    "Frozen",
    "Fiery",
    "Hidden",
    "Serene",
    "Vast",
    "Wandering",
    "Lost",
    "Eternal",
    "Distant",
    "Glowing",
    "Whispering",
    "Shattered",
    "Lonely",
    "Radiant",
    "Vibrant",
    "Sleek",
    "Rough",
    "Soft",
    "Hard",
    "Heavy",
    "Light",
    "Massive",
    "Tiny",
    "Huge",
    "Small",
    "Gigantic",
    "Minute",
    "Tall",
    "Short",
    "Long",
    "Brief",
    "Ancient",
    "Modern",
    "Old",
    "Young",
    "New",
    "Fresh",
    "Rotten",
    "Delicious",
    "Sweet",
    "Bitter",
    "Sour",
    "Salty",
    "Spicy",
    "Warm",
    "Cool",
    "Cold",
    "Hot",
    "Wet",
    "Dry",
    "Humid",
    "Arid",
    "Rainy",
    "Sunny",
    "Cloudy",
    "Stormy",
    "Snowy",
    "Windy",
    "Calm",
    "Busy",
    "Quiet",
    "Loud",
    "Noisy",
    "Peaceful",
    "Chaotic",
    "Orderly",
    "Messy",
    "Clean",
    "Dirty",
    "Gleaming",
    "Dull",
    "Shiny",
    "Matte",
    "Polished",
    "Rustic",
    "Elegant",
    "Clumsy",
    "Graceful",
    "Awkward",
    "Skillful",
    "Inept",
    "Clever",
    "Dumb",
    "Smart",
    "Wise",
    "Foolish",
    "Happy",
    "Sad",
    "Joyful",
    "Sorrowful",
    "Optimistic",
    "Pessimistic",
    "Cheerful",
]

nouns = [
    "Forest",
    "Shadow",
    "River",
    "Mountain",
    "Star",
    "Ocean",
    "Flame",
    "Castle",
    "Cloud",
    "Wind",
    "Meadow",
    "Void",
    "Peak",
    "Light",
    "Grove",
    "Path",
    "Island",
    "Moon",
    "Sun",
    "Wave",
    "Rock",
    "Tree",
    "Leaf",
    "Branch",
    "Root",
    "Flower",
    "Grass",
    "Mud",
    "Dirt",
    "Sand",
    "Stone",
    "Water",
    "Fire",
    "Sky",
    "Earth",
    "Air",
    "Metal",
    "Wood",
    "Paper",
    "Glass",
    "Rain",
    "Snow",
    "Ice",
    "Steam",
    "Fog",
    "Smoke",
    "Ash",
    "Mist",
    "Thunder",
    "Lightning",
    "Storm",
    "Hurricane",
    "Tornado",
    "Blizzard",
    "Flood",
    "Drought",
    "Desert",
    "Jungle",
    "Prairie",
    "Hill",
    "Valley",
    "Riverbank",
    "Beach",
    "Sea",
    "Ocean",
    "Lake",
    "Pond",
    "Spring",
    "Waterfall",
    "Creek",
    "Cave",
    "Canyon",
    "Cliff",
    "Plateau",
    "Peninsula",
    "Island",
    "Continent",
    "Planet",
    "Star",
    "Galaxy",
    "Universe",
    "Space",
    "Dimension",
    "Time",
    "Reality",
    "Dream",
    "Nightmare",
    "Vision",
    "Illusion",
    "Mirage",
]


# Function to extract all unique two-letter combinations from a list of words
def extract_combinations(words):
    combinations = set()
    for word in words:
        word = word.lower()  # Ensure uniformity in case
        for i in range(len(word) - 1):
            combinations.add(word[i : i + 2])
    return combinations


# Initialize the population with random solutions
def initialize_population(adjectives, nouns):
    population = []
    for _ in range(population_size):
        pairs = random.sample(list(product(adjectives, nouns)), PAIRS_PER_SOLUTION)
        population.append(pairs)
    return population


# Fitness function to calculate the total unique two-letter combinations
def calculate_fitness(solution):
    words = [adj + " " + noun for adj, noun in solution]
    all_combinations = extract_combinations(words)
    return len(all_combinations)


# Selection function to choose parent solutions
def select_parents(population):
    fitness_scores = [calculate_fitness(solution) for solution in population]
    sorted_population = [
        x
        for _, x in sorted(
            zip(fitness_scores, population), key=lambda pair: pair[0], reverse=True
        )
    ]
    return sorted_population[: len(sorted_population) // 2]


# Crossover function to create new solutions
def crossover(parents):
    new_generation = []
    while len(new_generation) < population_size:
        parent1, parent2 = random.sample(parents, 2)
        crossover_point = random.randint(1, PAIRS_PER_SOLUTION - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        new_generation.append(child)
    return new_generation


# Mutation function to introduce variability
def mutate(solution, adjectives, nouns):
    if random.random() < mutation_rate:
        mutation_index = random.randint(0, PAIRS_PER_SOLUTION - 1)
        solution[mutation_index] = (random.choice(adjectives), random.choice(nouns))
    return solution


# Genetic algorithm main loop
def genetic_algorithm(adjectives, nouns):
    population = initialize_population(adjectives, nouns)
    for _ in range(number_of_generations):
        parents = select_parents(population)
        new_generation = crossover(parents)
        new_generation = [mutate(child, adjectives, nouns) for child in new_generation]
        population = new_generation

    # Find the best solution in the final population
    best_solution = max(population, key=calculate_fitness)
    return best_solution, calculate_fitness(best_solution)


# Example execution with a limited set of words
best_solution, best_score = genetic_algorithm(
    adjectives[:20], nouns[:20]
)  # Use subsets for demonstration
print("Best Score:", best_score)
print("Best Solution:", best_solution)
