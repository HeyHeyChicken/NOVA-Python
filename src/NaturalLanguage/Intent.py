import math
import random

class Intent:
    def __init__(self, name: str):
        self.name: str = name
        self.documents: str() = []
        self.answers: str() = []
        self.errors = {}
        self.actions = []
        self.variables = {}

    def addDocuments(self, utterances: str()):
        self.documents = self.documents + utterances

    def addAnswers(self, answers: str()):
        self.answers = self.answers + answers

    def addActions(self, actions):
        self.actions = self.actions + actions
    
    def addErrors(self, errorsName: str, errors: str()):
        if not hasattr(self.errors, errorsName):
            self.errors[errorsName] = []
        self.errors[errorsName] = self.errors[errorsName] + errors
    
    def answer(self, answer = None):
        if answer is None:
            answer = self.answers[math.floor(random.random() * len(self.answers))]
        if answer is not None:
            for variable in self.variables:
                value: str = str(self.variables[variable])
                answer = answer.replace("%" + variable + "%", value)
            return answer

    def error(self, errorName: str):
        text = self.errors[errorName][math.floor(random.random() * len(self.errors[errorName]))];
        if text is not None:
            for variable in self.variables:
                text = text.replace("%" + variable + "%", self.variables[variable])
            return text