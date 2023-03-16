class ProcessorResult:
    def __init__(self, utterance: str):
        self.intent: str = None
        self.utterance: str = utterance
        self.variables: str() = []
        self.answers: str() = []
        self.answer: str = None