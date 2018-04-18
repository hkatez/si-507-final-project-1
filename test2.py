#from ig import igdb
#from igdb_api_python import igdb
from igdb_api_python.igdb import igdb as igdb
from datetime import datetime
import time, os
import sqlite3
import requests
import json
import secrets
import math

def get_datetime():
    now = time.strftime("%a %b %d %H:%M:%S %Y")
    time.sleep(5)
    soon = time.strftime("%a %b %d %H:%M:%S %Y")
    tdelta = datetime.strptime(now, '%a %b %d %H:%M:%S %Y') - datetime.strptime(soon, '%a %b %d %H:%M:%S %Y')
    print(tdelta.total_seconds())
    # timestamp2 = "Jan 27 11:52:02 2014"
    #
    # t1 = datetime.strptime(timestamp1, "%b %d %H:%M:%S %Y")
    # t2 = datetime.strptime(timestamp2, "%b %d %H:%M:%S %Y")
    #
    # difference = t1 - t2
    #
    # print(difference.days) # 380, in this case
    #
    # latest = max((t1, t2)) # t1, in this case

get_datetime()

#ENTER YOUR KEY HERE

API_KEY = secrets.API_KEY

igdb = igdb(API_KEY)

#DB starts
DBNAME = 'test.db'
#CACHE_FNAME
games_cache = 'games.json'
platform_cache = 'platform.json'
CACHE_FNAME = "cache.json"
CACHE_DICTION = {}
# GET COMING SOOM PLAYSTATION 4 GAMES


# try:
#     cache_file = open(CACHE_FNAME, 'r')
#     cache_contents = cache_file.read()
#     CACHE_DICTION = json.loads(cache_contents)
#     cache_file.close()
#
# # if there was no file, no worries. There will be soon!
# except:
#     CACHE_DICTION = {}
#
def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

#Code for Part 1:Get Tweets





# baseurl = 'https://api-2445582011268.apicast.io/platforms/'
# params ={ 'ids': 47, 'fields' : 'games', 'limit':50 }

# resp = requests.get(baseurl, params = params, headers = headers )
# cache = json.loads(resp.text)
# print(cache)
def check_platform_cache():
    now = time.strftime("%a %b %d %H:%M:%S %Y")
    tdelta = datetime.strptime(now, '%a %b %d %H:%M:%S %Y') - datetime.strptime(CACHE_DICTION["platform_time"], '%a %b %d %H:%M:%S %Y')
    if tdelta.total_seconds > 1340000:
        return True
    else:
        return False


def get_platform_info():

    result = igdb.platforms({
        'fields':["name", "id", "summary", "alternative_name", "generation"],
        'scroll':1,
        'limit':50
    })
    list_of_platforms = []
    xcount = result.headers["X-Count"]
    timestoscroll = (math.ceil((int(xcount)) / 50)) - 1
    for x in range(timestoscroll):
        for y in result.body:
            empty_dict = {}
            try:
                empty_dict["id"] = y["id"]
            except:
                empty_dict["id"] = ""
            try:
                empty_dict["name"] = y["name"]
            except:
                empty_dict["name"] = ""
            try:
                empty_dict["alternative_name"] = y["alternative_name"]
            except:
                empty_dict["alternative_name"] = ""
            try:
                empty_dict["generation"] = y["generation"]
            except:
                empty_dict["generation"] = ""
            try:
                empty_dict["summary"] = y["summary"]
            except:
                empty_dict["summary"] = ""
            list_of_platforms.append(empty_dict)
        result = igdb.scroll(result)
    # loaded_json = json.loads(newresult.text)
    dumped_json = json.dumps(list_of_platforms, indent = 4)
    fw = open(platform_cache,"w")
    fw.write(dumped_json)
    fw.close()
    CACHE_DICTION["platform_time"] = time.strftime("%a %b %d %H:%M:%S %Y")
    dumped_json = json.dumps(CACHE_DICTION, indent = 4)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json)
    fw.close()



def init_db():
    #code to create a new database goes here
    #handle exception if connection fails by printing the error

    try:
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()
    except Exception as e:
        print(e)
    #code to test whether table already exists goes here
    #if exists, prompt to user: "Table exists. Delete?yes/no"
    #if user input is yes, drop table. Else, use move on and use existing table


    statement = '''
        DROP TABLE IF EXISTS 'Games';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Platforms';
    '''
    cur.execute(statement)
    conn.commit()

    statement = ' CREATE TABLE `Games` ( '
    statement += '   `Id`        INTEGER UNIQUE PRIMARY KEY,'
    statement += '   `Name`  TEXT,'
    statement += '  `UserRating`    TEXT,'
    statement += '  `ReleaseDate`  TEXT ,'
    statement += '  `URL`    TEXT );'



    try:
        cur.execute(statement)
        conn.commit()
    except:
        # print('Table Exists. Delete? y/n')
        # while True:
        #     decision = input()
        #
        #     if decision == "y":
        #         dropstatement = ' DROP TABLE `Tweets` '
        #         cur.execute(dropstatement)
        #         cur.execute(statement)
        #         conn.commit()
        #         break
        #     elif decision == 'n':
        #         break
        #     else:
        #         pass
        pass


    statement = ' CREATE TABLE `Platforms` ( '
    statement += '   `Id`        INTEGER UNIQUE PRIMARY KEY,'
    statement += '   `Name`  TEXT,'
    statement += '  `AlternativeName`    TEXT,'
    statement += '  `ConsoleGeneration`  TEXT ,'
    statement += '  `Summary`    TEXT );'
    try:
        cur.execute(statement)
        conn.commit()
    except:
        pass


    #close database connection
    conn.close()
    #this function is not expected to return anything, you can modify this if you want



# def add_games_data():
#     # Connect to choc database
#     conn = sqlite3.connect('test.db')
#     cur = conn.cursor()
#
#
#     ### Add countries data first
#     with open('games.json') as json_data:
#         g = json.load(json_data)
#
#
#     for game in g:
#
#
#         #Add code to insert each of these data of interest to the games table
#         params= (game["id"], game["name"], game["rating"], game["release_date"], game["url"] )
#         try:
#             cur.execute(" INSERT INTO `Games` VALUES (?, ?, ?, ?, ?)", params)
#
#         except:
#             print("168")
#             pass #bandaid for repeat Tweets
#     conn.commit()
#     conn.close()

def add_platform_data():
    # Connect to choc database
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()


    ### Add countries data first
    with open(platform_cache) as json_data:
        g = json.load(json_data)


    for console in g:


        #Add code to insert each of these data of interest to the games table
        params= (console["id"], console["name"], console["alternative_name"], console["generation"], console["summary"] )
        try:
            cur.execute(" INSERT INTO `Platforms` VALUES (?, ?, ?, ?, ?)", params)

        except:
            print("168")
             #bandaid for repeat Tweets
    conn.commit()
    conn.close()

# get_platform_info()
# init_db()
# add_platform_data()



 # Close the open file
