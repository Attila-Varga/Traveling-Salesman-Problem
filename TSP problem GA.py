#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 10:33:04 2019

@author: Attila Varga
"""

import random
import math

class City:
    
    def __init__(self, x, y):
         self.x = x
         self.y = y
         
    def __str__(self):
        return "City (%s,%s)" % (self.x, self.y)
      
    def distanceTo(self, city):
         """
         Returns the distance between two cities.
         Cities are defined by their x and y coordinates.
         """
         
         return math.sqrt((city.x - self.x)**2 + (city.y - self.y)**2)
     

NUM_CITIES = 7
POPULATION_SIZE = 20
MAX_GENERATIONS = 75
GENOME_LENGTH = NUM_CITIES
MUTATION_RATE = 5
RECOMBINATION_RATE = 5
CITY_LIST = [City(7,8),
             City(6,9),
             City(5,8),
             City(12,-8),
             City(56,78),
             City(-2,6),
             City(4,5)]

START_POINT = CITY_LIST[2]

def initialPopulation():
    """
    Return an initial population of POPULATION SIZE genomes. Each genome is a list of integers, a 
    possible order of visiting the cities, generated randomly.
    """
    
    pop = []
    for i in range(0, POPULATION_SIZE):
        genome = []
        for j in range(GENOME_LENGTH):
            order = list(range(0, NUM_CITIES))
            random.shuffle(order)
            genome = order
        pop.append(genome)
    return pop


def getFitness(aGenome):
    """
    The function calculates the overall fitness of a genome in the population.
    The fitness is the total distance of the cities in the ordering of the genome
    The lower fitness score the better (smaller distance)
    """
    fitness = 0;
    for i in range(GENOME_LENGTH - 1):
       fitness = fitness + CITY_LIST[aGenome[i]].distanceTo(CITY_LIST[aGenome[i+1]])
    #return to start point
    fitness = fitness + CITY_LIST[GENOME_LENGTH].distanceTo(CITY_LIST[0])
    return fitness 


def getBest(currentPopulation):
    """
    Returns a tuple containing the genome with the best fitness score.
    """
    bestFitness = 999999
    for aGenome in currentPopulation:
        fitness = getFitness(aGenome)
        if fitness < bestFitness:
            bestFitness = fitness
            bestTuple = (aGenome, bestFitness)
    return bestTuple


def mutate(aPopulation):
    """
    Iterates over every genome. Every genome 1/MUTATION RATE to mutate.
    When mutation occurs two random elements will swap positions.
    This ensures diversity of the population. 
    """
    for i in range(POPULATION_SIZE):
        if random.randint(1, MUTATION_RATE) == MUTATION_RATE:
            selectedGenome = aPopulation[i]
            mutateBit = random.randint(0, GENOME_LENGTH - 1)
            mutateOtherBit = random.randint(0, GENOME_LENGTH - 1)
            selectedGenome[mutateBit] , selectedGenome[mutateOtherBit] = selectedGenome[mutateOtherBit]  , selectedGenome[mutateBit]


def crossover(matingPool):
    """
    Returns a new population created from mating pool.
    Iterates POPULATION_SIZE/2 times, each time it selectes two random genomes from 
    the mating pool. There is a 1/RECOMBINATION_RATE chance for each pair to swap genetic material.
    To preserve the uniqueness of the chromosomes, the bits before the crossover point will be swapped in the children,
    the rest of the chromosomes will be added in the same order, as they appear in their other parent.
    """
    newPopulation = []
    for i in range(0, int(POPULATION_SIZE / 2)):
        #randomly pick two mates from matingpool
        mate1 = matingPool[random.randint(0, POPULATION_SIZE - 1)]
        mate2 = matingPool[random.randint(0, POPULATION_SIZE - 1)]
        if random.randint(1, RECOMBINATION_RATE) == RECOMBINATION_RATE:
            #the new mates will swap bits at the crossover point
            child1 = []
            child2 = []
            leftover = []
            crossoverPoint = random.randint(1, GENOME_LENGTH)
            for i in range(crossoverPoint):
                child1.append(mate1[i])
                child2.append(mate2[i])     
                
            #get the difference of the two genomes, preserve the order of occurence of the chromosomes
            leftover = [x for x in mate2 if x not in child1]
            child1 += leftover
            leftover = [x for x in mate1 if x not in child2]
            child2 += leftover    
            newPopulation.append(child1)
            newPopulation.append(child2)
            
        else:
            #no genetic material swapped, mates go straight to the new population
            newPopulation.append(mate1)
            newPopulation.append(mate2)
    return newPopulation

def constructMatingPool(currentPopulation):
    """
    Returns a mating pool.
    
    The function picks genomes for mating from the population and 
    adds them to the mating pool. The same genome may be added twice.
    The size of the mating pool is the same as the current population.
    """
    
    matingPool = []
    for i in range(POPULATION_SIZE):
        matingPool.append(selectGenome(currentPopulation))
    return matingPool

def generateNewPopulation(currentPopulation):
    """
    Returns an evolved population from the current population.
    """
    
    matingPool = constructMatingPool(currentPopulation)
    newPopulation = crossover(matingPool)
    mutate(newPopulation)
    return newPopulation

def selectGenome(currentPopulation):
    """
    Selects two genomes randomly from the current population,
    then returns the one with best fitness score
    """
    
    genome1 = random.choice(currentPopulation)
    genome2 = random.choice(currentPopulation)
    if getFitness(genome1) < getFitness(genome2):
        return genome1
    else:
        return genome2
    
def main():
    """
    The main function. Creates an initial populations of genomes, then evolves it over a number
    of generations. Functions ends when solution is found, ow MAX_GENERATIONS have been reached.
    """
    
    population = initialPopulation()
    print('Initial Population')
    print(population)
    print()
    
    genomeTuple = ()
    numOfGenerations = 1
    evolved = False
    
    #put startpoint in the front of the list
    tmp = CITY_LIST[0]
    CITY_LIST[CITY_LIST.index(START_POINT)] = tmp
    CITY_LIST[0] = START_POINT
    CITY_LIST.append(START_POINT)
    
    while numOfGenerations <= MAX_GENERATIONS and not evolved:
        genomeTuple = getBest(population)

        if genomeTuple[1] == 0:
            evolved = True
            print(genomeTuple[0], 'evolved in generation', numOfGenerations)
        else:
            print("Generation: ", numOfGenerations)
            print(population)
            population = generateNewPopulation(population)
            numOfGenerations += 1
    if not evolved:
        print()
        print('After', MAX_GENERATIONS,'generations,The closest one is',genomeTuple[0],'with fitness(distance) of', genomeTuple[1])
    print()
    for i in range(len(population)):
       print(population[i],'Fitness:',getFitness(population[i]))

main()