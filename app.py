class Koala:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Hi I'm {self.name} from koala")


my_koala = Koala("Koko", 3)


my_koala.greet()
