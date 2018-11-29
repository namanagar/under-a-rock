import tweepy, json, re, pendulum, requests, psycopg2, collections, math
from tqdm import tqdm
from newsplease import NewsPlease
from keywordfinder import KeywordFinder
from math import floor, log
from keywordextractor import KeywordExtractor
#todo: things similar on wikipedia, scores for articles, different colors,
from newspaper import Article
from newspaper.article import ArticleException
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies


accounts=["cnnbrk","AP_Politics","BBCBreaking","Reuters","BreakingNews","AP","foxnewspolitics","AFP","thehill","politico","USATODAY","axios","washingtonpost","NPR","nytpolitics"]
account_names = {"cnnbrk":"CNN","AP_Politics":"AP","BBCBreaking":"BBC","Reuters":"Reuters","AP":"AP","BreakingNews":"NBC","foxnewspolitics":"Fox News","AFP":"AFP","thehill":"The Hill","politico":"Politico","USATODAY":"USA Today","axios":"Axios","washingtonpost":"The Washington Post","NPR":"NPR","nytpolitics":"The New York Times"}
flaggedPhrases = ["reuters",'ap','usa today','united states']


f = open('other/credentials.txt')
credentials = json.load(f)
f.close()
auth = tweepy.OAuthHandler(credentials["tweepyauth1"],credentials["tweepyauth2"])
auth.set_access_token(credentials["tweepyaccess1"], credentials["tweepyaccess2"])

api = tweepy.API(auth)
conn = psycopg2.connect(dbname = credentials["dbname"],
                        user = credentials["user"],
                        host = 'localhost',
                        port = '5432',
                        password = credentials["password"],
                        connect_timeout=10)
cur = conn.cursor()

def updateTweetsInDatabase():
    '''gets all new tweets since the most recent tweet in the database'''

    #get all the tweets
    data=getData()

    #print update
    print(f'{len(data)} tweets found')
    tweetcount = dict(collections.Counter([j[1] for j in data]))
    print(json.dumps(tweetcount, indent=1))

    #get the keywords to insert into DB
    kwdDict = {}
    print('Extracting keywords...')
    for url,name,timestamp,tweet_text,tweet_id in tqdm(data):
        title, text = getArticleTitleText(url)

        #make sure article could be found
        if title!='error':

            #extract non-flagged keyphrases
            finder = KeywordExtractor(text)
            keyphrases = [keyphrase for keyphrase in finder.getKeyphrases() if keyphrase.lower() not in flaggedPhrases]
            print(keyphrases)

            #make sure keyphrases were found in the article
            if len(keyphrases)>0:

                #add the tweet if it doesn't already exist in the database
                lede = text[:175]
                cur.execute('''SELECT "title","lede" FROM public.articles''')
                if (title in [x[0] for x in list(cur.fetchall())]) or (lede in [s[1] for s in list(cur.fetchall())]):
                    print("Article already exists in db: ",title)
                else:
                    cur.execute('''INSERT INTO public.articles VALUES (%s,%s,%s,%s,%s,%s)''', (url,keyphrases,title,name,lede,timestamp))
                    #api.update_status(f'@{name} Tired of reading the news? Visualize it at underarock.net',tweet_id)
    print(f'Waiting to insert {len(data)} tweets into database')
    return


def getData():
    now = pendulum.now('UTC')
    print(f'''---Starting script: {now.to_day_datetime_string()}---''')
    cur.execute('''SELECT "timestamp" FROM public.articles ORDER BY "timestamp" DESC LIMIT 1''')
    start = pendulum.from_timestamp(cur.fetchone()[0],'UTC')
    print(f'Last tweet in database: {start.to_day_datetime_string()}')
    #mintime = now.timestamp()-1209600.0
    #cur.execute('''DELETE FROM public.articles WHERE timestamp<%s''', (mintime,))
    data=[]
    print(f'Fetching tweets from the last {start.diff().in_minutes()} minutes')
    for name in accounts:
        print('Collecting tweets from',name)
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
        tweet_id = tweetjson['id']
        tweet_text = tweetjson["full_text"]
        name = tweetjson["user"]["screen_name"]
        urls = tweetjson['entities']['urls']
        if len(urls)>0 and len(urls[0]['url'])>0:
            dateDict[tweeted_datetime_utc.timestamp()] = (urls[0]['url'],name,tweeted_datetime_utc.timestamp(),tweet_text,tweet_id)
    return dateDict

