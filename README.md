# Genetic Algorithm

![alt text][logo5]

[logo5]: documentation/Evolution.png?style=centerme "Header"

*    Author: Guillem Alomar      
*    Current release: July 30th, 2019                     
*    Code version: 1.0                      
*    Availability: Public

## Index

* [Requirements](#requirements)
* [Documentation](#documentation)
    * [Explanation](#explanation)
    * [Algorithm](#algorithm)
    * [Application Structure](#application-structure)
* [Using the application](#using-the-application)
    * [First of all](#first-of-all)
    * [Executing the application](#executing-the-application)
    * [Output](#output)
    * [Testing](#testing)
* [Decisions taken](#decisions-taken)

## Requirements

Programming language

- Python +3.7

PIP packages

- asyncio 3.4.3
- matplotlib 3.1.1
- numpy 1.16.4
- pytest 5.0.1

Optional. If you want to use MongoDB, you will also need to install the following PIP package:

- pymongo 3.8.0

## Documentation

### Explanation

This project is an example of the most classic Genetic Algorithm problem. It will obtain 1 or more environments, will create a set of individuals with random parameters values within a specified range, and will see how these parameters change with the iterations by facing the individuals with each environment.

**Model**

The model is divided in two parts. The population model and the environment model.

###### Population Model

Each individual is summarized into a reduced set of parameters, which will be key for his/her future:

- Total reach: How height can the individual take fruits from trees.
- Speed: How fast can the individual run.
- Strength: How strong is the individual for fighting.
- Skin Thickness: How thick is the individual skin. The ideal thickness is not linearly proportional to the environment temperature. A low temperature will require a thick skin, but a high temperature will require it too.

| Parameter                          | Min  | Max | Units |
|------------------------------------|------|-----|-------|
| Total reach                        | 2.5  | 3   | m     |
| Speed                              | 10   | 20  | km/h  |
| Strength                           | 1    | 10  |       |
| Skin Thickness                     | 0.05 | 0.3 | mm    |

These are the default ranges, but can be modified in the settings/settings.py file.

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
| Temperature           | -10 | 50  | º    |
| Predators speed       | 10  | 20  | km/h |
| Food animals speed    | 10  | 20  | km/h |
| Food animals strength | 1   | 10  |      |

These min and max values are just a guide, not a fixed wall. But bear in mind that if you use values outside of these ranges the individuals will probably never fit in the environment, or take a lot of iterations to do it.

### Algorithm

The algorithm has 3 main phases:

![alt text][logo]

[logo]: documentation/Diagram.png "Genetic Algorithm"

### Application Structure

![alt text][logo2]

[logo2]: documentation/Structure.png "Application Structure"

## Using the application

### First of all

- I recommend creating a virtualenv for this project. After creating it, you should run:
```
~/GeneticAlgorithm$ pip install -r requirements.frozen
```
Now all pip packages needed have been installed.

You will also need to create your own _creds.py_ file. Use the _creds_dummy.py_ file as a layout guide.

### Executing the application

Now that the server is running, we can execute the application. This is done by typing this:
```
~/GeneticAlgorithm$ python GeneticAlgorithm.py
```

#### Input parameters

You can define a custom environment by activating the custom flag, and passing the specific parameters that you want to test:

```
-> % python GeneticAlgorithm.py -h
usage: GeneticAlgorithm.py [-h] [-a] [-db] [-c] [-n NAME] [-th TREE_HEIGHT]
                           [-t TEMPERATURE] [-ps PREDATORS_SPEED]
                           [-asp FOOD_ANIMALS_SPEED]
                           [-ast FOOD_ANIMALS_STRENGTH] [-i ITERATIONS]

Genetic Algorithm

optional arguments:
  -h, --help            show this help message and exit
  -a, --about           (flag) obtain a breve about the application
  -db, --database       (flag) activate MongoDB
  -c, --custom          (flag) activate custom mode, to use environment parameters given by the user
  -n NAME, --name NAME  (text) name of the custom execution
  -th TREE_HEIGHT, --tree_height TREE_HEIGHT
                        (float) the custom environment trees height
  -t TEMPERATURE, --temperature TEMPERATURE
                        (float) the custom environment temperature
  -ps PREDATORS_SPEED, --predators_speed PREDATORS_SPEED
                        (float) the custom environment predators speed
  -asp FOOD_ANIMALS_SPEED, --food_animals_speed FOOD_ANIMALS_SPEED
                        (float) the custom environment speed of the animals that the individuals can hunt
  -ast FOOD_ANIMALS_STRENGTH, --food_animals_strength FOOD_ANIMALS_STRENGTH
                        (float) the custom environment strength of the animals that the individuals can hunt
  -i ITERATIONS, --iterations ITERATIONS
                        (integer) number of iterations to run
```

### Output

The execution results will be stored in the folder _output_. The following is an example of an output:

![alt text][logo3]

[logo3]: output/ExampleOutput.png "Example output"

### Testing

Some tests have been added to the 'tests' folder. To run them, simply type from the main project folder:
```
nosetests tests
```

## Decisions taken

I have chosen these specific parameters because I think they are useful to show how evolution works. The height/jump - tree height for instance was added because I wanted to check how the algorithm modified the individuals during iterations so that the remaining ones could access the environment resources.

I have decided to use asyncio not only because I wanted to improve my knowledge on the library, but also because I really needed a good parallel library in order to obtain a good performance in both the filtering stage and the reproducing stage.

I'm using MongoDB because the kind of data that I use fits really well (dictionaries) and with MongoDB Compass I can obtain some valuable information from resulting datasets. It also allows to use much bigger datasets, as it's single read/write, so we don't need to have the full individuals dataset loaded in memory at any time. Bear in mind that the performance is much worse when this mode is activated.

I have decided not to use an API for a few reasons. The dataset used by the algorithm is intern, there are no external outputs, so to have an internal API only to encapsulate the processing code wouldn't make much sense. It would complicate the application without any strong reason.

![alt text][logo4]

[logo4]: documentation/MongoCompass.png "MongoDB Compass screenshot"
