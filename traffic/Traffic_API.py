import requests
import json


class Trafficcheck():
		
	def Trafficimport(self):
		response = requests.get('https://api.tomtom.com/traffic/services/4/incidentDetails/s3/6756997.24100998,415347.49168351,7082349.63287359,811455.63577321/10/-1/json?expandCluster=true&key=FkU4dHE5hoBcQBZFhAG4zrIqFnvVLFvG')
		geladen = response.json()['tm']['poi']
		jasons = []
		incidents = []
		for d in geladen:
			if 'cpoi' not in d:
				jasons.append(d)
			else: 
				jason = d['cpoi']
				jasons.append(jason)
	
		for c in jasons:
			for e in c:
				incident = []
				if not isinstance(e, str):
					if 'f' in e:
						if self.snelwegchecker(e['f']) or self.snelwegchecker(e['t']):
							van = e['f']
							incident.append('from: ' + van)
					if 't' in e:
						if self.snelwegchecker(e['t']) or self.snelwegchecker(e['f']): 
							eind = e['t']
							incident.append('to: ' + eind)
					if 'l' in e and incident:
						len = e['l']
						leng = "length: " + str(len)+'m'
						incident.append(leng)
				if incident:
					stringy = "" + incident[0] + " " + incident[1] + " " + incident[2]
					incidents.append(stringy)
		return incidents
		
	def snelwegchecker(self, obv):
		snelweg = ['A1','A2','A3','A4','A5','A6','A7','A8','A9']
		for weg in snelweg:
			if weg in obv:
				return True
			else:
				return False
