#!/usr/bin/env python3
"""Refresh EP membership, preserving verified functions by ID. Dry-run by default."""
import argparse,copy,datetime,json,pathlib,urllib.request,xml.etree.ElementTree as ET

def family_name(name):
    words=name.split()
    start=next((i for i,w in enumerate(words) if w.isupper() and any(c.isalpha() for c in w)),len(words)-1)
    return ' '.join(words[start:])

def merge_members(rows,current,label,day):
    previous={str(m['id']):m for m in current};result=[]
    for row in rows:
        if row['politicalGroupLabel']!=label:continue
        uid=str(row['persId']);m=copy.deepcopy(previous.get(uid,{'role':'','headOfDelegation':False,'coordinators':[],'isBureau':False,'strasbourg':'','brussels':''}))
        m.update(id=uid,name=row['fullName'],country=row['countryLabel'],party=row['nationalPoliticalGroupLabel'],lastName=family_name(row['fullName']),membershipCheckedAt=day)
        result.append(m)
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true',help='write members.json after validation');args=parser.parse_args()
    base=pathlib.Path(__file__).resolve().parent;config=json.loads((base/'directory-config.json').read_text());current=json.loads((base/'members.json').read_text())
    req=urllib.request.Request('https://www.europarl.europa.eu/meps/en/full-list/xml',headers={'User-Agent':'ParliamentDirectory/1.0'})
    raw=urllib.request.urlopen(req,timeout=30).read()
    if raw.lstrip().startswith(b'{'):rows=json.loads(raw)['list']
    else:
        root=ET.fromstring(raw);rows=[{c.tag:c.text or '' for c in m} for m in root.iter('mep')]
        for m in rows:
            m['persId']=m.get('persId',m.get('id',''));m['countryLabel']=m.get('countryLabel',m.get('country',''));m['politicalGroupLabel']=m.get('politicalGroupLabel',m.get('politicalGroup',''));m['nationalPoliticalGroupLabel']=m.get('nationalPoliticalGroupLabel',m.get('nationalPoliticalGroup',''))
    day=datetime.datetime.now(datetime.timezone.utc).date().isoformat();updated=merge_members(rows,current,config['groupLabel'],day)
    if not updated or len({m['id'] for m in updated})!=len(updated) or any(not m['id'].isdigit() or not m['name'] or not m['country'] or not m['party'] for m in updated):raise SystemExit('Invalid or empty official response. No file was modified.')
    old={str(m['id']) for m in current};new={m['id'] for m in updated}
    print(f"{config['short']}: {len(current)} -> {len(updated)} members")
    print('Added:',', '.join(m['name'] for m in updated if m['id'] not in old) or 'none');print('Removed:',', '.join(m['name'] for m in current if str(m['id']) not in new) or 'none')
    print('Functions are preserved, not reverified. Upload portraits for new ESN members to photos/<id>.jpg.')
    if args.write:
        target=base/'members.json';temporary=target.with_suffix('.json.tmp');temporary.write_text(json.dumps(updated,ensure_ascii=False,indent=2)+'\n');temporary.replace(target);print('members.json updated locally. Review the changes before committing to GitHub.')
    else:print('Dry-run only. Use --write to update the local file.')
if __name__=='__main__':main()
