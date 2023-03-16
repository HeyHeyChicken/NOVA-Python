class Corpus:
    def __init__(
            self, intent: str,
            utterances: str(),
            answers: str(),
            #errors: dict[str, str()] = {}
        ):
        self.intent: str = intent
        self.utterances: str() = utterances
        self.answers: str() = answers
        #self.errors: list[str] = errors