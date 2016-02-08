import json
import dbparse
from struct import pack

FILTER_MAP = json.load(open('filters.json'))

def getULEBString(string):
    uleb = pack('b', 0x0b)
    val = len(string)
    # pack length of string
    while val != 0:
        # get low order 7 bits and shift
        byte = (val & 0x7F)
        val >>= 7
        # more values to come: set high order bit
        if val != 0:
            byte |= 0x80

        uleb += pack('B', byte)

    uleb += pack(str(len(string))+'s', str(string))

    return uleb
        

class BeatmapFilter:
    def __init__(self, fld, op, val):
        self.field = fld
        self.operator = op
        self.value = val

    def check(self, bm):
        bmval = bm[FILTER_MAP[self.field]['key']]
        valtype = FILTER_MAP[self.field]['type']

        if valtype == 'float':
            bmval = float(bmval)

        if self.operator == '=' or self.operator == '==':
            return bmval == self.value
        elif self.operator == '<':
            return bmval < self.value
        elif self.operator == '<=':
            return bmval <= self.value
        elif self.operator == '>':
            return bmval > self.value
        elif self.operator == '>=':
            return bmval >= self.value
        elif self.operator == '!=':
            return bmval != self.value
        elif self.operator == '?':
            return self.value in bmval
        elif self.operator == '!?':
            return self.value not in bmval

    def toString(self):
        return self.field + ' ' + self.operator + ' ' + str(self.value)

def writeCollectionDB(collections):
    out = open('data/collection.db', 'wb')
    out.write(pack('I', int(collections['version'])))
    out.write(pack('I', len(collections['collections'])))

    for cname, hashes in collections['collections'].iteritems():
        out.write(getULEBString(cname))
        out.write(pack('I', len(hashes)))
        for md5 in hashes:
            out.write(getULEBString(md5))

    out.close()
    


def acceptInput(collections, bmJson):
    # print out list of current collections
    cmd = ''
    beatmaps = bmJson['beatmaps']
    done = False
    while not done:
        cnames = collections['collections'].keys()

        print '------------------'
        for i, cname in enumerate(cnames):
            nummaps = len(collections['collections'][cname])
            print '{} - {:25}: {} beatmaps'.format( \
                str(i), cname, nummaps)
        print '------------------'

        cmd = raw_input('> ')
        
        if cmd == 'add':
            addCollection(cmd, collections, beatmaps)

        if cmd.startswith('remove'):
            removeCollection(cmd, collections, beatmaps)

        elif cmd.startswith('list'):
            listCollection(cmd, collections, beatmaps)

        elif cmd.startswith('save'):
            writeCollectionDB(collections)

        elif cmd.startswith('quit'):
            res = raw_input('Save? Y/N: ')
            if res.upper() == 'Y':
                writeCollectionDB(collections)
            elif res.upper() == 'N':
                done = True

            
def addCollection(cmd, collections, beatmaps):
    print('Collection name:')
    cname = raw_input('> ')
    filters = []
    fstring = ""
    while True:
        print('Filter:')
        fstring = raw_input('> ')
        if fstring == 'done':
            break

        sp = fstring.split(' ', 3)
        if len(sp) < 3:
            print 'Usage: <filter> [=, ==, !=, <, >, <=, >=, ?, !?] <val>'
            print 'Or type \'done\' to exit'
            continue

        field = sp[0].upper()
        if field not in FILTER_MAP:
            print 'Error: not a valid filter'
            continue

        oper = sp[1]
        if oper not in ['=', '==', '!=', '<', '>', '<=', '>=', '?', '!?']:
            print 'Error: Invalid operator'
            continue

        valtype = FILTER_MAP[field]['type']
        val = sp[2]
        if valtype == 'float':
            try:
                val = float(sp[2])
            except ValueError:
                print 'Error: value should be a float'
                continue


        filters.append(BeatmapFilter(field, oper, val))

    collection = [bm for bm in filterBeatmaps(beatmaps, filters)]
    collections['collections'][cname] = collection

def removeCollection(cmd, collections, beatmaps):
    try:
        index = int(cmd.split(' ')[1])
    except ValueError:
        print "Usage: remove <index>"
        return

    cnames = collections['collections'].keys()
    if index not in range(len(cnames)):
        print "Index out of range: " + str(index)
        return

    del collections['collections'][cnames[index]]

def listCollection(cmd, collections, beatmaps):
    try:
        index = int(cmd.split(' ')[1])
    except ValueError:
        print "Usage: list <index>"
        return

    cnames = collections['collections'].keys()
    if index not in range(len(cnames)):
        print "Index out of range: " + str(index)
        return

    for md5 in collections['collections'][cnames[index]]:
        if md5 not in beatmaps:
            print 'Could not find local beatmap: ' + md5
        else:
            bm = beatmaps[md5]
            print bm['song_title'] + ' ['+bm['version']+']'

    print '* Press ENTER to continue...'
    raw_input()

# returns a collection of beatmaps that match the
# given filter criteria
def filterBeatmaps(beatmaps, filters):
    filtered = {md5: b for md5, b in beatmaps.iteritems() if all([f.check(b) for f in filters])}
    return filtered

if __name__ == '__main__':
    # c = {'version': '20151212', 'collections': {}}
    # writeCollectionDB(c)

    osuDb = open('data/osu!.db', 'rb')
    collectionsDb = open('data/collection.db', 'rb')

    collections = dbparse.parseCollectionsDb(collectionsDb.read())
    beatmaps = dbparse.parseOsuDb(osuDb.read())

    acceptInput(collections, beatmaps)
