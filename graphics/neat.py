import MultiNEAT as NEAT
from MultiNEAT.viz import DrawPhenotype
from MultiNEAT.viz import render_nn
import cv2
import numpy as np


import matplotlib.pyplot as plt
from MultiNEAT import EvaluateGenomeList_Serial
# To begin evolution, we need to create a seed genome and a population from it.
# Before everything though, we create an object which holds all parameters used by NEAT:


params = NEAT.Parameters()

params.PopulationSize = 100
params.MutateAddNeuronProb=0.1

# This is usually the point where all custom values for the parameters are set.
# Here we set the population size to 100 individuals (default value is 300).
# Now we create a genome with 3 inputs and 2 outputs:


genome = NEAT.Genome(0, 3, 0, 2, False, NEAT.ActivationFunction.UNSIGNED_SIGMOID, NEAT.ActivationFunction.UNSIGNED_SIGMOID, 0, params)

# Notice that we set more properties of the genome than just number of inputs/outputs.
# Also, if the number of inputs you're going to use in your project is 2, you need to write 3 in the constructor.
# Always add one extra input.
# The last input is always used as bias and also when you activate the network always set the last input to 1.0
# (or any other constant non-zero value). The type of activation function of the outputs and hidden neurons is also set. Hidden neurons are optional.
# After the genome is created, we create the population like this:


pop = NEAT.Population(genome, params, True, 1.0,1)
print(pop.GetSearchMode())

def evaluate(genome):

    # this creates a neural network (phenotype) from the genome

    net = NEAT.NeuralNetwork()
    genome.BuildPhenotype(net)

    # let's input just one pattern to the net, activate it once and get the output

    net.Input( [ 1.0, 0.0, 1.0 ] )
    net.Activate()
    output = net.Output()

    # the output can be used as any other Python iterable. For the purposes of the tutorial,
    # we will consider the fitness of the individual to be the neural network that outputs constantly
    # 0.0 from the first output (the second output is ignored)

    fitness = 1.0 - output[0]
     # draw the phenotype
    img = np.zeros((250, 250, 3), dtype=np.uint8)
    img += 10
    DrawPhenotype(img, (0, 0, 250, 250), net )
    cv2.imshow("current best", img)
    cv2.waitKey(1)
    return fitness

for generation in range(100): # run for 100 generations

    # retrieve a list of all genomes in the population
    genome_list = NEAT.GetGenomeList(pop)


    # apply the evaluation function to all genomes
    fitnesses = []
    for genome in genome_list:
        fitness = evaluate(genome)
        fitnesses.append(fitness)
        genome.SetFitness(fitness)

        net = NEAT.NeuralNetwork()
        genome.BuildPhenotype(net)


    # at this point we may output some information regarding the progress of evolution, best fitness, etc.
    # it's also the place to put any code that tracks the progress and saves the best genome or the entire
    # population. We skip all of this in the tutorial.
    print('Gen: %d Best: %3.5f' % (generation, max(fitnesses)))
    # advance to the next generation
    pop.Epoch()