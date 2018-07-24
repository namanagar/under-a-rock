import tweepy, json, re, pendulum, requests, psycopg2, collections, math
from summa import keywords
from readability import Document
from tqdm import tqdm
from operator import itemgetter
from math import ceil

accounts=["cnnbrk","AP_Politics","BBCBreaking","Reuters","BreakingNews","AP"]
flaggedPhrases=["follow live updates","follow updates","icymi","exclusive","breaking","reuters","said","news","file","report","state","states","reporting"]
auth=tweepy.OAuthHandler("LYuZ8TRRBuJ7IQcoyyZYwe0uy","eIwCZsZ4IOQqe8p3nI4ybAJHcShILcpmwYkzLXW5xLSTplzDRl")
auth.set_access_token("928145131886317568-6bAb5L7Xj9OfiPYfgGTfMrYG6kCdZjC", "iRivk0tnYtPHaTLlwNipd6pECm7RcOHrNp0hPVvqx8AWb")
api = tweepy.API(auth)

f = open('credentials.txt')
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
        response = requests.get(url)
        doc = Document(response.text)
        text = re.sub('<[^<]+?>','',doc.summary())
        title = doc.short_title()
        kwdandscores = keywords.keywords(text, split=True, scores=True)
        kwdList = [x for x in kwdandscores if len(x[0])>=3 and x[0].lower() not in flaggedPhrases]
        kwdInTweet = [kwd[0] for kwd in kwdList if kwd[0] in tweet_text]
        cur.execute('''INSERT INTO public.tweets VALUES (%s,%s,%s,%s,%s,%s,%s)''', (url,name,timestamp,[a[0] for a in kwdList],kwdInTweet,title,[b[1] for b in kwdList]))
    print(f'Waiting to insert {len(data)} tweets into database')
    return

def getData():
    now = pendulum.now('UTC')
    print(f'''---Starting script: {now.to_day_datetime_string()}---''')
    cur.execute('''SELECT "timestamp" FROM public.tweets ORDER BY "timestamp" DESC LIMIT 1''')
    start = pendulum.from_timestamp(cur.fetchone()[0],'UTC')
    print(f'Last tweet in database: {start.to_day_datetime_string()}')
    mintime = now.timestamp()-1209600.0
    cur.execute('''DELETE FROM public.tweets WHERE timestamp<%s''', (mintime,))
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
        cur.execute(f'''SELECT * FROM public.tweets WHERE timestamp>{pendulum.now('UTC').timestamp()-amount} AND keywordscores IS NOT NULL''')
        print(f"Creating graph for last {amount/60} minutes")
        tweets = cur.fetchall()
        print(f'{len(tweets)} relevant tweets found')
        keywords_total = []
        keywordscores_dict = {}
        urls = []
        kwd_to_urls = {}
        for url,name,timestamp,keywords,keywordsintitle,title,keywordscores in tweets:
            urls.append({url:{'name':name,'title':title,'keywords':keywords}})
            keywords_total.extend(keywords)
            for c,keyword in enumerate(keywords):
                if keyword not in kwd_to_urls.keys():
                    kwd_to_urls[keyword] = []
                kwd_to_urls[keyword].append(url)
                if keyword not in keywordscores_dict.keys():
                    keywordscores_dict[keyword] = []
                keywordscores_dict[keyword].append(keywordscores[c])
        kwd_final = sorted([(word, 2/(1+math.exp(-1*sum(keywordscores_dict[word])/math.sqrt(amount/3600)))-1) for word,score in collections.Counter(keywords_total).most_common(20)],key=itemgetter(1),reverse=True)[:10]
        urls = cleanURLs(urls,kwd_final)
        
        #add nodes
        for word,score in kwd_final:
            nodes.append({'label':word,'id':word,'size':ceil(10*score)})

        #add edges
        for i in range(len(kwd_final)-1):
            for j in range(i+1,len(kwd_final)):
                if kwd_final[i][0]!=kwd_final[j][0]:
                    if 2*len(set(kwd_to_urls[kwd_final[i][0]]) & set(kwd_to_urls[kwd_final[j][0]]))/(len(set(kwd_to_urls[kwd_final[i][0]]))+len(set(kwd_to_urls[kwd_final[j][0]])))>0.3:
                        edges.append({'id':kwd_final[i][0]+kwd_final[j][0],'source':kwd_final[i][0],'target':kwd_final[j][0]})
        
        cur.execute('''INSERT INTO public.graphs VALUES (%s,%s)''',(amount,json.dumps({'nodes':nodes,'edges':edges,'articles':urls})))
    print(f'Inserted {len(seconds)} graphs')

def cleanURLs(urls, kwd_final):
    filtered_urls = []
    for url in urls:
        filtered_kwds = [j for j,k in kwd_final if j in list(url.items())[0][1]['keywords']]
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


