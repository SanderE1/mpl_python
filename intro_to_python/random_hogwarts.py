# Random Hogwarts House Generator

import random

FirstPart = ["Gryphin", "Slyth", "Raven", "Huffle", "Puffy", "Smell", "Shark"]
SecondPart = ["dor", "erin", "claw", "puff", "gor", "grin", "doop"]

f = random.randint(0,len(FirstPart)-1)
s = random.randint(0,len(SecondPart)-1)

randomName = FirstPart[f] + SecondPart[s]
print "Your random Hogwarts House is: {}!!!!".format(randomName)

