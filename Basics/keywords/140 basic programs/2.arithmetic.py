
#Add function
def add(x,y):
    return x+y

#Subtract function
def subtract(x,y):
    return x-y

#Multiply function
def multiply(x,y):
    return x*y

#Division function
def divide(x,y):
    #Handle divide by zero exception
    if(y==0):
        return "Cannot divide by zero"
    return x/y

#main function
def main():
    print("Select the operation you want to perform: ")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")

    choice = input("Enter choice (1/2/3/4): ")
    #Handle invalid choice exception
    if choice in('1','2','3','4'):
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            return
        if choice == '1':
            print("Result: ", add(num1,num2))
        if choice == '2':
            print("Result: ", subtract(num1,num2))
        if choice == '3':
            print("Result: ", multiply(num1,num2))
        if choice == '4':
            print("Result: ", divide(num1,num2))
    else:
        print("Invalid choice. Please select the correct choice")

#Checks if the script is run directly or not. If it is run directly then call main function
if __name__ == "__main__":
    main()

