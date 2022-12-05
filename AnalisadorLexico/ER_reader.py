import os

class ER_parser:

    def __init__(self) -> None:
        self.definitions = dict()

    def parseEr(self,file):

        file = open(file,'r')
        Lines = file.readlines()
        file.close()

        for line in Lines:
            line = line[:-1]
            definition = line.split(":")
            #
            #for key in self.definitions:
            #    if key in definition[1]:
            #        definition[1] = definition[1].replace(key,self.definitions[key])
            self.definitions[definition[0]] = definition[1]




if __name__ == '__main__':
    obj = ER_parser()

    obj.parseEr(os.path.join('ER','er_1.txt'))
    print(obj.definitions)