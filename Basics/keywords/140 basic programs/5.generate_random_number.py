#Take start and end inputs from user
import random
start = int(input("Enter the start number to generate random number: "))
end = int(input("Enter the end number to generate random number: "))

#Generate random number between start and end numbers
rand_num = random.randint(start,end)

#Print a random number that was generated
print(f"Random number between {start} and {end} is: {rand_num}")