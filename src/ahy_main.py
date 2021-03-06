#!/usr/bin/python
import langmodel.ngram as ngram
import os
import tweepy

import mysql.connector
import time
import json

from mysql.connector import Error

from collections import Counter
from numpy import exp

from langutil.tokenizer import tokenize
from langutil.stemmer import ChaosStemmer
from langutil.tagger.sequentigram import NGramTag
from langutil.chunker.chunk import TagChunker
from langmodel.modeler.markov import NGramModels
from utils.loader import Loader

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener


consumer_key='jP99ZqVpvGVGHN3vA1ff24I9X'
consumer_secret='LyegLqYBAk6pCEafwrRFp9HIWETKbpeIG8qV9Wvy8WZhoha5hD'
access_token='1392391676-DoVxbpluZBYwN1FDRsS6UlkAVcbl0tLIzTwf3Td'
access_secret='9akl6YeSxV8fnIlwYypRdWZmhWt0jXKTfyHRmOVl896H3'
print 'haha'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

#Please repair this :"
#Take all data in twitter for ahok. But I don't know when it will stop.
#https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('dataanies.json', 'a') as f:

                import unicodedata
                print ('unicode')
                print(data)

                print ('string')
                newData = unicodedata.normalize('NFKD', data).encode('ascii', 'ignore')
                f.write(newData + ',')
                return True
        except BaseException as e:
            print("Error on_data: ", e)
        return True
 
    def on_error(self, status):
        print(status)
        return True

# print 'stream'
# print ('stream1')
#print(api.VerifyCredentials())

#query = Twitter.search.tweets(q = "ahok")
#print "Search complete (%.3f seconds)" % (query["search_metadata"]["completed_in"])

MAIN_DIR = os.path.abspath(os.path.curdir)
DS_DIR = '/dataset/'

def TextTokenizer(sen):
    # Materi Syntatic proses:text tokenizing
    # http://blog.pantaw.com/syntatic-proses-text-tokenizing/
    stopwords= ['kah','lah','pun','jah','jeh','mu','ku','ke','di','tapi','saya','kamu','mereka','dia', \
          'kita','adalah','dan','jika','kalau','sama','yang', \
          'sekarang','nanti','besok','kemarin','kemaren','nya','na',\
          'at','apa','ini','itu','juga','ketika','namun',\
          'sebab','oleh','malah','memang']
        
    tok = tokenize()
    kata = tok.WordTokenize(sen,removepunct=False)
    if kata:
        print "kalimat setelah di tokenize: ", kata, "\n"
    return kata

def NgramModel(sen):
    # Materi Syntatic proses:N-Gram
    # http://blog.pantaw.com/syntatic-proses-n-grams/
    kata = TextTokenizer(sen)
    kata = ngram.ngrams(kata,n=2,njump=3)
    
    print "Total sample: ", len(kata)

def stemm(toksen):
    # Materi Syntatic proses: Text Stemmer bahasa Indonesia dengan Python
    # http://blog.pantaw.com/syntatic-proses-text-stemmer-bahasa-indonesia-dengan-python/
    morph = ChaosStemmer(MAIN_DIR+DS_DIR, 'tb_katadasar.txt')
    
    for z in words:
        morph.stemm(z)
        #menyeimbangkan,menyerukan,mengatakan,berkelanjutan,pembelajaran,pengepulannya
        #print "Dirty guess word is: ",morph.getFoundGuessWord()
        #print "Detected Affix is: ", morph.getFoundSuffix(),"\n"
        print "Root kata untuk kata: ", z ," -> adalah: ", morph.getRootWord()
        print "Filtered guess word adalah:", morph.getFilteredGuessWord(),"\n"

def chunk(sent):
    # Proses chunking harus selalu didahuli dengan proses tagging text
    tagger = NGramTag(MAIN_DIR+DS_DIR,r'tb_tagged_katadasar.txt')
    chunk = TagChunker()
    result = tagger.tag(sent)

    return result
    # print chunk.treePrint(chunk.tagChunk(tagger.tag(sent, tagregex=True, verbose=True)))
    #print chunk.tagTokenExtractor(tagger.tag(sent))
    # print chunk.tagChunk(tagger.tag(sent))
    #print chunk.tagTokenizer(chunk.tagChunk(tagger.tag(sent)))

    #tagger.tag(sent,tagregex=True)
    #print tagger.tag(sent)

    # Delete specific tag
    #print delTag(sent,'XX')
    
    # Ekstrak specific tag
    # print chunk.treeExtractor(chunk.tagChunk(tagger.tag(sent)),lambda t: t.label() == 'PRED')


    # print ('haha')
    # print tagger.tag(sent)
    
def NGramLangModel():
    cl = Loader(MAIN_DIR+DS_DIR)
    f = cl.loadLarge('tb_kota_bywiki.txt',lazy_load=True)#tb_berita_onlinemedia, tb_kota_bywiki
    w = cl.processRaw(f,to_lower=True)
    r = cl.rawForLangmodel(w,punct_remove=True,to_token=True)
    
    lms = NGramModels(ngram=2)
    # njump parameter belum bisa digunakan untuk modkn optimizer
    models = lms.train(r, optimizer='modkn',\
                       separate=False, njump=0, verbose=False)

    print "##########################################################"

