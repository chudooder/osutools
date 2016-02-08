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

        valtype = FILTER_MAP[self.field]['type']
        if valtype == 'float':
            self.value = float(val)
        elif valtype == 'string':
            self.value = val

    def check(self, bm):
        try:
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

        except TypeError:
            print "Invalid type: " + self.toString()

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
    while cmd != 'done':
        i = 0
        for cname, hashes in collections['collections'].iteritems():
            print str(i) + ' - ' + cname + ': '
            i += 1
            for md5 in hashes:
                if md5 not in beatmaps:
                    print 'Could not find local beatmap: ' + md5
                bm = beatmaps[md5]
                print bm['song_title'] + ' ['+bm['version']+']'

        print '------------------'
        cmd = raw_input('>')
        
        if cmd == 'add':
            cname = raw_input('Collection name: ')
            filters = []
            fstring = ""
            while True:
                fstring = raw_input('Filter: ')
                if fstring == 'done':
                    break

                sp = fstring.split(' ', 3)
                filters.append(BeatmapFilter(sp[0], sp[1], sp[2]))

            collection = [bm for bm in filterBeatmaps(beatmaps, filters)]
            collections['collections'][cname] = collection

    writeCollectionDB(collections)
            
                

# returns a collection of beatmaps that match the
# given filter criteria
def filterBeatmaps(beatmaps, filters):
    filtered = {md5: b for md5, b in beatmaps.iteritems() if all([f.check(b) for f in filters])}
    return filtered

if __name__ == '__main__':
    # c = {'version': '20151212', 'collections': {}}
    # writeCollectionDB(c)

    osuDb = open('data/osu!.db')
    collectionsDb = open('data/collection.db')

    collections = dbparse.parseCollectionsDb(collectionsDb.read())
    beatmaps = dbparse.parseOsuDb(osuDb.read())

    acceptInput(collections, beatmaps)
