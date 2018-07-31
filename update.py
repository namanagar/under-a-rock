import tweepy, json, re, pendulum, requests, psycopg2, collections, math
from summa import keywords
from readability import Document
from tqdm import tqdm
from newsplease import NewsPlease
from operator import itemgetter
from math import ceil
from fuzzywuzzy import fuzz
from gensim.summarization import summarize
from keywordfinder import KeywordFinder

accounts=["cnnbrk","AP_Politics","BBCBreaking","Reuters","BreakingNews","AP"]
auth=tweepy.OAuthHandler("LYuZ8TRRBuJ7IQcoyyZYwe0uy","eIwCZsZ4IOQqe8p3nI4ybAJHcShILcpmwYkzLXW5xLSTplzDRl")
auth.set_access_token("928145131886317568-6bAb5L7Xj9OfiPYfgGTfMrYG6kCdZjC", "iRivk0tnYtPHaTLlwNipd6pECm7RcOHrNp0hPVvqx8AWb")
api = tweepy.API(auth)

f = open('other/credentials.txt')
credentials = json.load(f)
f.close()
conn = psycopg2.connect(dbname = credentials["dbname"],
                        user = credentials["user"],
                        host = 'localhost',
                        port = '5432',
                        password = credentials["password"])
cur = conn.cursor()

def updateTweetsInDatabase():
    '''returns a list of links from the twitter accounts in "accounts" in the last minutes'''

    #getting 200 tweets generally jumps past the stopping point, cut down to the subset that are before the specificed date
    data=getData()
    print(f'{len(data)} tweets found')
    tweetcount = dict(collections.Counter([j[1] for j in data]))
    print(json.dumps(tweetcount, indent=1))
    kwdDict = {}
    print('Extracting keywords...')
    for url,name,timestamp,tweet_text in tqdm(data):
        finder = KeywordFinder(url)
        keyphrases = finder.getKeyphrases()
        lede = finder.lede
        title = finder.title 
        cur.execute('''INSERT INTO public.articles VALUES (%s,%s,%s,%s,%s,%s)''', (url,keyphrases,title,name,lede,timestamp))
    print(f'Waiting to insert {len(data)} tweets into database')
    return


def getData():
    now = pendulum.now('UTC')
    print(f'''---Starting script: {now.to_day_datetime_string()}---''')
    cur.execute('''SELECT "timestamp" FROM public.articles ORDER BY "timestamp" DESC LIMIT 1''')
    start = pendulum.from_timestamp(cur.fetchone()[0],'UTC')
    print(f'Last tweet in database: {start.to_day_datetime_string()}')
    mintime = now.timestamp()-1209600.0
    cur.execute('''DELETE FROM public.articles WHERE timestamp<%s''', (mintime,))
    data=[]
    print(f'Fetching tweets from the last {start.diff().in_minutes()} minutes')
    for name in accounts:
        #assume at most 1 tweet per min 
        numtweets = min(200,int((now.timestamp()-start.timestamp())//20))
        status=api.user_timeline(screen_name=name,count=numtweets,tweet_mode='extended')
        for x in range(len(status)):
            data.append(status[x])
        lasttweet=json.loads(json.dumps(status[numtweets-1]._json))
        #ensure that the 3 tweets/hr covers the entire range. if not, keep pulling tweets
        while pendulum.parse(lasttweet["created_at"],strict=False)>start:
            morestatus=api.user_timeline(screen_name=name,count=numtweets,max_id=lasttweet["id"],tweet_mode='extended')
            lasttweet=json.loads(json.dumps(morestatus[len(morestatus)-1]._json))
            for z in range(len(morestatus)):
                data.append(status[z])
    return removeExcessTweets(dataToDateDict(data),start.timestamp())

def dataToDateDict(data):
    dateDict={}
    for item in data:
        tweetjson=json.loads(json.dumps(item._json))
        tweeted_datetime_utc=pendulum.parse(tweetjson["created_at"], strict=False)
        tweet_text = tweetjson["full_text"]
        name = tweetjson["user"]["screen_name"]
        urls = tweetjson['entities']['urls']
        if len(urls)>0 and len(urls[0]['url'])>0:
            dateDict[tweeted_datetime_utc.timestamp()] = (urls[0]['url'],name,tweeted_datetime_utc.timestamp(),tweet_text)
    return dateDict

def removeExcessTweets(dateDict,lastTimestamp):
    return [dateDict[key] for key in dateDict.keys() if key>lastTimestamp and isinstance(dateDict[key][0],str) and len(dateDict[key][0])>0]  

def generateGraphs():
    cur.execute('TRUNCATE public.graphs')
    seconds = [r*3600 for r in [3,6,12,24,48]]
    for amount in seconds:
        nodes=[]
        edges=[]
        cur.execute(f'''SELECT * FROM public.articles WHERE timestamp>{pendulum.now('UTC').timestamp()-amount} AND title IS NOT NULL''')
        print(f"Creating graph for last {amount/60} minutes")
        tweets = cur.fetchall()
        print(f'{len(tweets)} relevant tweets found')
        keywords_total = []
        urls = []
        kwd_to_urls = {}
        for url,keywords,title,name,lede,timestamp in tweets:
            urls.append({url:{'name':name,'title':title,'keywords':keywords}})
            keywords_total.extend(keywords)
            for c,keyword in enumerate(keywords):
                if keyword not in kwd_to_urls.keys():
                    kwd_to_urls[keyword] = []
                kwd_to_urls[keyword].append(url)
    
        covered = set()
        kwd_final = []
        for key, item in list(kwd_to_urls.items()):
            if len(item)<=1:
                del kwd_to_urls[key]
        elements = set([item for l in kwd_to_urls.values() for item in l])
        while covered!=elements:
            max_sub = max(kwd_to_urls, key = lambda x: len(set(kwd_to_urls[x])-covered))
            kwd_final.append(max_sub)
            covered |= set(kwd_to_urls[max_sub]) 
        count = collections.Counter(keywords_total)
        urls = cleanURLs(urls,kwd_final)
        print(urls)
        
        #add nodes
        for word in kwd_final:
            nodes.append({'label':word,'id':word,'size':count[word]})

        #add edges
        for i in range(len(kwd_final)-1):
            for j in range(i+1,len(kwd_final)):
                w1 = kwd_final[i]
                w2 = kwd_final[j]
                if w1!=w2:
                    if 2*len(set(kwd_to_urls[w1]) & set(kwd_to_urls[w2]))/(len(set(kwd_to_urls[w1]))+len(set(kwd_to_urls[w2])))>0.2:
                        edges.append({'id':w1+w2,'source':w1,'target':w2})
        
        cur.execute('''INSERT INTO public.graphs VALUES (%s,%s)''',(amount,json.dumps({'nodes':nodes,'edges':edges,'articles':urls})))
    print(f'Inserted {len(seconds)} graphs')

def cleanURLs(urls, kwd_final):
    filtered_urls = []
    for url in urls:
        filtered_kwds = [j for j in kwd_final if j in list(url.items())[0][1]['keywords']]
        if len(filtered_kwds)==0:
            continue
        url[list(url.keys())[0]]['keywords'] = filtered_kwds
        filtered_urls.append(url)
    return filtered_urls

def main():
    updateTweetsInDatabase()
    generateGraphs()
    conn.commit()
    cur.close()
    conn.close()
    print("DB changes confirmed")
    return

if __name__ == '__main__':
    main() 


