import string

class ER_parser:

    SYMBOLS = ['?','*','.','+','|']
    def __init__(self) -> None:
        self.definitions = dict()
        self.priority = []

    def put_concatenate_operator(self,text):
        text = text.replace(' ','')
        i = 0
        while True:
            if text[i] not in ['|','.','(']:
                if i >= len(text)-1:
                    break
                if text[i+1] not in (self.SYMBOLS+[')']):
                    text = text[:i+1]+'.'+text[i+1:]
                    
            i+=1
            if i >= len(text)-1:
                break
        return text                

    # Resolve [a-zAz] [0-9] type expression
    def solve_exp(self,text):
        start = text.find('[')
        end = text.find(']')
        expression = text[start+1:end]
        for i in range(len(expression)):
            if expression[i] == '-':
                if expression[i-1].islower():
                    if len(expression) >3:
                        lower_letters = list(string.ascii_lowercase)
                        upper_letters =  list(string.ascii_uppercase)
                        lower_list = lower_letters[lower_letters.index(expression[i-1]):lower_letters.index(expression[i+1])+1]
                        upper_list = upper_letters[upper_letters.index(expression[i+2]):upper_letters.index(expression[i+4])+1]
                        new_list = lower_list+upper_list
                    else:
                        letters = list(string.ascii_lowercase)
                        new_list = letters[letters.index(expression[i-1]):letters.index(expression[i+1])+1]
                elif expression[i-1].isupper():
                    letters = list(string.ascii_uppercase)
                    new_list = letters[letters.index(expression[i-1]):letters.index(expression[i+1])+1]
                else:
                    digits_list = list(string.digits)
                    new_list = digits_list[digits_list.index(expression[i-1]):digits_list.index(expression[i+1])+1]
                
                text = text.replace(f'[{expression}]',f'({"|".join(new_list)})')
                break       
        
        return text

    def parseEr_fromString(self,string):
        Lines = string.splitlines()
        for line in Lines:
            line = line.replace('\n','')
            if line != "":
                definition = line.split(":")
                definition[0] = definition[0].strip()
                definition[1] = definition[1].strip()
                self.priority.append(definition[0])
                while ('[') in definition[1]:
                    definition[1] = self.solve_exp(definition[1])
                
                self.definitions[definition[0]] = definition[1].strip()
        
        self.recursive_define()
        for key,value in self.definitions.items():
            self.definitions[key] = self.put_concatenate_operator(value.strip())



    def parseEr_fromFile(self,file):

        file = open(file,'r')
        Lines = file.readlines()
        file.close()

        for line in Lines:
            line = line.replace('\n','')
            if line != "":
                definition = line.split(":")
                definition[0] = definition[0].strip()
                definition[1] = definition[1].strip()
                self.priority.append(definition[0])
                while ('[') in definition[1]:
                    definition[1] = self.solve_exp(definition[1])
                
                self.definitions[definition[0]] = definition[1].strip()
        
        self.recursive_define()
        for key,value in self.definitions.items():
            self.definitions[key] = self.put_concatenate_operator(value.strip())

    #define 
    def recursive_define(self):
        has_defined = True        
        while (has_defined):
            has_defined = False
            for key,value in self.definitions.items():
                for key_2,value_2 in self.definitions.items():
                    if key in value_2:
                        self.definitions[key_2] = value_2.replace(key,value)


    def get_inner_parent(self,regex):
        pilha = []
        start = 0
        fim = len(regex)
        for i in range(len(regex)):
            if regex[i]=='(':
                start = i+1
            if regex[i]==')':
                fim = i
                break
        regex = regex[start:fim]
        return regex,start-1,fim+1
