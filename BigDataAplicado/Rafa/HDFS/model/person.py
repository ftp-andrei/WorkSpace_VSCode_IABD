from model.newPerson import NewPerson
import json
class Person(NewPerson):
    def __init__(self, name, age, email,info,_id=None):
        super().__init__(name, age, email,info)
        self._id=_id
    def __str__(self) -> str:
        return f"id: {self._id}, {super().__str__()}"
    def __repr__(self):
        return self.__str__()
    
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)