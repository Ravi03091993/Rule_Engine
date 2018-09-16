import json
import os.path

from .models import Mymodel

class rule_provider:
    signal = ["Select signal Name"]
    def __init__(self):
        self.path = None

    def relative_path_to_file(self):
        my_path = os.path.abspath(os.path.dirname(__file__))
        self.path = os.path.join(my_path, "../../Background_process/rule.json")
    
    def add(self, signal, value, value_type):
        self.relative_path_to_file()
        with open(self.path, 'r') as f:
            json_data = json.load(f) # deserialises it
        json_data[signal] = [value, value_type]
        with open(self.path, 'w') as f:
            json.dump(json_data,f)
            rule_provider.signal.append(signal)
        

    @classmethod
    def retrieve(self):
        l = [(sig, sig) for  sig in rule_provider.signal]
        l.append(("Input Signal Name","Other"))
        return l
        
        return book.keys()


class display_content:
    def __init__(self):
        self.my_path = os.path.abspath(os.path.dirname(__file__))

    def read_regex_invalidated_file(self):
        self.path = os.path.join(self.my_path, "../../Background_process/regex_validation_error")
        l = []
        with open(self.path, 'r') as f:
            for line in (f.readlines()[-5:]):
                l.append(line[:-2])
        return l
    

    def read_rule_invalidated_file(self):
        self.path = os.path.join(self.my_path, "../../Background_process/rule_validation_error")
        l = []
        with open(self.path, 'r') as f:
            for line in (f.readlines()[-5:]):
                l.append(line[:-2])
        return l