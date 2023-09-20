def i_input(prompt: str = "Eingabe:", type = str):
    while True:
        try:
            temp_input = type(input(f"{prompt} >"))
            return temp_input
        except ValueError:
            print("Typecast nicht möglich")

if __name__ == "__main__":
    ausgabe = i_input(prompt = "Gib einen Integer eun", type = int)
    print(ausgabe)