import random
from itertools import product

# Simplified genetic algorithm parameters
population_size = 300
number_of_generations = 10000
mutation_rate = 0.1
PAIRS_PER_SOLUTION = 6  # Number of adjective-noun pairs per solution

# Define adjectives and nouns lists for both languages
adjectives = {
    "english": [
        "ancient",
        "arid",
        "awkward",
        "bitter",
        "brief",
        "bright",
        "busy",
        "calm",
        "chaotic",
        "cheerful",
        "clean",
        "clever",
        "cloudy",
        "clumsy",
        "cold",
        "cool",
        "dark",
        "delicious",
        "dirty",
        "distant",
        "dry",
        "dull",
        "dumb",
        "elegant",
        "eternal",
        "fiery",
        "foolish",
        "fresh",
        "frozen",
        "gentle",
        "gigantic",
        "gleaming",
        "glowing",
        "graceful",
        "happy",
        "hard",
        "heavy",
        "hidden",
        "hot",
        "huge",
        "humid",
        "inept",
        "joyful",
        "light",
        "lonely",
        "long",
        "lost",
        "loud",
        "massive",
        "matte",
        "messy",
        "mighty",
        "minute",
        "modern",
        "mystical",
        "new",
        "noisy",
        "old",
        "optimistic",
        "orderly",
        "peaceful",
        "pessimistic",
        "polished",
        "quick",
        "quiet",
        "radiant",
        "rainy",
        "rotten",
        "rough",
        "rustic",
        "sad",
        "salty",
        "serene",
        "shattered",
        "shiny",
        "short",
        "silent",
        "skillful",
        "sleek",
        "small",
        "smart",
        "snowy",
        "soft",
        "sorrowful",
        "sour",
        "spicy",
        "stormy",
        "sunny",
        "sweet",
        "tall",
        "tiny",
        "vast",
        "vibrant",
        "wandering",
        "warm",
        "wet",
        "whispering",
        "windy",
        "wise",
        "young",
    ],
    "polish": [
        "aktywny",
        "bezpieczny",
        "blady",
        "bliski",
        "bogaty",
        "brzydki",
        "cichy",
        "ciekawy",
        "ciemny",
        "cienki",
        "cudowny",
        "czarny",
        "czerwony",
        "czysty",
        "daleki",
        "dumny",
        "energetyczny",
        "gadatliwy",
        "gotowy",
        "gruby",
        "jasny",
        "jedyny",
        "kolorowy",
        "konieczny",
        "konkretny",
        "kulisty",
        "lepszy",
        "lodowaty",
        "lojalny",
        "luksusowy",
        "martwy",
        "mniejszy",
        "mocny",
        "naiwny",
        "naturalny",
        "niebieski",
        "niedrogi",
        "nietykalny",
        "normalny",
        "nowoczesny",
        "ogromny",
        "oporny",
        "osobisty",
        "ostatni",
        "otwarty",
        "perfekcyjny",
        "pewny",
        "pilny",
        "pionowy",
        "pogodny",
        "pokorny",
        "polski",
        "popularny",
        "prawdziwy",
        "prawny",
        "prosty",
        "przyjemny",
        "przypadkowy",
        "pusty",
        "pyszny",
        "racjonalny",
        "rzadki",
        "samotny",
        "silny",
        "skromny",
        "skuteczny",
        "smaczny",
        "smutny",
        "spokojny",
        "stary",
        "stonowany",
        "suchy",
        "surowy",
        "sympatyczny",
        "szczery",
        "szeroki",
        "szybki",
        "trafny",
        "twardy",
        "widowiskowy",
        "wielki",
        "wolny",
        "wyboisty",
        "wygodny",
        "wysoki",
        "zabawny",
        "zachwycony",
        "zadowolony",
        "zagadkowy",
        "zakrzywiony",
        "zaskoczony",
        "zdalny",
        "zdeprawowany",
        "zdolny",
        "zdrowy",
        "zgrabny",
        "zielony",
        "zimowy",
        "znany",
        "zwarty",
    ],
}

