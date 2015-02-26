from difflib import SequenceMatcher
def s(s1, s2):
    if s1 is None:
        raise TypeError("s1 is None")
    if s2 is None:
        raise TypeError("s2 is None")
    if len(s1) == 0 or len(s2) == 0 or len(s1) > len(s2):
        return
    shorter = s1
    longer = s2
    m = SequenceMatcher(None, shorter, longer)
    blocks = m.get_matching_blocks()
    #print blocks
    scores = []
    for block in blocks:
        long_start = block[1] - block[0] if (block[1] - block[0]) > 0 else 0
        long_end = long_start + len(shorter)
        long_substr = longer[long_start:long_end]
        # print long_substr
        m2 = SequenceMatcher(None, shorter, long_substr)
        if m2.ratio()>0.8:
            print shorter + "  :  " + long_substr
            print m2.ratio()
            print
            return 1
        #r = m2.ratio()
        # print r
        #scores.append(r)
    return 0;


#===============imports
import csv
import getpass
import sys
csv.field_size_limit(sys.maxsize)

#===============Read translation sheet
print "Reading translation sheet..."
tokenMap = {}
with open('DE.csv', 'rb') as csvfile:
    
    dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=',')
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)
    for row in reader:
        if len(row)!=2:
            print 'Error0:'+ str(len(row))
        else:
            tokenMap[row[1]]=row[0].lower();

w = csv.writer(open("outputToken.csv", "w"))
for key, val in tokenMap.items():
    w.writerow([key, val])

#=================Read web content sheet
print "Reading web content sheet..."
webContentMap = {}
with open('WC.csv', 'rb') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=',')
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)
    for row in reader:
        if len(row)<2:
            print 'Error1:'
        if len(row)==2:
            webContentMap[row[0]]=row[1].lower();
        if len(row)>2:
            print 'Error2:'

w = csv.writer(open("outputWebContent.csv", "w"))
for key, val in webContentMap.items():
    w.writerow([key, val])

#==================Fussy search
contentToTokenMap={}
i=0
for key, value in webContentMap.iteritems():
    #print key, value
    print i
    contentToTokenMap[key]=[];
    i+=1
    for tokenKey, tokenValue in tokenMap.iteritems():
        if s(tokenValue, value)>0:
            contentToTokenMap[key].append(tokenKey);

w = csv.writer(open("output.csv", "w"))
for key, val in contentToTokenMap.items():
    w.writerow([key, val])