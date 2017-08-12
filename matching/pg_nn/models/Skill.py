from difflib import SequenceMatcher

class Skill:
    def __init__(self, skill):
        self.skill = skill

    def __str__(self):
        return self.skill

    def __eq__(self, other):
        return str.upper(self.skill) == str.upper(other.skill)


class SkillComparator:

    def __init__(self):
        self.candidate_skills = []
        self.posting_skills   = []

    def addCandidateSkills(self, skills):
        for skill in skills:
            if skill not in self.candidate_skills:
                self.candidate_skills.append(skill)


    def addPostingSkills(self, skills):
        for skill in skills:
            if skill not in self.posting_skills:
                self.posting_skills.append(skill)


    def run(self):

        self.match = map(
            #lambda skill: [SequenceMatcher(a=skill.skill, b=pskill.skill) for pskill in self.posting_skills],
            lambda skill : True in [skill == pskill for pskill in self.posting_skills],
            self.candidate_skills
        )
        items = list(self.match)
        matchRatio = 1 - sum(True == item for item in items)/len(items)
        return matchRatio

if __name__ == '__main__':

    c_skill_1 = Skill('Java')
    c_skill_2 = Skill('Python')
    c_skill_3 = Skill('Haskell')

    p_skill_1 = Skill('Java')
    p_skill_2 = Skill('Python')
    p_skill_3 = Skill('Matlab')

    comp = SkillComparator()
    comp.addCandidateSkills([c_skill_1, c_skill_2, c_skill_3])
    comp.addPostingSkills([p_skill_1, p_skill_2, p_skill_3])

    result = comp.run()

    print(result)

