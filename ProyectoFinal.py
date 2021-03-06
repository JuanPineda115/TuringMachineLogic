# Logica Matematica
# Proyecto 5 Maquina de Turing
# Universidad del Valle de Guatemala
# Diego Alvarez 19497
# Martin España 19258
# Alejandra Gudiel 19232
# Maria Jose Morales 190145
# Juan Pablo Pineda 19087

from prettytable import PrettyTable
import json

class Tape(object):
    blank_symbol = "-"

    def __init__(self, tape_string):
        self.tape = dict((enumerate(tape_string)))

    def __str__(self):
        return "".join(self.tape[i] for i in self.tape)

    def __getitem__(self, index):
        return self.tape[index] if index in self.tape else Tape.blank_symbol

    def __setitem__(self, pos, char):
        self.tape[pos] = char


class TuringMachine(object):
    def __init__(self, filename):
        self.Head = 0
        self.loadTape(filename)

    @property
    def thisTape(self):
        return str(self.theTape)

    @property
    def isFinalnextStep(self):
        return self.currentState in self.final_states

    def loadTape(self, filename):
        configutations = self.parseJSON(filename)
        self.States = configutations["q"]
        self.currentState = configutations["initial_state"]
        self.transFunc = configutations["transition_function"]
        self.final_states = configutations["final_states"]
        self.theTape = Tape(configutations["tape"])

    def nextStep(self):
        thisBit = self.theTape[self.Head]
        transIndex = "{},{}".format(self.currentState, thisBit)
        if transIndex in self.transFunc \
            and self.currentState in self.States:            
            transition = self.transFunc[transIndex]
            self.currentState = transition["state"]
            self.theTape[self.Head] = transition["value"]
            if transition["direc"] == "R":
                self.Head += 1
            elif transition["direc"] == "L":
                self.Head -= 1

    def start(self):
        # theTable = PrettyTable(["Paso", "Config"])
        cont = 0
        with open('result.txt', 'w') as output_file:
            while True:
                currSetting = ""
                for i in range(len(self.thisTape)):
                    if (self.Head == i):
                        currSetting += self.currentState
                    currSetting += self.thisTape[i]
                    if (self.Head == len(self.thisTape) \
                        and (i + 1) == len(self.thisTape)):
                        currSetting += self.currentState
                print(cont, "   ", currSetting)
                # theTable.add_row([cont, currSetting])
                output_file.write(currSetting + "\n")
                if self.isFinalnextStep: return print("cantidad de pasos: ", cont-1)
                self.nextStep()
                cont += 1

    def parseJSON(self, filename):
        with open(filename) as my_json:
            return json.load(my_json)

flag = True
while flag:
    print("---------- Maquina de Turing ----------")
    option = input("1. Ejemplo aleatorio \n2. Ejemplo de aceptacion \n3. Ejemplo de Rechazo \n4. Ejemplo Infinito \n5. Salir \n")
    if (option == '1'):
        turing = TuringMachine("JSON/ejemplo.json")
        turing.start()
    elif (option == '2'):
        turing = TuringMachine("JSON/aceptacion.json")
        turing.start()
    elif (option == '3'):
        turing = TuringMachine("JSON/rechazo.json")
        turing.start()
    elif (option == '4'):
        turing = TuringMachine("JSON/infinito.json")
        turing.start()
    elif (option == '5'):
        flag = False
    else:
        print("la opcion no es valida, intente de nuevo \n")

