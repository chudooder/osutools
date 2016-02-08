import json
import csv
import operator

DIFF = 4
NO_MOD = 54
RANK = 19

def diffProgression():
    scores = csv.reader(open('data/scores_aug.csv'))
    header = next(scores)
    sortedlist = sorted(scores, key=operator.itemgetter(13))

    criteria = ['passed', 'SS', 'S', 'A']
    progressions = {}

    for criterion in criteria:
        print criterion
        progression = []
        difficulty = 0.0
        for score in sortedlist:
            if float(score[DIFF]) > difficulty and score[NO_MOD] == 'True' and passCriteria(criterion, score):
                progression.append(dict(zip(header, score)))
                difficulty = float(score[DIFF])
                print difficulty
        progressions[criterion] = progression

    json.dump(progressions, open('data/difficulty_progression.json', 'w'), indent=4)

def passCriteria(criterion, score):
    if criterion == 'passed':
        return True
    elif criterion == 'A':
        if score[RANK] == 'A' or score[RANK] == 'S' or score[RANK] == 'SS':
            return True
    elif criterion == 'S':
        if score[RANK] == 'S' or score[RANK] == 'SS':
            return True
    elif criterion == 'SS' and score[RANK] == 'SS':
        return True
    return False

if __name__ == '__main__':
    diffProgression()
