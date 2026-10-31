import json,urllib.request,os,math
from datetime import date,timedelta
from xml.sax.saxutils import escape
ROOT=os.path.dirname(__file__)
USER='Ais-KSA'
# GitHub public contribution calendar via GitHub GraphQL when token is provided.
def counts():
 token=os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
 if not token:return None
 query='query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}'
 req=urllib.request.Request('https://api.github.com/graphql',data=json.dumps({'query':query,'variables':{'login':USER}}).encode(),headers={'Authorization':'Bearer '+token,'Content-Type':'application/json','User-Agent':'ChemistryReaction'})
 try:
  with urllib.request.urlopen(req,timeout=20) as resp: data=json.load(resp)
  weeks=data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
  return {d['date']:d['contributionCount'] for w in weeks for d in w['contributionDays']}
 except Exception as e:
  print('Contribution fetch unavailable:',e)
  return None

def generate():
 data=counts()
 if data is None:
  # Decorative grid when run locally without credentials; not fabricated activity.
  data={}
 today=date.today();start=today-timedelta(days=364);start-=timedelta(days=(start.weekday()+1)%7)
 W,H=920,275
 out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
 '<title id="title">AIS Chemistry Reaction</title>', '<desc id="desc">Animated chemistry-inspired contribution grid, with atoms bonding and a traveling reaction wave.</desc>',
 '<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#080D0B"/><stop offset="1" stop-color="#151B1A"/></linearGradient><filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="4"/></filter></defs>',
 '<rect width="920" height="275" rx="16" fill="url(#bg)"/>',
 '<rect x="1" y="1" width="918" height="273" rx="15" fill="none" stroke="#344C3F"/>',
 '<text x="30" y="36" fill="#D6DFD2" font-family="monospace" font-size="18" font-weight="bold">CHEMISTRY REACTION</text>',
 '<text x="890" y="35" text-anchor="end" fill="#9BB3A1" font-family="monospace" font-size="11">AIS / LAB 01</text>',
 '<text x="30" y="57" fill="#819988" font-family="monospace" font-size="11">ATOMS  +  BONDS  →  DISCOVERY</text>']
 colors=['#202B26','#344C3F','#4C7159','#6F9B77','#9BB3A1']
 for col in range(53):
  for row in range(7):
   d=start+timedelta(days=col*7+row)
   if d>today:continue
   n=data.get(d,0)
   level=0 if n==0 else min(4,1+int(math.log2(n+1)))
   x=30+col*16;y=78+row*16
   out.append(f'<rect x="{x}" y="{y}" width="11" height="11" rx="2" fill="{colors[level]}"/>')
 # Reaction sweep and orbiting atom pair, SMIL compatible with SVG images in GitHub.
 out += ['<g opacity="0.8"><rect x="30" y="78" width="5" height="107" rx="2" fill="#9BB3A1" opacity="0.4" filter="url(#glow)"><animate attributeName="x" values="30;870;30" dur="12s" repeatCount="indefinite"/></rect><rect x="30" y="78" width="2" height="107" fill="#9BB3A1" opacity="0.8"><animate attributeName="x" values="30;870;30" dur="12s" repeatCount="indefinite"/></rect></g>',
 '<g><animateTransform attributeName="transform" type="translate" values="0 0;230 0;460 0;690 0;0 0" dur="12s" repeatCount="indefinite"/><line x1="65" y1="210" x2="100" y2="210" stroke="#9BB3A1" stroke-width="4" stroke-linecap="round"><animate attributeName="x2" values="100;85;100" dur="2s" repeatCount="indefinite"/></line><circle cx="65" cy="210" r="13" fill="#344C3F" stroke="#9BB3A1" stroke-width="2"/><circle cx="100" cy="210" r="10" fill="#819988" stroke="#D6DFD2" stroke-width="2"><animate attributeName="cx" values="100;85;100" dur="2s" repeatCount="indefinite"/></circle><circle cx="65" cy="210" r="20" fill="none" stroke="#9BB3A1" opacity="0.4"><animate attributeName="r" values="16;28;16" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.5;0;0.5" dur="2s" repeatCount="indefinite"/></circle></g>',
 '<text x="30" y="255" fill="#819988" font-family="monospace" font-size="11">REACTION IN PROGRESS</text>',
 '<text x="890" y="255" text-anchor="end" fill="#D6DFD2" font-family="monospace" font-size="11">CHEMISTRY × CODE</text>', '</svg>']
 path=os.path.join(ROOT,'assets','chemistry-reaction.svg')
 with open(path,'w',encoding='utf8') as f:f.write('\n'.join(out))
 print('Wrote',path,'with', 'real contribution data' if data is not None else 'decorative fallback')
if __name__=='__main__':generate()
