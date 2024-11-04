num = float(input("Enter a number: "))

#Check the number is negative or positive
if(num<0):
    print(f"{num} is negative")
elif(num>0):
    print(f"{num} is positive")
elif(num == 0):
    print(f"{num} is zero")
else:
    print("Please enter number")

