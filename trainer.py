import random
import multiprocessing

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

from joblib import Parallel, delayed

from tetris import Tetris
from agent import Agent

POPULATION = 40
GENERATIONS = 15

WIDTH = 10
HEIGHT = 20


class Chromosome:

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = 0


class Trainer:

    def __init__(self):
        self.chromosomes = [Chromosome([random.uniform(-1, 1) for _ in range(4)]) for _ in range(POPULATION)]

    def select(self):
        """"""
        self.chromosomes.sort(key=lambda chromosome: chromosome.fitness)
        self.chromosomes = self.chromosomes[::-1][:POPULATION // 2]

    def reproduce(self):
        """"""
        pool = self.chromosomes[:]
        while len(self.chromosomes) < POPULATION:
            chromosomes = self.crossover(pool)
            for chromosome in chromosomes:
                self.mutate(chromosome)
            self.chromosomes.extend(chromosomes)

    def crossover(self, pool):
        """"""
        parents = [random.choice(pool), random.choice(pool)]
        children = []
        if random.random() < 0.85:
            i = random.randint(0, 3)
            children.append(Chromosome(parents[0].chromosome[:i] + parents[1].chromosome[i:]))
            children.append(Chromosome(parents[1].chromosome[:i] + parents[0].chromosome[i:]))
        else:
            children.append(Chromosome(parents[0].chromosome[:]))
            children.append(Chromosome(parents[1].chromosome[:]))
        return children

    def mutate(self, chromosome):
        """"""
        for i in range(4):
            if random.random() < 0.05:
                chromosome.chromosome[i] = random.uniform(-1, 1)

    def evaluate(self, chromosome, seed):
        """"""
        agent = Agent(chromosome.chromosome)
        game = Tetris(WIDTH, HEIGHT, 0, 0, seed)
        while game.state != 0:
            agent.play(game, game.current_tetromino, game.grid)
            game.update()
        chromosome.fitness = game.score.score
        print(f'Fitness: {chromosome.fitness}')
        return chromosome

    def get_solution(self):
        """"""
        for i in range(GENERATIONS):
            print(f'=== Generation {i} ===\n')
            seed = random.randint(0, 99)
            self.chromosomes = Parallel(n_jobs=-1)(delayed(self.evaluate)(chromosome, seed) for chromosome in self.chromosomes)
            fitnesses = [chromosome.fitness for chromosome in self.chromosomes]
            print(f'\nAverage: {sum(fitnesses) / POPULATION}')
            print(f'Minimum: {min(fitnesses)}')
            print(f'Maximum: {max(fitnesses)}\n')
            self.select()
            self.reproduce()
        return max(self.chromosomes, key=lambda chromosome: chromosome.fitness).chromosome


# progress bar?

# [0.760666, -0.510066, -0.184483, -0.35663]
# [0.12642928451627444, -0.5942505141752759, -0.4878447647500257, -0.6599707308739864] - 44681.0
# [0.5180391994404643, -0.8547864639326359, -0.44058523366400215, -0.08594419661904484] - 497442.8
# [0.7837095684471436, -0.898865132380853, -0.2885922822019038, -0.44284669938161314] - 3134715.6

if __name__ == '__main__':
    trainer = Trainer()
    print(trainer.get_solution())
