import sys
import numpy
import nltk
import nltk.data
from nltk.tag import StanfordNERTagger

import collections
import yesno
import json
#from bs4 import BeautifulSoup
# from reduction import *
# reduction = Reduction()
reduced_text = ""
count = 0
cnt = 0
sent_list = []
# Setup
snow = nltk.stem.SnowballStemmer("english")

st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz',
					   'stanford-ner.jar',
					   encoding='utf-8')
#corenlp = StanfordCoreNLP()
sent_detector = nltk.data.load("tokenizers/punkt/english.pickle")

# Hardcoded word lists
yesnowords = ["can", "could", "would", "is", "does", "has", "was", "were", "had", "have", "did", "are", "will"]
commonwords = ["the", "a", "an", "is", "are", "were", "."]
questionwords = ["who", "what", "where", "when", "why", "how", "whose", "which", "whom"]

# Take in a tokenized question and return the question type and body
def processquestion(qwords):
    
    # Find "question word" (what, who, where, etc.)
    questionword = ""
    qidx = -1

    for (idx, word) in enumerate(qwords):
        if word.lower() in questionwords:
            questionword = word.lower()
            qidx = idx
            break
        elif word.lower() in yesnowords:
            return ("YESNO", qwords)

    if qidx < 0:
        return ("MISC", qwords)

    if qidx > len(qwords) - 3:
        target = qwords[:qidx]
    else:
        target = qwords[qidx+1:]
    type = "MISC"

    # Determine question type
    if questionword in ["who", "whose", "whom"]:
        type = "PERSON"
    elif questionword == "where":
        type = "PLACE"
    elif questionword == "when":
        type = "TIME"
    elif questionword == "how":
        if target[0] in ["few", "little", "much", "many"]:
            type = "QUANTITY"
            target = target[1:]
        elif target[0] in ["young", "old", "long"]:
            type = "TIME"
            target = target[1:]

    # Trim possible extra helper verb
    if questionword == "which":
        target = target[1:]
    if target[0] in yesnowords:
        target = target[1:]
    
    # Return question data
    return (type, target)

# Get command line arguments
articlefilename = sys.argv[1]
#questionsfilename = sys.argv[2]

# Process article file
#article = open(articlefilename, 'r')
article = open(articlefilename, encoding="utf8")
print(type(article))
article = article.read()
print(type(article))
article = sent_detector.tokenize(article)

# Process questions file
#questions = open(questionsfilename, 'r').read()
#questions = questions.decode('utf-8')
#questions = questions.splitlines()

# Iterate through all questions
while True:
    question = input()

    # Answer not yet found
    done = False

    # Tokenize question
    #print (question)
    qwords = nltk.word_tokenize(question.replace('?', ''))
    questionPOS = nltk.pos_tag(qwords)

    # Process question
    (type, target) = processquestion(qwords)

    # Answer yes/no questions
    if type == "YESNO":
        yesno.answeryesno(article, qwords)
        continue

    # Get sentence keywords
    searchwords = set(target).difference(commonwords)
    dict = collections.Counter()
        
    # Find most relevant sentences
    for (i, sent) in enumerate(article):
        sentwords = nltk.word_tokenize(sent)
        wordmatches = set(filter(set(searchwords).__contains__, sentwords))
        dict[sent] = len(wordmatches)
    
    max_match = max(dict.values())
    #print("max march", max_match)
    #print("ductionakty", dict)
    for i in dict:
        if max_match == dict[i]:
            sent_list.append(i)
    if len(sent_list) == 1:
        print("key", sent_list)
        print("target 0 : ", target[0])
        print("target -1 : ", target[-1])
        tokens = nltk.word_tokenize(sent_list[0])
        target_stem = snow.stem(target[-1])
        for word in tokens:
            stemmed = snow.stem(word)
            if stemmed == target_stem:
                endidx = sent_list[0].index(word)
            else:
                endidx = sent_list[0].index(target[-1])                

        #answer = sent_list[0][:endidx + len(target[-1])]
        answer = sent_list[0]
        done = True

    else:
        print("multiple keys")
        # Focus on 10 most relevant sentences
        for (sentence, matches) in dict.most_common(10):
            tokens = nltk.word_tokenize(sentence)
            parse = st.tag(tokens)
            sentencePOS = nltk.pos_tag(nltk.word_tokenize(sentence))

            # Attempt to find matching substrings
            searchstring = ' '.join(target)
            #print("search", searchstring) 
            #print("sent lisyt", sent_list[0])
            """if searchstring in sent_list[0]:
                startidx = sentence.index(target[0])
                endidx = sentence.index(target[-1])
                answer = sentence[:startidx]
                done = True"""
            for each_target in target:
                if each_target in sentence:
                    cnt+=1
            if cnt == len(target):
                tokens = nltk.word_tokenize(sent_list[0])
                target_stem = snow.stem(target[-1])
                for word in tokens:
                    stemmed = snow.stem(word)
                if stemmed == target_stem:
                    endidx = sent_list[0].index(word)
                else:
                    endidx = sent_list[0].index(target[-1])                

                #answer = sent_list[0][:endidx + len(target[-1])]
                answer = sent_list[0]
                done  = True
            # Check if solution is found
            if done:
                continue

            # Check by question type
            answer = ""
            #print("parse", parse)
            for worddata in parse:
                #print("worddata", worddata)
                # Mentioned in the question
                if worddata[0] in searchwords:
                    continue
            
                if type == "PERSON":
                    if worddata[1] == "PERSON":
                        answer = answer + " " + worddata[0]
                        done = True
                    elif done:
                        break

                if type == "PLACE":
                    if worddata[1] == "LOCATION":
                        answer = answer + " " + worddata[0]
                        done = True
                    elif done:
                        break

                if type == "QUANTITY":
                    if worddata[1] == "NUMBER":
                        answer = answer + " " + worddata[0]
                        done = True
                    elif done:
                        break

                if type == "TIME":
                    if worddata[1] == "NUMBER":
                        answer = answer + " " + worddata[0]
                        done = True
                    elif done:
                        answer = answer + " " + worddata[0]
                        break
            
    if done:
        print("answer",answer)
    if not done:
        (answer, matches) = dict.most_common(1)[0]
        #if len(answer) > 250:
        #    print("REDUCE")
        #    reduced_text = reduction.reduce(answer, 0.7)
        #    print(reduced_text, len(reduced_text))
        #else:
        print ("answer", answer)
