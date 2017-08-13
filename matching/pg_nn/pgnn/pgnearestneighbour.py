from matching.pg_nn.models import Skill, Location, Interest, PsychometricAnalysis
from accounts.models import Candidate, CandidatePsychometrics, CandidateSkill, CandidateLocation, CandidateInterest
from employers.models import Team, TeamMember, EmployeePsychometrics, EmployerPsychometrics
from postings.models import Posting, PostingSkill, PostingLocation, PostingInterest, PostingPsychometrics
from matching.models import Match
import statistics
from concurrent.futures import ThreadPoolExecutor

class DistanceMeasurement:
    def __init__(self, posting_skills, posting_interests, post_location, posting_psychometrics, **kwargs):
        self.skills = kwargs.get('skills')
        self.interests = kwargs.get('interests')
        self.locations = kwargs.get('locations')
        self.psychometrics = kwargs.get('psychometrics')
        self.psychometrics_setting = kwargs.get('psychometrics_setting', 'similar')
        self.posting_skills = posting_skills
        self.posting_interests = posting_interests
        self.post_location = post_location
        self.posting_psychometrics = posting_psychometrics

        self.normalizeSkills()
        self.normalizeInterests()
        self.normalizeLocations()
        self.normalizePsychometrics()

    def normalizeSkills(self):
        self.n_skills = [Skill.Skill(skill) for skill in self.skills]
        self.n_pskills = [Skill.Skill(skill) for skill in self.posting_skills]
        comparator = Skill.SkillComparator()
        comparator.addCandidateSkills(self.n_skills)
        comparator.addPostingSkills(self.n_pskills)
        self.skillVal = comparator.run()
        print(self.skillVal)

    def normalizeInterests(self):
        self.n_interests = [Interest.Interest(interest) for interest in self.interests]
        self.n_pinterests = [Interest.Interest(interest) for interest in self.posting_interests]
        comparator = Interest.InterestComparator()
        comparator.addCandidateInterests(self.n_interests)
        comparator.addPostingInterests(self.n_pinterests)
        self.interestVal = comparator.run()

    def normalizeLocations(self):
        self.n_locations = [Location.Location(location[0], location[1]) for location in self.locations]
        self.n_plocation = Location.Location(self.post_location[0], self.post_location[1])
        comparator = Location.LocationComparator(self.n_plocation, self.n_locations)
        shortest_distance = comparator.getShortestDistance()
        self.distance = shortest_distance

    def normalizePsychometrics(self):
        self.candidate_psy = PsychometricAnalysis.PsychometricIndex(self.psychometrics)
        self.posting_psy = PsychometricAnalysis.PsychometricIndex(self.posting_psychometrics)
        comparator = PsychometricAnalysis.PsychometricsComparator(self.candidate_psy, self.posting_psy, self.psychometrics_setting)
        self.psychoVal = comparator.run()

    def getdistance(self):
        self.distance_matrix = {
            "skills" : self.skillVal,
            "interests" : self.interestVal,
            "locations" : self.distance,
            "psychometrics" : self.psychoVal,
            "total" : self.skillVal + self.interestVal + self.distance + self.psychoVal / 4
        }

        return self.distance_matrix


class JSort:
    def __init__(self, distances):
        self.distances = distances
        self.matches = []

    def sort(self):
        first = True
        for distance in self.distances:
            print(distance.total)
            if first:
                self.matches.append(distance)
                first = False
            else:
                for i in range(0, len(self.matches)):
                    inserted = False
                    if distance.total < self.matches[i].total:
                        self.matches.insert(i, distance)
                        inserted = True
                        break
                if inserted == False and len(self.matches) < 10:
                    self.matches.append(distance)

                if len(self.matches) > 10:
                    self.matches.pop()
                print(self.matches)
        return self.matches


class Distance:
    def __init__(self, candID, total, left=None, right=None):
        self.id = candID
        self.total = total

    def __str__(self):
        return "{}".format(self.total)

    def __repr__(self):
        return "{}".format(self.total)

