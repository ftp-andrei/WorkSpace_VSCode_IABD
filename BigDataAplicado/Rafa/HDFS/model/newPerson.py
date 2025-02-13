class NewPerson:
    def __init__(self, name, age, email,info):
        self.name = name
        self.age = age
        self.email = email
        self.info= info
    def __str__(self) -> str:
        return f"name: {self.name}, age: {self.age} email: {self.email} info: {self.info}"
    def __repr__(self):
        return self.__str__()