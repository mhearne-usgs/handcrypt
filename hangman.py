#!/usr/bin/env python

import random
import hashlib
import sys
import string
import collections

DIGRAPHS = 'TH, HE, AN, IN, ER, ON, RE, ED, ND, HA, AT, EN, ES, OF, NT, EA, TI, TO, IO, LE, IS, OU, AR, AS, DE, RT, VE'.split(',')
LETTERS = 'etaoinshrdlcumwfgypbvkjxqz'
VOWELS = 'eaoiuy'

class WordServer(object):
    limbs = 0
    maxlimbs = 6
    wordfile = None
    wordhash = {}
    testWord = None
    def __init__(self,wordfile):
        f = open(wordfile,'rt')
        words = f.readlines()
        f.close()
        for word in words:
            m = hashlib.sha512()
            m.update(word[0:-1])
            hashtext = m.hexdigest()
            self.wordhash[hashtext] = word[0:-1]

    def start(self,testword=None):
        if testword is None:
            n = len(self.wordhash)
            wordidx = random.randint(0,n-1)
            hashtext = self.wordhash.keys()[wordidx]
            wordlength = len(self.wordhash[hashtext])
        else:
            self.testWord = testword
            m = hashlib.sha512()
            m.update(testword)
            hashtext = m.hexdigest()
            wordlength = len(testword)
                        
        self.limbs = 0
        return (hashtext,wordlength,self.limbs)

    def guess(self,letter,hashtext,guessed):
        letter = letter.lower()
        if self.testWord is not None:
            word = self.testWord
        else:
            word = self.wordhash[hashtext]
        if self.limbs > self.maxlimbs:
            raise Exception,word
        if letter not in word:
            self.limbs += 1
            return (guessed,self.limbs)
        n = word.count(letter)
        off = 0
        for i in range(0,n):
            idx = word.find(letter,off)
            guessed = guessed[0:idx]+letter+guessed[idx+1:]
            off = idx
        return (guessed,self.limbs)

def getMostCommonLetters(guess,bindict,wordlist=None):
    nword = len(guess)
    if wordlist is None:
        wordlist = bindict[nword]
    else:
        pass
    letters = string.ascii_lowercase
    freqs = zip(letters,[0 for l in letters])
    freqs = [list(f) for f in freqs]
    for word in wordlist:
        word = word.lower()
        for ch in word:
            idx = letters.find(ch)
            freqs[idx][1] += 1
    freqs = sorted(freqs,key=lambda freq: freq[1],reverse=True)
    newfreqs = []
    for f in freqs:
        if f[0] not in guess:
            newfreqs.append(f)
    common = ''.join([freq[0] for freq in newfreqs])
    return common

def getMostCommonLettersByDigraph(guess,alreadyguessed):
    letters = []
    for i in range(0,len(guess)-1):
        ch = guess[i]
        ch1 = guess[i+1]
        if ch == '_' and ch1 != '_':
            for dig in DIGRAPHS:
                dig = dig.lower().strip()
                if dig[1] == ch1:
                    letters.append(dig[0])
        if ch1 == '_' and ch != '_':
            for dig in DIGRAPHS:
                dig = dig.lower()
                if dig[0] == ch:
                    letters.append(dig[1])

    letters = list(set(letters).difference(alreadyguessed))
    if not len(letters):
        return letters
    c = collections.Counter(letters)
    mostcommon = [c[0] for c in c.most_common()]
    return mostcommon
        
def getMatchingWords(guess,bindict,wordlist=None):
    nword = len(guess)
    if wordlist is None:
        wordlist = bindict[nword]
    if guess.count('_') == len(guess):
        return wordlist
    newlist = []
    nright = len(guess) - guess.count('_')
    for word in wordlist:
        score = 0
        for i in range(0,len(word)):
            if word[i] == guess[i]:
                score += 1
        if score == nright:
            newlist.append(word)
    return newlist

if __name__ == '__main__':
    ws = WordServer('words.txt')
    f = open('englishwords.txt','rt')
    words = f.readlines()
    f.close()

    bindict = {}
    for word in words:
        word = word[0:-1]
        nword = len(word)
        if bindict.has_key(nword):
            bindict[nword].append(word)
        else:
            bindict[nword] = [word]
    
    nright = 0
    nwrong = 0
    numberofwords = 0
    #for word in words:
    while numberofwords < 2000:
        word = word.strip()
        if len(word) < 4:
            continue
        numberofwords += 1
        hashtext,wlen,limbs = ws.start(testword=word)
        guess = '_'*wlen
        mostcommon = list(getMostCommonLetters(guess,bindict))
        alreadyguessed = []
        while guess.count('_'):
            # letters = getMostCommonLettersByDigraph(guess,alreadyguessed)
#             if not len(letters):
#                 letter = mostcommon.pop(0)
#             else:
#                 letter = letters.pop(0)
            letter = mostcommon.pop(0)
            if letter in alreadyguessed:
                continue
            alreadyguessed.append(letter)
            try:
                guess,limbs = ws.guess(letter,hashtext,guess)
            except Exception,msg:
                #print 'Crap - I could not get the word "%s"' % msg
                nwrong += 1
                break
            if guess.count('_') == 0:
                #print 'I correctly guessed "%s"' % guess
                nright += 1
                break
            wordlist = getMatchingWords(guess,bindict)
            mostcommon = list(getMostCommonLetters(guess,bindict,wordlist))

    fmt = '%i words: Correct %i Incorrect: %i (%.1f%% success rate)'
    print fmt % (numberofwords,nright,nwrong,float(nright)/numberofwords*100)
            
                                
