# -*- coding: utf8 -*-
import json, pyUtilsClass
from flask import Flask
from flask import request
from flask import jsonify
from pyDAOClass import *

dao = DAO()
utils = pyUtilsClass.Utils()
subjectList = utils.readJsonFile(utils.getLocalPath() + '/../config/subject.json')
app = Flask(__name__)

def setDBConnection(dbConfig):
    dao.setClient(dbConfig["host"], dbConfig["port"], dbConfig["id"], dbConfig["pw"])
    dao.setDB(dbConfig["database"])
    return dao

@app.route('/')
def index():
    return 'Welcome to TrendyWord WebApp'

# input: 단어, 검색 컬렉션 이름
# output(json):
#       1. WordDictionary :: 단어 의미, 발음기호, 사운드링
#       2. WordCount :: 단어 카운트 정보
@app.route('/word_info/', methods=['GET'])
def getWordInfo():
    word = request.args.get('word')
    collection = request.args.get('collection')

    # 컬렉션 선택
    dao.setCollection(collection)

    query = '{"word": "%s"}' % word
    wordInfo = dao.select(query)

    result = ''
    if wordInfo is None:
        result = '[WNF] %s is not found in word dictionary' % word
    else:
        result = wordInfo['info'] if collection == 'WordDictionary' else wordInfo['count']

    #return jsonify(json.dumps(result, ensure_ascii=False))
    return result

# input: 출력 TOP N 단어수, 정렬 기준점[totalCount, yearly, monthly, daily, bySubject], 날짜, 주제
# output(json):
#       - 기준점 별 TOP N { 단어, 카운트 } 출력
@app.route('/word_info/top_rank/', methods=['GET'])
def getWordRank():
    rank = request.args.get('rank')
    cycle = request.args.get('cycle')
    date = request.args.get('date')
    subject = request.args.get('subject')

    # 단어 카운트 컬렉션 선택
    dao.setCollection("WordCount")

    query = '{}'
    filterInfo = '{"_id":0, "word": 1, "count": 1 }'
    wordInfo = dao.selectMany(query, filterInfo)

    data = {}
    for wordCount in wordInfo:
        data[wordCount['word']] = getCountInfo(wordCount['count'], cycle, date, subject)

    sortedData = sorted(data.items(), key=(lambda x: x[1]), reverse = True)
    return json.dumps(sortedData[:int(rank)], ensure_ascii=False)

def getCountInfo(countInfo, cycle, date, subject):

    count = 0
    if cycle == 'totalCount':
        count = countInfo[cycle]
    elif cycle == 'yearly':
        count = countInfo[cycle][date]
    elif cycle == 'monthly':
        year = date[:4]
        month = int(date[5:])-1
        count = countInfo[cycle][year][month]
    elif cycle == 'daily':
        yearAndMonth = date[:6]
        day = int(date[7:]) - 1
        count = countInfo[cycle][yearAndMonth][day]
    else:
        # bySubject
        count = countInfo[cycle][subjectList[subject]]

    return count