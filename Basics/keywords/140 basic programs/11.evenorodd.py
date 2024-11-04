#Check even or odd
try:
    num = float(input("Enter a number: "))
    if(num%2 == 0):
        print(f"{num} is even number")
    else:
        print(f"{num} is odd number")
except ValueError:
    print("Please enter value in integer format")


