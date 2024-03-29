import logging

class PsychometricIndex:
    """
    This index is used to catalog the psychometric profile
     of candidates and posting in a format which can be compared.
    """
    def __init__(self, psychometrics):
        self.extroversion = psychometrics.get('extroversion', 0)
        self.openness     = psychometrics.get('openness_to_experience', 0)
        self.agreeableness = psychometrics.get('agreeableness', 0)
        self.neuroticism  = psychometrics.get('neuroticism', 0)
        self.consciousness = psychometrics.get('conscientiousness', 0)
        self.strength = psychometrics.get('strength', 1)

class PsychometricsComparator:
    """
    This class is used to measure the distance between two PsychmetricIndex vectors
    """
    def __init__(self, candidate_psy_index, posting_psy_index, settings='similar'):
        self.candidate = candidate_psy_index
        self.posting = posting_psy_index
        self.settings = settings

    def run(self):
        if self.settings == 'similar':

            extro = abs(self.posting.extroversion - (self.candidate.extroversion))
            openn = abs(self.posting.openness - (self.candidate.openness))
            neuro = abs(self.posting.neuroticism - (self.candidate.neuroticism))
            agree = abs(self.posting.agreeableness - (self.candidate.agreeableness))
            consc = abs(self.posting.consciousness - (self.candidate.consciousness))

            result = {
                "extroversion" : extro,
                "openness_to_experience" : openn,
                "neuroticism" : neuro,
                "agreeableness" : agree,
                "conscientiousness" : consc
            }

            return result
