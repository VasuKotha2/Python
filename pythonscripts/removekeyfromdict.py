dict1 = {'a':1,'b':2,'c':3}
dict2 = {'x':24,'y':25}

key_to_move = input("Enter the key you want to move from dict1 to dict2:")
if key_to_move in dict1:
    dict2[key_to_move] = dict1.pop(key_to_move)
else:
    print("The provided key is not present in dict1")

print("Updated dict1", dict1)
print("Updated dict2", dict2)