def insertTweetToMySql(data, calon):
  try:
        conn = mysql.connector.connect(host='localhost',
                                       database='nlp_text',
                                       user='root',
                                       password='alberttriadrian')
        if conn.is_connected():
            cursor = conn.cursor();
            print('Connected to MySQL database')

            for datum in data:
              datum["text"] = datum["text"].replace("'", "")
              datum["user"]["name"] = datum["user"]["name"].replace("'","")
              if (datum["user"]["location"] is None):
                datum["user"]["location"] = 'UNKNOWN'

              if (datum["user"]["description"] is None):
                datum["user"]["description"] = 'UNKNOWN'

              datum["user"]["description"] = datum["user"]["description"].replace("'","")
              cursor.execute("INSERT INTO twitter (created_at,teks, name, location, description, follower_count, friends_count, retweet_count, calon, tweet_id) VALUES (\'" + datum["created_at"] + "\',\'" + (datum["text"]) + "\',\'" + datum["user"]["name"] + "\',\'" + (datum["user"]["location"]) + "\',\'" + (datum["user"]["description"]) + "\'," + str(datum["user"]["followers_count"]) + "," +str(datum["user"]["friends_count"]) + "," + str(datum["retweet_count"]) + ",\'" + calon + "\',\'" + str(datum["id"]) + "\')")
              conn.commit()
            print("Finish add to database")
        conn.close()
  except Error as e:
    print(e)

def insertTweetKata(data, calon):
  #0 : tweet_id
  #1 : kata
  print ('albert')
  try:
        conn = mysql.connector.connect(host='localhost',
                                       database='nlp_text',
                                       user='root',
                                       password='alberttriadrian')
        if conn.is_connected():
            cursor = conn.cursor();
            print('Connected to MySQL database')

            for datum in data:
              cursor.execute("INSERT INTO tweet_kata (calon, kata, tweet_id) VALUES (\'" + calon + "\',\'" + datum[1] + "\',\'" + str(datum[0]) + "\')")
              conn.commit()
            print("Finish add to database")
        conn.close()
  except Error as e:
    print(e)

def insertTweetResult(data, calon):
  #0 : kata
  #2 : jumlah_kemunculan
  try:
        conn = mysql.connector.connect(host='localhost',
                                       database='nlptext',
                                       user='root',
                                       password='')
        if conn.is_connected():
            cursor = conn.cursor();
            print('Connected to MySQL database')

            for datum in data:
              cursor.execute("INSERT INTO tweet_result (calon, kata, jumlah_kemunculan) VALUES (\'" + calon + "\',\'" + datum[0] + "\'," + str(datum[2]) + ")")
              conn.commit()
            print("Finish add to database")
        conn.close()
  except Error as e:
    print(e)

    
if __name__ == "__main__":   

    ADJECTIVE_WORD_TYPE = 'ADJ'

    with open('dataahy.json') as json_data:
        d = json.load(json_data)

        insertTweetToMySql(d, "AHY")

        finalResult = []
        finalTweets = []

        for data in d:

            result = chunk(data['text'])

            filteredResult = filter(lambda (word, wordType),: wordType == ADJECTIVE_WORD_TYPE, result)

            wordCounterResult = Counter(filteredResult)
            wordCounts = list(wordCounterResult.items())

            wordCounts.sort(key = (lambda tupleItem: tupleItem[1]), reverse = True)

            for wordCount in wordCounts:
                word = wordCount[0][0]
                wordType = wordCount[0][1]
                wordCount = wordCount[1]

                finalTweets.append((data['id'], word))

                found = False
                numberOfFinalResult = len(finalResult)
                i = 0

                while (not found and i < numberOfFinalResult):
                    if (finalResult[i][0] == word):
                        finalResult[i] = (word, wordType, finalResult[i][2] + wordCount)
                        found = True
                    else:
                        i = i + 1

                if (not found):
                    finalResult.append((word, wordType, wordCount))                    

        finalResult.sort(key = lambda item: item[2], reverse = True)
        print finalResult

    print ('setelah unused word dibuang')
    with open("dataset/stopwords.txt", "r") as ins:
        unusedWords = []
        for line in ins:
            unusedWords.append(line)

        for data in finalResult:
            for data2 in unusedWords:
                if data[0] == data2:
                    finalResult.remove(data)

    for data in finalResult:
        print data[0]

    insertTweetKata(finalTweets, "AHY")

    with open('ahy_result.txt', 'a') as the_file:
        for data in finalResult:
            the_file.write(data[0] + ',' + str(data[2]) + '\n')


    # kata = "ahok sangat hebat hebat albert juga sangat kejam, marco juga sangat cepat"


    # # ## Stemming hanya membutuhkan textTokenize
    # # #words = TextTokenizer(kata.lower())
    # # #stemm(words)

    # # #NgramModel(kata.lower())
    # # #NGramLangModel()

    # print kata

