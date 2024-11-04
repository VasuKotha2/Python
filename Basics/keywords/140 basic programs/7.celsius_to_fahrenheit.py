try:
    celsius = float(input("Enter temperature in celsius: "))
    
    #Conversion formula Fahrenheit = (Celsius * 9/5) +32
    fahrenheit = (celsius * 9/5) +32
    print(f"{celsius} celsius is equal to {fahrenheit} degrees fahrenheit")
except ValueError:
    print("Please provide the celsius value in integer")



