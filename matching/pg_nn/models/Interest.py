class Interest:

    def __init__(self, interest):
        self.interest = interest

    def __str__(self):
        return self.interest

    def __eq__(self, other):
        return str.upper(self.interest) == str.upper(other.interest)


class InterestComparator:

    def __init__(self):
        self.candidate_interests = []
        self.posting_interests   = []

    def addCandidateInterests(self, interests):
        for interest in interests:
            if interest not in self.candidate_interests:
                self.candidate_interests.append(interest)

    def addPostingInterests(self, interests):
        for interest in interests:
            if interest not in self.posting_interests:
                self.posting_interests.append(interest)


    def run(self):

        self.match = map(
            lambda interest : True in [interest == pinterest for pinterest in self.posting_interests],
            self.candidate_interests
        )
        items = list(self.match)
        matchRatio = 1 - sum(True == item for item in items)/len(items)
        return matchRatio


if __name__ == '__main__':

    c_int_1 = Interest('Cooking')
    c_int_2 = Interest('Reading')
    c_int_3 = Interest('Cloud Computing')

    p_int_1 = Interest('Design')
    p_int_2 = Interest('Reading')
    p_int_3 = Interest('Engineering')

    comp = InterestComparator()
    comp.addCandidateInterests([c_int_1, c_int_2, c_int_3])
    comp.addPostingInterests([p_int_1, p_int_2, p_int_3])

    result = comp.run()
    print(result)
