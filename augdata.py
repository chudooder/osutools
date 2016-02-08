import dbparse
import json

scoredb = dbparse.parseScoresDb(open('data/scores.db').read())
beatmapdb = dbparse.parseOsuDb(open('data/osu!.db').read())

for beatmap in scoredb['beatmaps']:
    if beatmap['file_md5'] not in beatmapdb['beatmaps']:
        print beatmap['file_md5'] + ' not in local beatmaps'
        continue
    db = beatmapdb['beatmaps'][beatmap['file_md5']]
    for key in db:
        beatmap[key] = db[key]

json.dump(scoredb, open('data/scores_aug.json', 'w'), indent=4)
