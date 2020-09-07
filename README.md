# Genetic Algorithm

![alt text][logo5]

[logo5]: documentation/Evolution.png?style=centerme "Header"

*    Author: Guillem Alomar      
*    Current release: September 7th, 2020                    
*    Code version: 1.1                      
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
    * [Using your database](#using-your-database)
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

Optional. If you want to use MongoDB or MySQL, you will also need to install the following PIP packages:
- pymongo 3.8.0
- mysql-connector-python 8.0.14
- mysql-connector-python-rf 2.2.2

## Documentation

### Explanation

This project is an example of the most classic Genetic Algorithm problem, the evolution of individuals when faced against an environment. In computer science and operations research, a genetic algorithm (GA) is a metaheuristic inspired by the process of natural selection that belongs to the larger class of evolutionary algorithms (EA). Genetic algorithms are commonly used to generate high-quality solutions to optimization and search problems by relying on bio-inspired operators such as mutation, crossover and selection. John Holland introduced genetic algorithms in 1960 based on the concept of Darwin’s theory of evolution; afterwards, his student David E. Goldberg extended GA in 1989.
To know more, you can check the [Wikipedia page](https://en.wikipedia.org/wiki/Genetic_algorithm).

This application will obtain 1 or more environments, create a set of individuals with random parameters values within a specified range, and show how these parameters change with the iterations by facing the individuals against each environment.

It also has the option of defining your own set of values for both the individuals and the environment, and to give weights to each value.

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
~/GeneticAlgorithm$ pip install -r requirements.txt
```
Now all pip packages needed have been installed.

You will also need to create your own _creds.py_ file. Use the _creds_dummy.py_ file as a layout guide.

### Executing the application

We can execute the application with the following command:
```
~/GeneticAlgorithm$ python GeneticAlgorithm.py
```

#### Input parameters

You can define a custom environment by activating the custom flag:

```
-> % python GeneticAlgorithm.py -h
usage: GeneticAlgorithm.py [-h] [-a] [-db DATABASE] [-g] [-n NAME] [-p PARAMS]
                           [-m] [-e] [-pop POPULATION] [-i ITERATIONS]
                           [-mf MUTATIONFACTOR]

Genetic Algorithm

optional arguments:
  -h, --help            show this help message and exit
  -a, --about           (flag) obtain a breve about the application
  -db DATABASE, --database DATABASE
                        (string) activate database [MongoDB, MySQL]
  -g, --generic         (flag) activate generic mode, to use the parameters in the settings/generic_model.py file
  -n NAME, --name NAME  (text) name of the single execution
  -p PARAMS, --params PARAMS
                        (text) comma separated parameters for the single execution
  -m, --multiple        (flag) activate multiple mode, to execute many environments at once
  -e, --elitist         (flag) pair individuals with other with a similar fitness value, instead of randomly
  -pop POPULATION, --population POPULATION
                        (int) initial population size
  -i ITERATIONS, --iterations ITERATIONS
                        (integer) number of iterations to run
  -mf MUTATIONFACTOR, --mutationfactor MUTATIONFACTOR
                        (float) mutation factor
```

You can also do the following by modifying the following files:

_settings/settings.py_:
- change the default initial population size
- change the default maximum number of iterations
- change the default mutation factor
- change the default elitism

_settings/generic_model.py_:
- change existing environments or create new ones
- change the weights of the individuals parameters
- change the default individuals parameter ranges

_settings/human_model.py_:
- change existing environments or create new ones
- change the weights of the individuals parameters
- change the default individuals parameter ranges

### Using your Database

This application has the option of using your MongoDB or MySQL database.

In order to do so, you will need to create a _creds.py_ file in your main folder (you can use the _creds_dummy.py_ file as a guide) and add your database credentials. Also don't forget to specify the database that you want to use by adding the input parameter when running the application:

```
% python GeneticAlgorithm.py -db [mongodb|mysql]
```

### Output

When executing, the terminal will show some results similar to these:

```
#################### NEW EXECUTION ####################
################################# Executing with the following parameters:
################################# Environment name: Generic Execution
################################# -value1: 3
################################# -value2: 4
################################# -value3: 5
################################# -value4: 6
################################# -value5: 7
Worst individual in iteration 5: {'_id': 884, 'age': 7, 'value1': 4.613, 'value2': 4.094, 'value3': 4.4, 'value4': 3.904, 'value5': 4.882, 'value': 0.477702380952381}
Best individual in iteration 5:  {'_id': 359, 'age': 8, 'value1': 3.014, 'value2': 4.291, 'value3': 5.152, 'value4': 7.018, 'value5': 4.748, 'value': 0.9839142857142857}
Worst individual in iteration 10: {'_id': 2, 'age': 13, 'value1': 3.296, 'value2': 4.193, 'value3': 3.93, 'value4': 4.739, 'value5': 4.462, 'value': 0.9499630952380953}
Best individual in iteration 10:  {'_id': 1115, 'age': 14, 'value1': 3.205, 'value2': 4.108, 'value3': 4.95, 'value4': 5.226, 'value5': 5.137, 'value': 0.9792428571428571}
Worst individual in iteration 15: {'_id': 420, 'age': 16, 'value1': 3.021, 'value2': 4.141, 'value3': 4.581, 'value4': 4.56, 'value5': 5.303, 'value': 0.9674985714285715}
Best individual in iteration 15:  {'_id': 912, 'age': 17, 'value1': 3.186, 'value2': 4.173, 'value3': 5.024, 'value4': 5.435, 'value5': 4.877, 'value': 0.9801273809523809}
Worst individual in iteration 20: {'_id': 31, 'age': 23, 'value1': 3.235, 'value2': 4.204, 'value3': 5.241, 'value4': 4.813, 'value5': 4.942, 'value': 0.9754083333333333}
Best individual in iteration 20:  {'_id': 1140, 'age': 24, 'value1': 3.193, 'value2': 4.273, 'value3': 4.992, 'value4': 5.451, 'value5': 5.264, 'value': 0.9828650000000001}
Worst individual in iteration 25: {'_id': 571, 'age': 25, 'value1': 3.203, 'value2': 4.276, 'value3': 4.85, 'value4': 5.345, 'value5': 5.441, 'value': 0.9804059523809524}
Best individual in iteration 25:  {'_id': 763, 'age': 26, 'value1': 3.286, 'value2': 4.392, 'value3': 5.723, 'value4': 5.416, 'value5': 5.633, 'value': 0.9853690476190476}
Worst individual in iteration 30: {'_id': 475, 'age': 30, 'value1': 3.353, 'value2': 4.301, 'value3': 5.444, 'value4': 5.364, 'value5': 5.631, 'value': 0.9849214285714285}
Best individual in iteration 30:  {'_id': 1070, 'age': 33, 'value1': 3.368, 'value2': 4.201, 'value3': 5.053, 'value4': 5.978, 'value5': 5.707, 'value': 0.9905809523809523}
Worst individual in iteration 35: {'_id': 785, 'age': 36, 'value1': 3.207, 'value2': 4.423, 'value3': 5.249, 'value4': 5.784, 'value5': 5.836, 'value': 0.9898857142857144}
Best individual in iteration 35:  {'_id': 1057, 'age': 38, 'value1': 3.005, 'value2': 4.095, 'value3': 5.595, 'value4': 6.04, 'value5': 6.237, 'value': 0.99455}
Worst individual in iteration 40: {'_id': 532, 'age': 43, 'value1': 3.396, 'value2': 4.12, 'value3': 5.473, 'value4': 6.075, 'value5': 6.119, 'value': 0.9937071428571429}
Best individual in iteration 40:  {'_id': 805, 'age': 41, 'value1': 3.199, 'value2': 4.289, 'value3': 5.344, 'value4': 6.251, 'value5': 6.664, 'value': 0.9976}
Worst individual in iteration 45: {'_id': 421, 'age': 48, 'value1': 3.336, 'value2': 4.263, 'value3': 5.365, 'value4': 6.77, 'value5': 6.65, 'value': 0.9975}
Best individual in iteration 45:  {'_id': 1090, 'age': 49, 'value1': 3.187, 'value2': 4.077, 'value3': 5.623, 'value4': 6.021, 'value5': 7.064, 'value': 1.0}
Worst individual in iteration 50: {'_id': 549, 'age': 51, 'value1': 3.115, 'value2': 4.204, 'value3': 5.117, 'value4': 6.123, 'value5': 7.144, 'value': 1.0}
Best individual in iteration 50:  {'_id': 1080, 'age': 54, 'value1': 3.339, 'value2': 4.255, 'value3': 5.339, 'value4': 6.212, 'value5': 7.291, 'value': 1.0}
Worst individual in iteration 55: {'_id': 883, 'age': 57, 'value1': 3.18, 'value2': 4.217, 'value3': 5.472, 'value4': 6.019, 'value5': 7.31, 'value': 1.0}
Best individual in iteration 55:  {'_id': 1080, 'age': 59, 'value1': 3.455, 'value2': 4.324, 'value3': 5.162, 'value4': 6.541, 'value5': 7.019, 'value': 1.0}
Total number of iterations: 57
```

Here you can see the worst valued and best valued individuals every 5 iterations.

The average execution results will be stored in the folder _output_. The following is an example of an output:

![alt text][logo3]

[logo3]: output/ExampleOutput.png "Example output"

You can also find some logs in the file _genetic_algorithm.log_, which will have data from your last execution

### Testing

Some tests have been added to the 'tests' folder. To run them, simply type from the main project folder:
```
nosetests tests
```

## Decisions taken

I have chosen these specific parameters because I think they are useful to show how evolution works. The height/jump - tree height for instance was added because I wanted to check how the algorithm modified the individuals during iterations so that the remaining ones could access the environment resources.

I have decided to use asyncio not only because I wanted to improve my knowledge on the library, but also because I really needed a good parallel library in order to obtain a good performance in both the filtering stage and the reproducing stage.

I'm using MongoDB because the kind of data that I use fits really well (dictionaries) and with MongoDB Compass I can obtain some valuable information from resulting datasets. It also allows to use much bigger datasets, as it's single read/write, so we don't need to have the full individuals dataset loaded in memory at any time. Bear in mind that the performance is much worse when this mode is activated.
I have also added support for MySQL because it's one of the most used DDBBs and I thought it could be useful.

I have decided not to use an API for a few reasons. The dataset used by the algorithm is intern, there are no external outputs, so to have an internal API only to encapsulate the processing code wouldn't make much sense. It would complicate the application without any strong reason.

![alt text][logo4]

[logo4]: documentation/MongoCompass.png "MongoDB Compass screenshot"
