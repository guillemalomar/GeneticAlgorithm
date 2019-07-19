# Genetic Algorithm

*    Title: Genetic Algorithm     
*    Author: Guillem Nicolau Alomar Sitjes      
*    Initial release: July 19th, 2019                     
*    Code version: 0.1                         
*    Availability: Public     

**Index**
* [Requirements](#requirements)
* [Documentation](#documentation)
    * [Explanation](#explanation)
    * [Project Structure](#project-structure)
* [Using the application](#using-the-application)
    * [Executing](#executing)
    * [Output](#output)
    * [Testing](#testing)
* [Decisions taken](#decisions-taken)

## Requirements

- Python +3.7
- asyncio 3.4.3
- matplotlib 3.1.1
- numpy 1.16.4
- pymongo 3.8.0 (optional)
- pytest 5.0.1

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

- Tree height: At which height are the tree fruits.
- Temperature: Minimum and maximum temperatures.
- Predators speed: Max speed of the predators.
- Food animals speed: Max speed of the animals that individuals eat.
- Food animals strength: How strong are the animals when fighting.

| Parameter             | Min | Max | Unit |
|-----------------------|-----|-----|------|
| Tree height           | 2.5 | 3   | m    |
| Temperature           | -5  | 30  | º    |
| Predators speed       | 10  | 20  | km/h |
| Food animals speed    | 10  | 20  | km/h |
| Food animals strength | 1   | 10  |      |

These min and max values are just a guide, not a fixed wall. But bear in mind that if you use values outside of these ranges the individuals will probably never fit in the environment, or take a lot of iterations to do it.

**Algorithm**

The algorithm has 3 main phases:

![alt text][logo]

[logo]: documentation/Diagram.png "Application Architecture"

### Project Structure

- Application Architecture

![alt text][logo2]

[logo2]: file_url "Application Architecture"

## Using the application

### First of all
- I recommend creating a virtualenv for this project. After creating it, you should run:
```
~/GeneticAlgorithm$ pip install -r requirements.txt
```
Now all pip packages needed have been installed.

You will also need to create your own _creds.py_ file. Use the _creds_dummy.py_ file as a layout guide.

### Executing

- Executing the application

Now that the server is running, we can execute the application. This is done by typing this:
```
~/GeneticAlgorithm$ python GeneticAlgorithm.py
```

#### Input parameters

You can define a custom environment by activating the custom flag, and passing the specific parameters that you want to test:

```
-> % python GeneticAlgorithm.py -h
usage: GeneticAlgorithm.py [-h] [-i ITERATIONS] [-db] [-c] [-n NAME]
                           [-th TREE_HEIGHT] [-t TEMPERATURE]
                           [-ps PREDATORS_SPEED] [-asp FOOD_ANIMALS_SPEED]
                           [-ast FOOD_ANIMALS_STRENGTH]

Genetic Algorithm

optional arguments:
  -h, --help            show this help message and exit
  -i ITERATIONS, --iterations ITERATIONS
                        Number of iterations to run.
  -db, --db             Use MongoDB.
  -c, --custom          Flag to activate custom mode, to use environment parameters given by the user.
  -n NAME, --name NAME  Name of the custom execution.
  -th TREE_HEIGHT, --tree_height TREE_HEIGHT
                        The environment trees height.
  -t TEMPERATURE, --temperature TEMPERATURE
                        The environment temperature.
  -ps PREDATORS_SPEED, --predators_speed PREDATORS_SPEED
                        The speed of the environment predators.
  -asp FOOD_ANIMALS_SPEED, --food_animals_speed FOOD_ANIMALS_SPEED
                        The speed of the animals that the individuals can hunt.
  -ast FOOD_ANIMALS_STRENGTH, --food_animals_strength FOOD_ANIMALS_STRENGTH
                        The strength of the animals that the individuals can hunt.
```

### Output

The execution results will be stored in the folder _output_. The following is an example of an output:

![alt text][logo3]

[logo3]: output/ExampleOutput.png "Example output"

### Testing

Some tests will bee added to the 'tests' folder. To run them, simply type from the main project folder:
```
nosetests tests
```

## Decisions taken

I have chosen these specific parameters because I think they are useful to show how evolution works. The height/jump - tree height for instance was added because I wanted to check how the algorithm modified the individuals during iterations so that the remaining ones could access the environment resources.

I have decided to try to use asyncio not only because I wanted to improve my knowledge on the library, but also because I really needed a good parallel library in order to obtain a good performance in the filtering stage.

I have decided not to use an API for a few reasons. The dataset used by the algorithm is intern, there are no external outputs, so to have an internal API only to encapsulate the processing code wouldn't make much sense. It would complicate the application without any strong reason.

I'm using MongoDB because the kind of data that I use fits really well (dictionaries) and with MongoDB Compass I can obtain some valuable information from resulting datasets. It would be interesting to, instead of simply storing and obtaining all individuals in every iteration, reading and writing individuals 1 by 1. This is not needed right now as the set fits in memory, but it could be a need if we want to use much bigger sets.

![alt text][logo4]

[logo4]: documentation/MongoCompass.png "MongoDB Compass screenshot"