def removeExcessTweets(dateDict,lastTimestamp):
    return [dateDict[key] for key in dateDict.keys() if key>lastTimestamp and isinstance(dateDict[key][0],str) and len(dateDict[key][0])>0]  

def generateGraphs():
    cur.execute('TRUNCATE public.graphs')
    seconds = [r*3600 for r in [3,4,5,6,12,24,48]]
    for amount in seconds:
        nodes=[]
        edges=[]
        cur.execute(f'''SELECT url,keywords,title,name,lede,timestamp FROM public.articles WHERE timestamp>{pendulum.now('UTC').timestamp()-amount} AND title IS NOT NULL''')
        print(f"Creating graph for last {amount/60} minutes")
        tweets = cur.fetchall()
        print(f'{len(tweets)} relevant tweets found')
        keywords_total = []
        urls = []
        kwd_to_urls = {}
        for url,keywords,title,name,lede,timestamp in tweets:
            if title not in [qwe['title'] for qwe in urls]:
                urls.append({'url':url,'name':account_names[name],'title':title,'keywords':keywords,'lede':lede,'timestamp':timestamp})
            keywords_total.extend(keywords)
            for c,keyword in enumerate(keywords):
                if keyword not in kwd_to_urls.keys():
                    kwd_to_urls[keyword] = []
                kwd_to_urls[keyword].append(url)
    
        covered = set()
        kwd_final = []
        # min_keywords = 1 if amount<=(12*3600) else 3
        # for key, item in list(kwd_to_urls.items()):
        #     if len(item)<=min_keywords:
        #     #if len(item)<=2:
        #         del kwd_to_urls[key]
        elements = set([item for l in kwd_to_urls.values() for item in l])
        num=0
        while covered!=elements and num<15:
            max_sub = max(kwd_to_urls, key = lambda x: len(set(kwd_to_urls[x])-covered))
            kwd_final.append(max_sub)
            covered |= set(kwd_to_urls[max_sub])
            num+=1
        count = collections.Counter(keywords_total)
        for w,s in count.most_common(10):
            #if w not in kwd_final and s>min_keywords:
            if w not in kwd_final:
                kwd_final.append(w)
        urls = cleanURLs(urls,kwd_final)
        scaler = count.most_common(1)[0][1]/5
        final_scores = sorted([count[item] for item in kwd_final])
        final_scores_dict = {item:1+(c*4/(len(final_scores)-1)) for c,item in enumerate(final_scores)}
        #add nodes
        for word in kwd_final:
            nodes.append({'label':word,'id':word,'size':final_scores_dict[count[word]]})

        #add edges
        for i in range(len(kwd_final)-1):
            for j in range(i+1,len(kwd_final)):
                w1 = kwd_final[i]
                w2 = kwd_final[j]
                if w1!=w2:
                    edge_score = 2*len(set(kwd_to_urls[w1]) & set(kwd_to_urls[w2]))/(len(set(kwd_to_urls[w1]))+len(set(kwd_to_urls[w2])))
                    if edge_score>0.25:
                        edges.append({'id':w1+w2,'source':w1,'target':w2,'score':10*edge_score})

        #get stock prices
        # ts = TimeSeries(key='DR4TY38ATCKM5LYO')
        # data, metadata = ts.get_intraday(symbol='DJIA', interval='30min')
        # print(data)

        cur.execute('''INSERT INTO public.graphs VALUES (%s,%s)''',(amount,json.dumps({'nodes':nodes,'edges':edges,'articles':urls})))
    print(f'Inserted {len(seconds)} graphs')

def cleanURLs(urls, kwd_final):
    filtered_urls = []
    for d in urls:
        filtered_kwds = [j for j in kwd_final if j in d['keywords']]
        if len(filtered_kwds)==0:
            continue
        d['keywords'] = filtered_kwds
        filtered_urls.append(d)
    return filtered_urls

def getArticleTitleText(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return (article.title, article.text)
    except ArticleException:
        print("URL failed:",url)
        return ('error','error')

def main():
    updateTweetsInDatabase()
    generateGraphs()
    conn.commit()
    cur.close()
    conn.close()
    print("DB changes confirmed")
    return

# def getNetPriceDifference(time):
#     ts = TimeSeries(key='DR4TY38ATCKM5LYO')


if __name__ == '__main__':
    main() 


