import random
import math

# ====== DECODE KROMOSOM ======
def decode(chromosome, domain_min, domain_max):
    x1_bin = chromosome[:16]
    x2_bin = chromosome[16:]
    x1_int = int(x1_bin, 2)
    x2_int = int(x2_bin, 2)
    x1 = domain_min + (domain_max - domain_min) * x1_int / (2**16 - 1)
    x2 = domain_min + (domain_max - domain_min) * x2_int / (2**16 - 1)
    return x1, x2

# ====== FUNGSI FITNESS ======
def fitness(x1, x2):
    try:
        value = -(math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) + (3 / 4) * math.exp(1 - math.sqrt(x1 ** 2)))
    except:
        value = float('inf')
    return value

# ====== RANDOM KROMOSOM ======
def random_chromosome(chrom_length):
    return ''.join(random.choice('01') for _ in range(chrom_length))

# ====== INISIALISASI POPULASI ======
def initialize_population(pop_size, chrom_length):
    return [random_chromosome(chrom_length) for _ in range(pop_size)]

# ====== SELEKSI ORANGTUA (ROULETTE WHEEL) DENGAN INDEKS ======
def select_parent_with_index(population, fitnesses):
    total_fit = sum(1 / (f + 1e-6) for f in fitnesses)
    pick = random.uniform(0, total_fit)
    current = 0
    for idx, (chrom, fit) in enumerate(zip(population, fitnesses)):
        current += 1 / (fit + 1e-6)
        if current >= pick:
            return idx, chrom
    return len(population)-1, population[-1]

# ====== CROSSOVER ======
def crossover(parent1, parent2, pc):
    if random.random() < pc:
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    else:
        return parent1, parent2

# ====== MUTASI ======
def mutate(chromosome, pm):
    new_chrom = ''
    for gene in chromosome:
        if random.random() < pm:
            new_chrom += '1' if gene == '0' else '0'
        else:
            new_chrom += gene
    return new_chrom

# ====== ALGORITMA UTAMA ======
def genetic_algorithm(pop_size, chrom_length, gen_max, pc, pm, domain_min, domain_max):
    population = initialize_population(pop_size, chrom_length)
    best_chrom = None
    best_fit = float('inf')

    for gen in range(gen_max):
        print(f"\n=== Generasi {gen} ===")
        decoded = [decode(chrom, domain_min, domain_max) for chrom in population]
        fitnesses = [fitness(x1, x2) for x1, x2 in decoded]

        print("\nPopulasi dan Fitness:")
        for i, (chrom, fit) in enumerate(zip(population, fitnesses)):
            x1, x2 = decode(chrom, domain_min, domain_max)
            print(f" Individu {i+1}: {chrom} | x1 = {x1:.4f}, x2 = {x2:.4f}, Fitness = {fit:.6f}")

        for chrom, fit in zip(population, fitnesses):
            if fit < best_fit:
                best_chrom = chrom
                best_fit = fit

        new_population = []
        while len(new_population) < pop_size:
            idx1, parent1 = select_parent_with_index(population, fitnesses)
            
            # Pilih parent2 yang tidak sama dengan parent1
            idx2 = idx1
            while idx2 == idx1:
                idx2, parent2 = select_parent_with_index(population, fitnesses)

            print(f"\n\nSelected Parents:")
            print(f" Parent 1 (Individu {idx1+1}): {parent1}")
            print(f" Parent 2 (Individu {idx2+1}): {parent2}")

            child1, child2 = crossover(parent1, parent2, pc)
            print(f"\n After Crossover:")
            print(f" Child 1: {child1}")
            print(f" Child 2: {child2}")

            child1 = mutate(child1, pm)
            child2 = mutate(child2, pm)
            print(f"\n After Mutation:")
            print(f" Child 1: {child1}")
            print(f" Child 2: {child2}")

            new_population.append(child1)
            if len(new_population) < pop_size:
                new_population.append(child2)

        population = new_population

    # Output akhir
    best_x1, best_x2 = decode(best_chrom, domain_min, domain_max)
    print("\n=== HASIL AKHIR ===")
    print(f"Kromosom Terbaik : {best_chrom}")
    print(f"Nilai x1         : {best_x1:.6f}")
    print(f"Nilai x2         : {best_x2:.6f}")
    print(f"Fitness Terbaik  : {best_fit:.6f}")

# ====== EKSEKUSI PROGRAM ======
if __name__ == "__main__":
    print("=== Parameter Algoritma Genetika ===")
    pop_size = int(input("Masukkan ukuran populasi: "))
    chrom_length = 32  # Tetap 32 bit
    gen_max = int(input("Masukkan jumlah generasi: "))
    pc = float(input("Masukkan probabilitas crossover (0-1): "))
    pm = float(input("Masukkan probabilitas mutasi (0-1): "))
    domain_min = -10
    domain_max = 10

    genetic_algorithm(pop_size, chrom_length, gen_max, pc, pm, domain_min, domain_max)