nouns = {
    "english": [
        "air",
        "archipelago",
        "ash",
        "asteroid",
        "beach",
        "blizzard",
        "branch",
        "canyon",
        "castle",
        "cave",
        "cliff",
        "cloud",
        "continent",
        "creek",
        "desert",
        "dimension",
        "dirt",
        "dream",
        "drought",
        "earth",
        "eclipse",
        "field",
        "fire",
        "flame",
        "flood",
        "flower",
        "frog",
        "forest",
        "galaxy",
        "glacier",
        "glass",
        "grass",
        "grove",
        "hill",
        "hurricane",
        "ice",
        "illusion",
        "island",
        "jungle",
        "jupiter",
        "lake",
        "leaf",
        "light",
        "lightning",
        "meadow",
        "metal",
        "meteor",
        "mirage",
        "mist",
        "moon",
        "mountain",
        "mud",
        "nebula",
        "nightmare",
        "oasis",
        "ocean",
        "paper",
        "path",
        "peak",
        "peninsula",
        "planet",
        "plateau",
        "pond",
        "prairie",
        "quasar",
        "rain",
        "reality",
        "river",
        "riverbank",
        "rock",
        "root",
        "sand",
        "savannah",
        "sea",
        "shadow",
        "sky",
        "smoke",
        "snow",
        "space",
        "spring",
        "star",
        "steam",
        "stone",
        "storm",
        "sun",
        "system",
        "thunder",
        "time",
        "tornado",
        "tree",
        "universe",
        "valley",
        "vision",
        "void",
        "volcano",
        "water",
        "waterfall",
        "wave",
        "wind",
        "wood",
    ],
    "polish": [
        "adapter",
        "aktor",
        "alarm",
        "aparat",
        "asfalt",
        "atencjusz",
        "balon",
        "beton",
        "bilet",
        "blender",
        "cygaro",
        "dach",
        "dron",
        "dysk",
        "ekran",
        "ekspres",
        "faks",
        "film",
        "fotel",
        "gitara",
        "gong",
        "grill",
        "hak",
        "hetman",
        "hotel",
        "humor",
        "internet",
        "jacht",
        "kabel",
        "kajak",
        "kaloryfer",
        "kangur",
        "karabin",
        "karton",
        "kask",
        "kij",
        "klakson",
        "klocek",
        "klucz",
        "kompas",
        "komputer",
        "kontakt",
        "koral",
        "kot",
        "kran",
        "kredens",
        "krem",
        "kubek",
        "kufel",
        "kwarc",
        "kwiat",
        "laptop",
        "lornetka",
        "lustro",
        "magnet",
        "mikrofon",
        "monitor",
        "most",
        "motyl",
        "namiot",
        "nos",
        "notes",
        "obiektyw",
        "obraz",
        "ocean",
        "odkurzacz",
        "okno",
        "organizator",
        "ornament",
        "palec",
        "parasol",
        "piec",
        "pies",
        "pilot",
        "poduszkowiec",
        "pomnik",
        "port",
        "projektor",
        "przejazd",
        "przybornik",
        "robot",
        "rower",
        "rybak",
        "samolot",
        "satelita",
        "sedes",
        "telefon",
        "telewizor",
        "ubranie",
        "wagon",
        "wazon",
        "wiatr",
        "wilk",
        "zamek",
        "zapalnik",
        "zasobnik",
        "zastrzyk",
        "zebra",
        "zegar",
        "zszywacz",
    ],
}


def find_duplicates(words):
    seen = set()
    duplicates = set()
    for word in words:
        if word in seen:
            duplicates.add(word)
        else:
            seen.add(word)
    return duplicates


def validate_lists():
    for language, adjs in adjectives.items():
        adj_set = set(adjs)
        if len(adj_set) != 100:
            dup_count = len(adjs) - len(adj_set)
            duplicates = find_duplicates(adjs)
            raise ValueError(
                f"Adjectives list for {language} contains {len(adjs)} elements with {dup_count} duplicates ({', '.join(duplicates)}), expected 100 unique elements."
            )
    for language, ns in nouns.items():
        noun_set = set(ns)
        if len(noun_set) != 100:
            dup_count = len(ns) - len(noun_set)
            duplicates = find_duplicates(ns)
            raise ValueError(
                f"Nouns list for {language} contains {len(ns)} elements with {dup_count} duplicates ({', '.join(duplicates)}), expected 100 unique elements."
            )


# Call the validation function to check the lists
validate_lists()


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
def genetic_algorithm(language="english"):
    selected_adjectives = adjectives[language]
    selected_nouns = nouns[language]
    population = initialize_population(selected_adjectives, selected_nouns)
    for _ in range(number_of_generations):
        parents = select_parents(population)
        new_generation = crossover(parents)
        new_generation = [
            mutate(child, selected_adjectives, selected_nouns)
            for child in new_generation
        ]
        population = new_generation

    best_solution = max(population, key=calculate_fitness)
    return best_solution, calculate_fitness(best_solution)


# Language selection
language = input("Select language (english/polish): ").lower()
while language not in ["english", "polish"]:
    print("Invalid language selection.")
    language = input("Select language (english/polish): ").lower()

# Execute the genetic algorithm using the selected language
best_solution, best_score = genetic_algorithm(language)

# Format and print the best solution
formatted_phrases = [
    '  "{} {}"'.format(adj.capitalize(), noun.capitalize())
    for adj, noun in best_solution
]
formatted_output = ",\n".join(formatted_phrases)
print("Best Score:", best_score)
print("Best Solution as Phrases:\n[\n{}\n]".format(formatted_output))
