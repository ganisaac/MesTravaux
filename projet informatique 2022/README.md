# Projet-info-2A

# The aim of the project

The goal of this webservice is to create some data following some rules given by the user. 
The user first needs to run the API file in the code. Then he has access to different functions. He has to create some type first with a name and a chance of apparition. Next, the user will be able to create some modalities, each of them connected to an already existing type. Each modality has a value and a chance of apparition. Then this will enable the user to create some meta type, a list of already existing types. Finally the user will be able to create all the data he wants using the number of rows he wants to create and the meta type associated.

The user can also import a set of rules, by creating a Json file containing all the rules and use the API to import it.

Once the data are created he can either save them online or on his computer using different types of files. If the datas are saved online he can then manipulate them using the fonctions of the API.

Example:

The user wants to create 100 people in a dataframe with their Sexe and their birth country both with a probability of appearance of 100.

-First he creates the type Sexe with chance of apparition of 100%
-He also needs to create the type Birth_Country with chance of apparition of 100%
-Then he adds the modalities liked to type Sexe : 'M' and 'F' both with a 50% chance of apparition
-Next he adds the modalities liked to type Birth_Country : 'USA' 'UK' both with a 50% chance of apparition
-Then he creates the meta types 'people' with two types associated : 'Sexe' and 'Age'
-Finally he can create a dataframes with 100 people.

# How to install the application

First the user needs to download the following packages:
-uvicorn
-fastapi
-pandas
-unittest
-abc
-json
-xml
-random
-psycopg2_binary
-requests

Then if the user wants to use the data access online fonctionnalities he has to install Postgre on his computer.