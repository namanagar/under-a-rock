from newsplease import NewsPlease
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
from nltk.chunk import tree2conlltags
import wikipedia, requests, pendulum, json

class KeywordFinder:

	def __init__(self, url):
		self.url = url
		try:
			article = NewsPlease.from_url(self.url)
			self.lede = article.description
			self.title = article.title
			self.og_dict = {}
			keywords = self.extractKeywords(self.lede) if self.lede is not None else []
			self.keyphrase_scores = self.wikipediaNormalizeScore(keywords)
		except:
			self.keyphrase_scores = None
			self.og_dict = None

	def extractKeywords(self, text):
		keywords = []
		#print(text)
		for sentence in sent_tokenize(text):
			live = []
			for name, pos, entity in tree2conlltags(ne_chunk(pos_tag(word_tokenize(sentence)))):
				if entity=='O':
					if len(live)>0:
						keywords.append(" ".join(live))
						live = []
				else:
					live.append(name)
			if len(live)>0:
				keywords.append(" ".join(live))
		return keywords

	def wikipediaNormalizeScore(self, keyphrases):
		keyphraseScores = []
		now = pendulum.now('UTC')
		for phrase in keyphrases:
			if wikipedia.search(phrase):
				title = wikipedia.search(phrase)[0]
				resp = requests.get('http://en.wikipedia.org/w/api.php',params = {'action':'query', 'prop':'revisions','rvprop':'timestamp','rvlimit':10, 'format':'json','titles':title})
				if resp.status_code == 200:
					for d in list(json.loads(json.dumps(resp.json()))['query']['pages'].values()):
						final_title = str(title.split(" (")[0])
						score = 0
						for i,d2 in enumerate(d['revisions']):
							score+=(((1/2)**i)*(pendulum.parse(d2['timestamp']).diff(now).in_hours()))
						keyphraseScores.append((final_title,score))
						self.og_dict[final_title] = phrase
		return keyphraseScores

	def getKeyphrases(self):
		if self.keyphrase_scores:
			return list(set([phrase for phrase,score in self.keyphrase_scores if score<335]))
		else:
			return []

	def getOriginalDict(self):
		if self.og_dict:
			return self.og_dict
		else:
			return {}



