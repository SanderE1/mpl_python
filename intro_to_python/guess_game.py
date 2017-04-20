# let's guess a number between 1 and 10

import random




print "Let's play a game!"
print "I'm thinking of a number between 1 and 10, can you guess it?"

secret_number = random.randint(1,10)

# print "the secret number is: {0}".format(secret_number)

guess = input("Enter a number: ")

print "You guessed: {}".format(guess)

if guess == secret_number:
    print "You win!"
else:
    print "You lose!  It was: {}".format(secret_number)

    