class Matching:
    """
    This class will be the class called to create the matching environment used to compare a posting to all candidates,
    error checking will occur here and this will also produce the list of matches for each job posting
    """
    def __init__(self, posting):
        """Take the posting as a parameter then gather all candidates"""
        self.posting = posting
        self.candidates = Candidate.objects.all()

    def cleanCandidates(self):
        """produce a list of 'clean' candidates, that have all the required information to do matches"""
        self.clean_candidates = []
        for candidate in self.candidates:
            psychometrics = CandidatePsychometrics.objects.get(candidate=candidate)
            if (candidate.locations is not None and
                candidate.skills is not None and
                candidate.interests is not None and
                psychometrics.exists()):
                self.clean_candidates.append(candidate)


    def match(self, psycho_setting=None):
        """
        Perform the matching process by applying the distance measurement to all of the cleaned candidates
        :return: a list of the top matches
        """

        #get data formatted from objects
        posting_skills_objs = PostingSkill.objects.filter(posting=self.posting)
        posting_skills = [instance.skill.name for instance in posting_skills_objs]
        posting_interests_objs = PostingInterest.objects.filter(posting=self.posting)
        posting_interests = [instance.interest.name for instance in posting_interests_objs]
        posting_location_obj = PostingLocation.objects.get(posting=self.posting)
        posting_location = posting_location_obj.location
        posting_psychometrics = {
            "extroversion": None,
            "neuroticism": None,
            "openness_to_experience": None,
            "agreeableness": None,
            "conscientiousness": None
        }
        if psycho_setting == None:
            #get psychometrics from a range of team + employee and employer data
            #get any team assigned to the posting
            team = self.posting.team
            if team is not None and team is not "":
                team_members = set(TeamMember.objects.filter(team=team))
                for member in team_members:
                    member_psych = EmployeePsychometrics.objects.get(employee=member.employee)
                    if member_psych.exists():
                        posting_psychometrics = Matching.__addPsychometrics(posting_psychometrics, member_psych)

        employer = self.posting.employer
        employer_psych = EmployerPsychometrics.objects.get(employer=employer)
        if employer_psych.exists():
            posting_psychometrics = Matching.__addPsychometrics(posting_psychometrics, employer_psych)

        self.distances = {}
        for candidate in self.clean_candidates:
            #need to clean up this class
            #first get the needed information about each candidate
            skills = [instance.skill.name for instance in set(CandidateSkill.objects.filter(candidate=candidate))]
            interests = [instance.interest.name for instance in set(CandidateInterest.objects.filter(candidate=candidate))]
            locations = [(instance.location.lat, instance.location.lon) for instance in set(CandidateLocation.objects.filter(candidate=candidate))]
            psychometrics = CandidatePsychometrics.objects.get(candidate=candidate)
            clean_psychometrics = Matching.__cleanCandidatePsychometrics(psychometrics)
            with ThreadPoolExecutor() as pool:
                try:
                    self.distances[candidate.id] = pool.submit(DistanceMeasurement(posting_skills, posting_interests, (posting_location.lat, posting_location.lon), posting_psychometrics,
                                                                                skills=candidate.skills,
                                                                                interests=interests,
                                                                                locations=locations,
                                                                                psychometrics=clean_psychometrics))
                except Exception as exp:
                    raise exp

            matches = Matching.__sortResults()

            #create a model to represent the new matches
            for match in matches:
                #Get candidate
                candidate = Candidate.objects.get(id=match.id)
                new_match = Match.objects.create(candidate=candidate, posting=self.posting)

        #now that the distance measurements have all been applied, sort the list and produce the top ten
        #potentially use nested sorts.

    def __addPsychometrics(self, current, other):
        """Helper function that adds psychometric data to the current psychometric index to produce the pooled index"""
        current['extroversion'] = statistics.mean([current['extroversion'], other['extroversion']])
        current['neuroticism'] = statistics.mean([current['neuroticism'], other['neuroticism']])
        current['openness_to_experience'] = statistics.mean([current['openness_to_experience'], other['openness_to_experience']])
        current['agreeableness'] = statistics.mean([current['agreeableness'], other['agreeableness']])
        current['conscientiousness'] = statistics.mean([current['conscientiousness'], other['conscientiousness']])
        return current

    def __cleanCandidatePsychometrics(self, psychometrics):
        cleaned = {
            "extroversion": psychometrics.extroversion,
            "neuroticism": psychometrics.neuroticism,
            "openness_to_experience": psychometrics.openness_to_experience,
            "agreeableness": psychometrics.agreeableness,
            "conscientiousness": psychometrics.conscientiousness,
            "strength": psychometrics.strength
        }
        return cleaned

    def __sortResults(self):
        """
        Sorts the returned candidates into an ordered list the depict the candidates which are the closest in orientation to the posting
        :return: an ordered list of Distance objects, which contain the ID and the total score of the candidates whom have been matched
        """
        dists = [Distance(k, self.distances[k]['total']) for k in self.distances]
        sorter = JSort(dists)
        sorted_matches = sorter.sort()
        return sorted_matches


"""
if __name__ == '__main__':
    c_skill_1 = 'Java'
    c_skill_2 = 'Python'
    c_interest_1 = 'Salesforce'
    c_interest_2 = 'Management'
    norwich = Location.Location(52.6388845, 1.2273144)
    chelmsford = Location.Location(51.7258701, 0.4090747)
    norwich2 = Location.Location(52.6217286, 1.2793956)
    p_skill_1 = 'Java'
    p_skill_2 = 'Salesforce'
    p_interest_1 = 'Management'
    p_interest_2 = 'HTML'

    candidate_psycho = {
        'extroversion' : 3,
        'agreeableness' : 1,
        'openness' : -1,
        'consciousness' : 0,
        'neuroticism' : -2
    }

    posting_psycho = {
        'extroversion': 4,
        'agreeableness': 0,
        'openness': -3,
        'consciousness': 2,
        'neuroticism': 1
    }

    normalizedcandidate = DistanceMeasurement([p_skill_1, p_skill_2], [p_interest_1, p_interest_2], (52.6388845, 1.2273144),
                                              posting_psycho,
                                              skills=[c_skill_1, c_skill_2],
                                              interests=[c_interest_1, c_interest_2],
                                              locations=[(52.6217286, 1.2793956), (51.7258701, 0.4090747)],
                                              psychometrics=candidate_psycho)
    print(normalizedcandidate.getdistance())"""

