import wikipedia, requests, pendulum, json
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
from nltk.chunk import tree2conlltags


class KeywordExtractor:

	def __init__(self, text):
		if text is not None and len(text)>3:
			self.keyphrase_scores = self.wikipediaNormalizeScore(self.removeSubsets(self.extractKeywords(text[:400])))

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
		return keyphraseScores

	def removeSubsets(self, keywords):
		finalkwds = list(keywords)
		for i in range(len(keywords)-1):
			for j in range(i+1,len(keywords)):
				if keywords[i] in keywords[j]:
					if keywords[i] in finalkwds:
						finalkwds.remove(keywords[i]) 
				elif keywords[j] in keywords[i]:
					if keywords[j] in finalkwds:
						finalkwds.remove(keywords[j])
		return finalkwds


	def getKeyphrases(self):
		try:
			return list(set([phrase for phrase,score in self.keyphrase_scores if score<335]))
		except AttributeError:
			return []



