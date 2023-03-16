import math
import json
import re
from src.NaturalLanguage.Corpus import Corpus
from src.NaturalLanguage.Intent import Intent
from src.NaturalLanguage.ProcessorResult import ProcessorResult

class Processor:
    def __init__(self):
        self.intents: dict[str, Intent] = {}
        self.__checkIntentExistence("none")

    def loadJson(self, jsonPath: str):
        allCorpus: list[Corpus] = []
        data = json.load(open(jsonPath, encoding='utf-8'))
        for corpus in data:
            allCorpus.append(Corpus(
                corpus['intent'],
                corpus['utterances'],
                corpus['answers'] if 'answers' in corpus else []
            ))
        self.loadCorpus(allCorpus)

    # Load
    # This function loads a corpus.
    def loadCorpus(self, corpus): #list[Corpus]
        for c in corpus:
            if c.utterances is not None:
                self.addDocuments(c.intent, c.utterances)
            if c.answers is not None:
                self.addAnswers(c.intent, c.answers)
                """
            if c.errors is not None:
                for code in c.errors:
                    self.addErrors(c.intent, code, c.errors[code])
                    """

    #region Documents

    # This function adds a way to call an action.
    def addDocument(self, intentName: str, utterance: str):
        self.addDocuments(intentName, [utterance])

    # This function adds ways to call an action.
    def addDocuments(self, intentName: str, utterances: str()):
        self.__checkIntentExistence(intentName)
        self.intents[intentName].addDocuments(utterances)

    #endregion

    #region Answers

    # This function adds a response to an action.
    def addAnswer(self, intentName: str, answer: str):
        self.addAnswers(intentName, [answer])

    # This function adds responses to an action.
    def addAnswers(self, intentName: str, answers: str()):
        self.__checkIntentExistence(intentName)
        self.intents[intentName].addAnswers(answers)

    #endregion
    
    # Errors
    def addErrors(self, intentName: str, errorsName: str, errors: str()):
        self.__checkIntentExistence(intentName)
        self.intents[intentName].addErrors(errorsName, errors)

    #region Actions

    # This function adds an action. This action will be triggered when a document is called.
    def addAction(self, intentName: str, _action):
        self.addActions(intentName, [_action])

    # This function adds actions. These actions will be triggered when a document is called.
    def addActions(self, intentName: str, actions):
        self.__checkIntentExistence(intentName)
        self.intents[intentName].addActions(actions)

    #endregion

    # Process
    # This function executes the intent that matches the customer's phrase.
    def process(self, utterance: str):
        splittedSay = utterance.split(" ")
        intent_name: str = None
        variables = []
        result: ProcessorResult = ProcessorResult(utterance)

        break_out_flag: bool = False
        for loop_intent_name in self.intents:
            for document in self.intents[loop_intent_name].documents:
                processResult = self.__process(document, splittedSay)
                if processResult != False:
                    intent_name = loop_intent_name
                    variables = processResult
                    break_out_flag = True
                    break
            if break_out_flag:
                break

        break_out_flag = False
        if intent_name == None:
            for loop_intent_name in self.intents:
                for document in self.intents[loop_intent_name].documents:
                    processResult = self.__process(document, splittedSay, False)
                    if processResult != False:
                        intent_name = loop_intent_name
                        variables = processResult
                        break_out_flag = True
                        break
                if break_out_flag:
                    break

        if intent_name == None:
            intent_name = "none"
        else:
            result.answers = self.intents[intent_name].answers
        result.intent = intent_name

        for variable in variables:
            if re.match(r'^-?\d+(?:\.\d+)$', variables[variable]) is not None:
                VALUE = float(variables[variable])
                if not math.isnan(VALUE):
                    variables[variable] = VALUE
                
        self.intents[intent_name].variables = variables
        result.variables = self.intents[intent_name].variables
        if result.answers != None:
            if len(result.answers) > 0:
                result.answer = self.intents[intent_name].answer()

        if len(self.intents[intent_name].actions) > 0:
            for action in self.intents[intent_name].actions:
                action(self.intents[intent_name], result)
                result.answer = None
                
        return result

    # This function checks if an intent exists, if not, it creates it.
    def __checkIntentExistence(self, intentName):
        if not intentName in self.intents:
            self.intents[intentName] = Intent(intentName)

    # This function is an essential loop of the "process" function.
    def __process(self, sentence: str, splitedSay: str(), asc: bool = True):
        sentence = sentence.lower()
        splittedSentense = sentence.split(" ")

        if asc == False:
            splittedSentense.reverse()
            splitedSay.reverse()

        variables = {}
        variables_position: int = 0
        variable_name: str = None
        ok: int = 0 # cette variablre représente le nombre de mots ou variables correspondantes à la phrase testée.

        break_out_flag: bool = False
        sentense: str
        for sentenseIndex, sentense in enumerate(splittedSentense):
            # SI LE MOT EST UNE VARIABLE
            if sentense[0] == "{" and sentense[-1] == "}":
                without_percent = sentense[1: len(sentense) - 1].split("|")
                variable_name = without_percent[0]
                max_words: int = 0
                if len(without_percent) > 1:
                    max_words = int(without_percent[1])
                    
                variables[variable_name] = []
                next_word = None
                if len(splittedSentense) > sentenseIndex + 1:
                    next_word = splittedSentense[sentenseIndex + 1]
                while len(splitedSay) > sentenseIndex + variables_position and splitedSay[sentenseIndex + variables_position] != next_word and splitedSay[sentenseIndex + variables_position] != None:
                    variables[variable_name].append(splitedSay[sentenseIndex + variables_position])
                    variables_position = variables_position + 1
                    if max_words > 0:
                        if len(variables[variable_name]) > max_words:
                            break_out_flag = True
                            break
                variables_position = variables_position - 1
                if asc == False:
                    variables[variable_name] = variables[variable_name].reverse()
                
                if variables[variable_name] is not None:
                    variables[variable_name] = " ".join(variables[variable_name])
                ok = ok + 1
            # SI LE MOT N'EST PAS UNE VARIABLE
            else:
                # SI LE MOT EN COUR EST EGAL AU MOT QUE L'ON A ENTENDU
                if len(splitedSay) > sentenseIndex + variables_position:
                    if sentense == splitedSay[sentenseIndex + variables_position]:
                        ok = ok + 1
                    else:
                        break
            if break_out_flag:
                    break

        if ok == len(splittedSentense):
            return variables
            
        return False