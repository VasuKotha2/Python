#Take input from user
a = input("Enter the value of the first variable (a): ")
b = input("Enter the value of the second variable (a): ")

print("Value of a before swap:", a)
print("Value of b before swap:", b)

a,b = b,a


print("\nValue of a after swap:", a)
print("Value of b after swap:", b)

