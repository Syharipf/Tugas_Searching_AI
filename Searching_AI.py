import random
import math

# ====== PARAMETER GA ======
POP_SIZE = 6                # <--- Diperkecil supaya output tidak terlalu panjang
CHROM_LENGTH = 32           
GEN_MAX = 5                 # <--- Generasi diperkecil untuk demo
PC = 0.8                    
PM = 0.01                   
DOMAIN_MIN = -10
DOMAIN_MAX = 10


# ====== DECODE KROMOSOM ======
def decode(chromosome):
    x1_bin = chromosome[:16]
    x2_bin = chromosome[16:]
    x1_int = int(x1_bin, 2)
    x2_int = int(x2_bin, 2)
    x1 = DOMAIN_MIN + (DOMAIN_MAX - DOMAIN_MIN) * x1_int / (2**16 - 1)
    x2 = DOMAIN_MIN + (DOMAIN_MAX - DOMAIN_MIN) * x2_int / (2**16 - 1)
    return x1, x2


# ====== FUNGSI FITNESS ======
def fitness(x1, x2):
    try:
        value = -(math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) + (3 / 4) * math.exp(1 - math.sqrt(x1 ** 2)))
    except:
        value = float('inf')
    return value


# ====== RANDOM KROMOSOM ======
def random_chromosome():
    return ''.join(random.choice('01') for _ in range(CHROM_LENGTH))


# ====== INISIALISASI POPULASI ======
def initialize_population():
    return [random_chromosome() for _ in range(POP_SIZE)]


# ====== SELEKSI ORANGTUA (ROULETTE WHEEL) ======
def select_parents(population, fitnesses):
    total_fit = sum(1 / (f + 1e-6) for f in fitnesses)
    pick = random.uniform(0, total_fit)
    current = 0
    for chrom, fit in zip(population, fitnesses):
        current += 1 / (fit + 1e-6)
        if current >= pick:
            return chrom
    return population[-1]


# ====== CROSSOVER ======
def crossover(parent1, parent2):
    if random.random() < PC:
        point = random.randint(1, CHROM_LENGTH - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    else:
        return parent1, parent2


# ====== MUTASI ======
def mutate(chromosome):
    new_chrom = ''
    for gene in chromosome:
        if random.random() < PM:
            new_chrom += '1' if gene == '0' else '0'
        else:
            new_chrom += gene
    return new_chrom


# ====== ALGORITMA UTAMA (OUTPUT BERTAHAP) ======
def genetic_algorithm():
    population = initialize_population()
    best_chrom = None
    best_fit = float('inf')

    for gen in range(GEN_MAX):
        print(f"\n=== Generasi {gen} ===")
        decoded = [decode(chrom) for chrom in population]
        fitnesses = [fitness(x1, x2) for x1, x2 in decoded]

        print("\nPopulasi dan Fitness:")
        for i, (chrom, fit) in enumerate(zip(population, fitnesses)):
            x1, x2 = decode(chrom)
            print(f" Individu {i+1}: {chrom} | x1 = {x1:.4f}, x2 = {x2:.4f}, Fitness = {fit:.6f}")

        # Cek solusi terbaik
        for chrom, fit in zip(population, fitnesses):
            if fit < best_fit:
                best_chrom = chrom
                best_fit = fit

        # Membuat populasi baru
        new_population = []
        while len(new_population) < POP_SIZE:
            # Pilih orangtua
            parent1 = select_parents(population, fitnesses)
            parent2 = select_parents(population, fitnesses)
            print(f"\nSelected Parents:")
            print(f" Parent 1: {parent1}")
            print(f" Parent 2: {parent2}")

            # Crossover
            child1, child2 = crossover(parent1, parent2)
            print(f" After Crossover:")
            print(f" Child 1: {child1}")
            print(f" Child 2: {child2}")

            # Mutasi
            child1 = mutate(child1)
            child2 = mutate(child2)
            print(f" After Mutation:")
            print(f" Child 1: {child1}")
            print(f" Child 2: {child2}")

            new_population.append(child1)
            if len(new_population) < POP_SIZE:
                new_population.append(child2)

        population = new_population

    # Output akhir
    best_x1, best_x2 = decode(best_chrom)
    print("\n=== HASIL AKHIR ===")
    print(f"Kromosom Terbaik : {best_chrom}")
    print(f"Nilai x1         : {best_x1:.6f}")
    print(f"Nilai x2         : {best_x2:.6f}")
    print(f"Fitness Terbaik  : {best_fit:.6f}")


# ====== EKSEKUSI PROGRAM ======
if __name__ == "__main__":
    genetic_algorithm()
