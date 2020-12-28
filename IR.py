from os import terminal_size
from ReadFiles import readFiles
from PreProcessing import preProcessing
from Indexer import indexer
from PhraseQuery import phraseQuery
from QueryPreProcessing import prepareQuery
import json
import time
import math

auxiliary_table = {}


def saveOnDisk(path, data):
    file = open(path, "w")
    json.dump(data, file)
    file.close


def loadFromDisk(path):
    data = None
    with open(path, "r") as fp:
        data = json.load(fp)
    return data


def readQueryFromUser():
    query = input("Enter your query :")
    return query


def getTableForTerms(list_query):
    try:
        global auxiliary_table
        for item in list_query:
            result = auxiliary_table[item]
            print(item, ":", result, "\n")
    except:
        return


def printTable(table):
    for key in table:
        print(key + ":", table[key], "\n")


def getTermFreq(table):
    sum = 0
    for key in table:
        sum += len(table[key])
    return sum


def printResult(query, result, time, df, tf, idf):
    print(
        "-------------------------------------------------------------------------------------------------------------------------------------------------"
    )
    print(query, "in", df, "documents", "with", tf, "times")
    print(
        "------------------------------------------------------------------------------------------------------------------------------------------------- \n"
    )
    printTable(result)

    print("idf : ", idf)
    print("Time taken is: ", time)


def calcIDF(total_num_of_doc, df):
    return math.log(total_num_of_doc / df, 10)


def main():
    global auxiliary_table
    query = readQueryFromUser()

    # prepare query, stop words removal, normalization, ...etc
    list_query = prepareQuery(query)
    if list_query == False:
        print("Wrong syntax!!")
        return

    # read files from disk
    start = time.time()
    files = readFiles("files/")

    # run preprocessing on files and save result on disk in data/data.json
    data = preProcessing(files)
    saveOnDisk("data/data.json", data)

    # load the tokens and result from data.json file
    data = loadFromDisk("data/data.json")

    # pass the result to Indexer to create the auxiliary table and save it on disk
    indexer("data/auxiliary table.json", data)

    # load the auxliliary from disk
    auxiliary_table = loadFromDisk("data/auxiliary table.json")

    # print auxliliary table for every term
    getTableForTerms(list_query)

    # pass the phrase query which enterd by user and auxlliary table to the phrasequery to get result
    # start = time.time()
    result = phraseQuery(auxiliary_table, list_query)
    end = time.time()

    term_frequency = getTermFreq(result)
    doc_frequency = len(result)
    idf = calcIDF(10, doc_frequency)

    printResult(query, result, end - start, doc_frequency, term_frequency, idf)


if __name__ == "__main__":
    main()