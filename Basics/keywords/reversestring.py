
def ReverseString(element):
    ReversedString = ""
    for n in element:
        ReversedString = n + ReversedString
    return ReversedString

String1 = "Hey, there!"
FinalString = ReverseString(String1)
print(FinalString)