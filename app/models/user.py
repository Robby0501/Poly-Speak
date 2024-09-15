class User:
    def __init__(self, username, target_language, proficiency_level):
        self.username = username
        self.target_language = target_language
        self.proficiency_level = proficiency_level
        self.points = 0
        self.streak = 0
        self.badges = []
        self.vocabulary = set()
        self.mistakes = {}

    def add_points(self, points):
        self.points += points

    def increase_streak(self):
        self.streak += 1

    def add_badge(self, badge):
        self.badges.append(badge)

    def add_vocabulary(self, word):
        self.vocabulary.add(word)

    def add_mistake(self, word):
        if word in self.mistakes:
            self.mistakes[word] += 1
        else:
            self.mistakes[word] = 1