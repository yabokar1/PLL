from typing import List 
from presidio_analyzer import EntityRecognizer, RecognizerResult
from presidio_analyzer.nlp_engine import NlpArtifacts
from presidio_analyzer import AnalyzerEngine





class NumbersRecognizer(EntityRecognizer):

    expected_confidence_level = 0.7

    def load(self) -> None:
        pass

    def analyze(self, text: str, entities: List[str], nlp_artifacts: NlpArtifacts) -> List[RecognizerResult]:
        results = []

        # iterate over the spaCy tokens, and call `token.like_num`
        print(nlp_artifacts.tokens)
        print(self.expected_confidence_level)
        for token in nlp_artifacts.tokens:
            print(token)
            if token.like_num:
                result = RecognizerResult(
                    entity_type="NUMBER",
                    start=token.idx,
                    end=token.idx + len(token),
                    score=self.expected_confidence_level,
                )
                results.append(result)
        return results
    


new_numbers_recognizer = NumbersRecognizer(supported_entities=["NUMBER"])



text3 = "Roberto lives in Five 10 Broad st."
analyzer = AnalyzerEngine()
analyzer.registry.add_recognizer(new_numbers_recognizer)

numbers_results2 = analyzer.analyze(text=text3, language="en")
print("Results:")
print("\n".join([str(res) for res in numbers_results2]))