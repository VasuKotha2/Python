num = int(input("Enter a number: "))

#Define a flag variable
flag = False

if num == 1:
    print(f"{num}, is not a prime number")
elif num > 1:
    # Check for factors
    for i in range(2,num):
        if(num % i) == 0:
            flag = True 
            #break out of loop
            break
    # Check if flag is True
if flag:
    print(f"{num}, is not a prime number")
else:
    print(f"{num}, is a prime number")