
class Mouse:
    """ 
    Markus Kattner has a micro Penis                                                                #Wichtige Erkenntnis auf süß aber q:D
                                                                                                    #Das hat Markus nicht <===============8
    """
    
    def __init__(self, Hz = int, weight = int, shape = str, types = str, name = str):
        self.Hz = Hz
        self.weight = weight
        self.shape = shape
        self.types = types
        self.name = name
    @staticmethod
    def welcome():
        print("This is a Mouse class")
        
    def __str__(self) -> str:
        return f"This extraordinary Mouse has {self.Hz}Hz Pooling Rate, weighs {self.weight}g is made for the {self.shape} gripstyle and is {self.__types}"
    
    @property
    def types(self): 
        return self.__types

    @types.setter
    def types(self, value):
        if value not in ["wired", "wireless"]:
            raise ValueError("Type must be either 'wired' or 'wireless'.")
        self.__types = value
        
Op18k = Mouse(8000, 50.5, "claw", "wired", "Op18k")
print(Op18k)
