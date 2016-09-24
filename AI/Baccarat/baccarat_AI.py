#estimate baccarat winner with NEAT by regressing between number of cards of each type and the output (win bank, win player, tie)

#!/usr/bin/python3


import os
import sys
import time
import random as rnd
import cv2
import numpy as np
import pickle as pickle
import MultiNEAT as NEAT
from MultiNEAT import EvaluateGenomeList_Serial
from MultiNEAT import GetGenomeList, ZipFitness

from concurrent.futures import ProcessPoolExecutor, as_completed
import baccarat_sim;

def evaluate(genome):
    net = NEAT.NeuralNetwork()
    genome.BuildPhenotype(net)

    fitness = 0

    #generate 100 games with 8 decks
    n_games=5
    n_decks=8
    bcc_results = baccarat_sim.generate_games(n_games,n_decks)

    for outcome,cards in bcc_results:
        # net.Flush()
        #the normalised count cards is number of occurences divided by max (4* nr_of_decks)
        input =np.append(np.array(list(cards.values()))/(8*4),[1.0]).astype(np.float64)
        net.Input(input) # can input numpy arrays, too
                                          # for some reason only np.float64 is supported
        net.Activate()
        #bet is either -1,0,1 but output is between 0 and 1
        output_bet = net.Output()[0] *2 -1
        bet = round(output_bet)
        #the error should be differentiable gradient, I think

        fitness += baccarat_sim.payout_map[(bet,outcome)]* (1-abs(bet-output_bet))**2
    return fitness/len(bcc_results)

def play(genome):
    net = NEAT.NeuralNetwork()
    genome.BuildPhenotype(net)
    money=0
    n_games=10
    n_decks=8
    bcc_results = baccarat_sim.generate_games(n_games,n_decks)

    for outcome,cards in bcc_results:
        # net.Flush()
        #the normalised count cards is number of occurences divided by max (4* nr_of_decks)
        input =np.append(np.array(list(cards.values()))/(8*4),[1.0]).astype(np.float64)
        net.Input(input) # can input numpy arrays, too
                                          # for some reason only np.float64 is supported
        net.Activate()
        #bet is either -1,0,1 but output is between 0 and 1
        output_bet = net.Output()[0] *2 -1
        bet = round(output_bet)
        #the error should be differentiable gradient, I think

        money += baccarat_sim.payout_map[(bet,outcome)]
    return money


params = NEAT.Parameters()
params.PopulationSize = 200
params.DynamicCompatibility = True
params.WeightDiffCoeff = 4.0
params.CompatTreshold = 2.0
params.YoungAgeTreshold = 15
params.SpeciesMaxStagnation = 15
params.OldAgeTreshold = 35
params.MinSpecies = 5
params.MaxSpecies = 10
params.RouletteWheelSelection = False
params.RecurrentProb = 0.1
params.OverallMutationRate = 0.8

params.MutateWeightsProb = 0.90

params.WeightMutationMaxPower = 2.5
params.WeightReplacementMaxPower = 5.0
params.MutateWeightsSevereProb = 0.5
params.WeightMutationRate = 0.25

params.MaxWeight = 8

params.MutateAddNeuronProb = 0.1
params.MutateAddLinkProb = 0.1
params.MutateRemLinkProb = 0.04

params.MinActivationA  = 4.9
params.MaxActivationA  = 4.9

params.ActivationFunction_SignedSigmoid_Prob = 0.0
params.ActivationFunction_UnsignedSigmoid_Prob = 1.0
params.ActivationFunction_Tanh_Prob = 0.0
params.ActivationFunction_SignedStep_Prob = 0.0

params.CrossoverRate = 0.75  # mutate only 0.25
params.MultipointCrossoverRate = 0.4
params.SurvivalRate = 0.2

import viz
import matplotlib.pyplot as plt
def getbest(i):

    g = NEAT.Genome(0, 14, 0, 1, False, NEAT.ActivationFunction.UNSIGNED_SIGMOID, NEAT.ActivationFunction.UNSIGNED_SIGMOID, 0, params)
    pop = NEAT.Population(g, params, True, 1.0, i)
    pop.RNG.Seed(i)
    generations=100
    for gen in range(generations):
        genome_list = NEAT.GetGenomeList(pop)
        fitness_list = EvaluateGenomeList_Serial(genome_list, evaluate, display=False)
        NEAT.ZipFitness(genome_list, fitness_list)

        pop.Epoch()
        #visualise
        best = max(fitness_list)
        worst = min(fitness_list)
        net = NEAT.NeuralNetwork()
        pop.Species[0].GetLeader().BuildPhenotype(net)
        img = np.zeros((500, 500, 3), dtype=np.uint8)
        img += 10
        viz.DrawPhenotype(img, (0, 0, 500, 500), net )

        cv2.imshow("CPPN", img)
        cv2.waitKey(1)
        print("Generation:",gen)
        print("Highest fitness:", best)
        print("Lowest fitness", worst)


    return pop.GetBestGenome(),pop.GetBestFitnessEver()


genome,fitness = getbest(1)
print('best fitness', fitness)
nr_of_new_plays=100
multiplier=0
for _ in range(nr_of_new_plays):
    multiplier += play(genome)
print("Average multiplier made over ",nr_of_new_plays," games :", multiplier/nr_of_new_plays)


