def i_input(prompt: str = "Eingabe:", type = str):
    while True:
        try:
            temp_input = type(input(f"{prompt} >"))
            return temp_input
        except ValueError:
            print("Typecast nicht möglich")


testlist = ["Hallo", "Welt", "!"]

def intelligent_print(testlist):     
    for i in range(len(testlist)):
        print(f"{i}: {testlist[i]}")

if __name__ == "__main__":
    intelligent_print(testlist)






