# Genetic Algorithm

*    Title: Genetic Algorithm     
*    Author: Guillem Nicolau Alomar Sitjes      
*    Initial release: July 13th, 2019                     
*    Code version: 0.1                         
*    Availability: Public     

**Index**
* [Requirements](#requirements)
* [Documentation](#documentation)
    * [Explanation](#explanation)
    * [Project Structure](#project-structure)
* [Using the application](#using-the-application)
    * [Executing](#executing)
    * [Testing](#testing)
* [Decisions taken](#decisions-taken)

## Requirements

- Python +3.6
- numpy==1.16.4

## Documentation

### Explanation

This project is an example of the most classic Genetic Algorithm problem.

**Model**

The model is divided in two parts. The population model and the environment model.

###### Population Model

Each individuals is summarized into a reduced set of parameters, which will be key for his/her future:

- Arm reach: How height can the individual take fruits from trees without jumping.
- Speed: How fast can the individual run.
- Strength: How strong is the individual for fighting.
- Jump: How height can the individual jump.
- Skin Thickness: How thick is the individual skin.

Ranges of values

| Parameter                          | Min  | Max | Units |
|------------------------------------|------|-----|-------|
| Arm reach                          | 2    | 2.5 | m     |
| Speed                              | 10   | 20  | km/h  |
| Strength: Range of values: 1 - 10  | 1    | 10  |       |
| Skin Thickness                     | 0.05 | 2   | mm    |
| Jump                               | 0    | 0.5 | m     |

###### Environment Model

An environment is summarized into a reduced set of parameters, which will be key for the future of the individuals living in it:

- Fruit tree height: At which height are the tree fruits.
- Temperature: Minimum and maximum temperatures.
- Predators speed: Max speed of the predators.
- Food animals speed: Max speed of the animals that individuals eat.
- Food animals strength: How strong are the animals when fighting.

| Parameter             | Min | Max | Unit |
|-----------------------|-----|-----|------|
| Fruit tree height     | 2.5 | 3   | m    |
| Temperature           | -5  | 30  | º    |
| Predators speed       | 10  | 20  | km/h |
| Food animals speed    | 10  | 20  | km/h |
| Food animals strength | 1   | 10  |      |

**Algorithm**

The algorithm has 3 main phases:

1) Creation of the population and environment
    
    In this phase the initial N individuals are created, following the specified parameters. The environment is also created in this phase

2) Main phase

    This phase contains the main iteratation

    2.1 Selection
    
    In this subphase it will be checked if the individuals fit in their environment. The ones that fit will remain in the set for the next iteration, and the ones who doesn't will be eliminated.
    
    2.2 Reproduction
    
    In this subphase the fitting individuals will be paired randomly between them, and a new individual will be added for the next iteration, which will have an average of the parents parameters, multiplied by a random number which represents a random mutation.
    
    2.3 Natural Death
    
    Individuals that are too old cannot reproduce any more and cannot get into the next iteration. These individuals will be eliminated.
    
3) Finish

    3.1 Plot results

### Project Structure

- Application Architecture

![alt text][logo]

[logo]: file_url "Application Architecture"

## Using the application

### First of all
- I recommend creating a virtualenv for this project. After creating it, you should run:
```
~/GeneticAlgorithm$ pip install -r requirements.txt
```
Now all pip packages needed have been installed.

### Executing

- Executing the application

Now that the server is running, we can execute the application. This is done by typing this:
```
~/GeneticAlgorithm$ python src/genetic_algorithm.py
```
### Testing

Some tests will bee added to the 'tests' folder. To run them, simply type from the main project folder:
```
nosetests tests
```

## Decisions taken

I have chosen these specific parameters because I think they are useful to show how evolution works. The height/jump - tree height for instance was added because I wanted to check how the algorithm modified the individuals during iterations so that the remaining ones could access the environment resources.

I have decided to try to use asyncio not only because I wanted to improve my knowledge on the library, but also because I really needed a good parallel library in order to obtain a good performance in the filtering stage. The parallelization will be added in the near future.

I have decided not to use an API for a few reasons. The dataset used by the algorithm is intern, there are no external outputs, so to have an internal API only to encapsulate the processing code wouldn't make much sense. It would complicate the application without any strong reason.

I still don't know which database I will use. Probably MySQL or MongoDB. Right now everything is working in memory.