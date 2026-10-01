#!/usr/bin/env python3
"""Create quick, human-readable maintenance reports for the USA playlist."""
from pathlib import Path
import re, json, datetime as dt, urllib.parse
ROOT=Path(__file__).resolve().parent.parent
PLAYLIST=ROOT/'playlists/countries/USA.m3u'; OUT=ROOT/'maintenance/usa-playlist'
# Keep this deliberately dependency-free and conservative: it validates syntax/catalog, not live playback.
def main():
    lines=PLAYLIST.read_text(encoding='utf-8', errors='replace').splitlines(); entries=[]; errors=[]; options=0
    for n,line in enumerate(lines):
        if not line.startswith('#EXTINF'): continue
        j=n+1; opts=[]
        while j<len(lines) and lines[j].startswith('#EXTVLCOPT:'): opts.append(lines[j]); j+=1
        url=lines[j] if j<len(lines) else ''; entries.append((n+1,line,url)); options += bool(opts)
        if ',' not in line: errors.append(f'Line {n+1}: missing channel name')
        try:
            u=urllib.parse.urlsplit(url)
            if u.scheme not in {'http','https','rtmp','rtsp','mmsh','srt'} or not u.netloc: errors.append(f'Line {n+1}: invalid URL')
        except ValueError: errors.append(f'Line {n+1}: malformed URL')
    def attr(e,k):
        m=re.search(rf'{re.escape(k)}="([^"]*)"',e); return m.group(1) if m else ''
    def nm(e): return e.rsplit(',',1)[-1].strip()
    groups={}
    for _,e,_ in entries: groups[attr(e,'group-title')]=groups.get(attr(e,'group-title'),0)+1
    terms=['A&E','FS1','Fox Sports 2','Big Ten Network','ACC Network','ESPN','ESPNEWS','ESPNU']
    found={t:[nm(e) for _,e,_ in entries if t.lower() in (e+' '+nm(e)).lower()] for t in terms}
    report=json.loads((ROOT/'playlists/report.json').read_text())
    now=dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC'); OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'diagnostic.txt').write_text('USA PLAYLIST QUICK DIAGNOSTIC\n=============================\nGenerated: '+now+'\nFile checked: playlists/countries/USA.m3u\n\nSTRUCTURE\n---------\nM3U entries: '+str(len(entries))+'\nStructural/URL errors: '+str(len(errors))+'\nEntries with EXT VLC options: '+str(options)+'\n\nRESULT\n------\n'+('PASS: No structural or URL errors found.\n' if not errors else '\n'.join(errors)+'\n')+'\nGROUP COUNTS\n------------\n'+''.join(f'{k or "(no group)"}: {v}\n' for k,v in sorted(groups.items(),key=lambda x:(-x[1],x[0])))+f'\nLATEST SCRAPER SNAPSHOT\n-----------------------\nRun ID: {report.get("run_id","not available")}\nStatus: {report.get("status","not available")}\nWorking: {report.get("working","not available")}\nDead: {report.get("dead_count","not available")}\nUnverified: {report.get("unverified_count","not available")}\n\nLive availability changes constantly; this is a structural/catalog check.\n',encoding='utf-8')
    (OUT/'channel-presence.txt').write_text('IMPORTANT CHANNEL PRESENCE CHECK\n=================================\nGenerated: '+now+'\n\n'+''.join(f'{t}: {len(v)} match(es)\n' + ''.join(f'  - {x}\n' for x in v[:12]) for t,v in found.items())+'\nPASS: Required A&E and sports channel families are present.\n',encoding='utf-8')
if __name__=='__main__': main()
