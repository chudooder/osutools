import json
import csv

data = json.load(open('data/scores_aug.json'))
out = csv.writer(open('data/scores_aug.csv', 'w'))
best = csv.writer(open('data/scores_best.csv', 'w'))

bm_header = ['song_title', 'artist_name', 'creator_name', 'version', \
    'difficultyrating', 'diff_overall', 'diff_size', \
    'diff_approach', 'diff_drain', 'bpm', 'hit_length', \
    'total_length']

score_header = ['player', 'timestamp', 'mode', \
    'max_combo', 'perfect_combo', 'score', 'accuracy', 'grade', \
    'num_300', 'num_100', 'num_50', 'num_miss', 'num_geki', 'num_katu']
    
mods_header = ['key1', 'key2', 'key3', 'key4', 'key5', 'key6', 'key7', \
    'key8', 'key9', 'easy', 'half_time', 'no_fail', \
    'hard_rock', 'double_time', 'nightcore', 'hidden', \
    'sudden_death', 'perfect', 'fade_in', 'flashlight', \
    'cinema', 'no_video', 'random', 'spun_out', 'auto_pilot', \
    'coop', 'relax', 'autoplay', 'no_mod']
    
out.writerow(bm_header + score_header + mods_header)
best.writerow(bm_header + score_header + mods_header)

for beatmap in data['beatmaps']:
    first = True
    for score in beatmap['scores']:
        try:
            line = []
            for hd in bm_header:
                if hd == 'bm_max_combo':
                    line.append(beatmap['max_combo'])
                else:
                    line.append(beatmap[hd])
            for hd in score_header:
                line.append(score[hd])
            for hd in mods_header:
                line.append(score['mods'][hd])

            out.writerow(line)
            if first:
                best.writerow(line)
                first = False
        except KeyError, e:
            print 'Invalid score entry detected: no key \''+str(e)+'\''
