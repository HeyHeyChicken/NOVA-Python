class Corpus:
    def __init__(
            self, intent: str,
            utterances: str(),
            answers: str(),
            #errors: dict[str, str()] = {}
        ):
        self.intent: str = intent
        self.utterances: list[str] = utterances
        self.answers: list[str] = answers
        #self.errors: list[str] = errors