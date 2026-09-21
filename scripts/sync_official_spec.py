#!/usr/bin/env python3
"""Synchronize released App Defense Alliance CASA material and rebuild generated catalogues.

Uses Python standard library only. The script intentionally follows the latest *published release*
rather than the upstream develop branch. It compares CASA component content, so an unrelated ASA-WG
release does not force a CASA baseline change.
"""
import argparse, hashlib, json, re, sys, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'official/upstream-manifest.json'
CURRENT=ROOT/'official/current'
CATALOG=ROOT/'references/casa-control-catalog.json'
TEST_CASES=ROOT/'references/casa-test-cases.generated.json'
UPSTREAM='appdefensealliance/ASA-WG'
FILES={
  'CASA/CASA Specification.md':'CASA-Specification.md',
  'CASA/CASA Test Guide.md':'CASA-Test-Guide.md',
  'CASA/ADA Burp Audit Scan Configuration.json':'ADA-Burp-Audit-Scan-Configuration.json'
}
UA='casa-readiness-skill/1.0 (+https://github.com/)'

def get(url, accept=None):
    headers={'User-Agent':UA}
    if accept: headers['Accept']=accept
    req=urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(req,timeout=45) as r: return r.read()

def get_json(url): return json.loads(get(url,'application/vnd.github+json').decode())
def sha256(b): return hashlib.sha256(b).hexdigest()

def component_version(text):
    m=re.search(r'^Version\s+([^\s]+)\s*-\s*(\d{4}-\d{2}-\d{2})\s*$',text,re.M)
    if not m: raise ValueError('Unable to parse CASA Version line')
    return m.group(1),m.group(2)

def parse_spec(text):
    lines=text.splitlines(); domain=''; section=''; scope=[]; controls=[]
    for i,line in enumerate(lines):
        if re.match(r'^# \d+\s',line): domain=line[2:].strip()
        if re.match(r'^## \d+\.\d+\s',line): section=line[3:].strip(); scope=[]
        if line.strip()=='### Scope':
            scope=[]; j=i+1
            while j<len(lines) and lines[j].startswith('- '):
                scope.append(lines[j][2:].strip()); j+=1
        m=re.match(r'^\|\s*\[(\d+\.\d+\.\d+)\]\([^)]+\)\s*\|\s*(.*?)\s*\|',line)
        if m:
            controls.append({'id':m.group(1),'domain':domain,'section':section,'scope':list(scope),'description':' '.join(m.group(2).split())})
    if len(controls)<20: raise ValueError(f'Parser found only {len(controls)} controls; upstream format may have changed')
    ids=[c['id'] for c in controls]
    if len(ids)!=len(set(ids)): raise ValueError('Duplicate control IDs detected')
    return controls

def section_text(block,name,next_names):
    if next_names:
        lookahead='|'.join(rf'\*\*{re.escape(n)}\*\*' for n in next_names) + r'|\Z'
    else:
        lookahead=r'\Z'
    p=re.search(rf'\*\*{re.escape(name)}\*\*\s*(.*?)(?=' + lookahead + r')',block,re.S)
    return p.group(1).strip() if p else ''

def split_levels(text):
    if not text: return {'AL1':'','AL2':''}
    m1=re.search(r'\*AL1\*\s*(.*?)(?=\*AL2\*|\Z)',text,re.S)
    m2=re.search(r'\*AL2\*\s*(.*)',text,re.S)
    clean=lambda s:'\n'.join(x.rstrip() for x in s.strip().splitlines()) if s else ''
    return {'AL1':clean(m1.group(1) if m1 else ''),'AL2':clean(m2.group(1) if m2 else '')}

def parse_test_guide(text):
    matches=list(re.finditer(r'^###\s+(\d+\.\d+\.\d+)\s+(.+)$',text,re.M))
    out={}
    for idx,m in enumerate(matches):
        cid=m.group(1); title=m.group(2).strip()
        start=m.end(); end=matches[idx+1].start() if idx+1<len(matches) else len(text)
        block=text[start:end]
        ext=re.search(r'External Reference:\s*(.+)',block)
        evidence=split_levels(section_text(block,'Evidence',['Test Procedure','Verification']))
        procedure=split_levels(section_text(block,'Test Procedure',['Verification']))
        verification=split_levels(section_text(block,'Verification',[]))
        out[cid]={'id':cid,'title':title,'external_reference':ext.group(1).strip() if ext else None,'evidence':evidence,'test_procedure':procedure,'verification':verification}
    if len(out)<20: raise ValueError(f'Test-guide parser found only {len(out)} controls; upstream format may have changed')
    return out

def write_review(old_catalog,new_catalog,old_manifest,new_manifest):
    old={c['id']:c for c in (old_catalog or {}).get('controls',[])}
    new={c['id']:c for c in new_catalog['controls']}
    added=sorted(set(new)-set(old)); removed=sorted(set(old)-set(new)); changed=sorted(k for k in set(old)&set(new) if old[k]!=new[k])
    lines=['# Upstream CASA Change Review','',f"Generated: {datetime.now(timezone.utc).isoformat()}",'',
           f"Previous CASA component: `{(old_manifest or {}).get('casa_component_version','unknown')}`",
           f"New CASA component: `{new_manifest['casa_component_version']}`",'',
           '## Control delta','',f'- Added: {len(added)}',f'- Removed: {len(removed)}',f'- Changed metadata/wording: {len(changed)}','']
    for label,items in [('Added',added),('Removed',removed),('Changed',changed)]:
        if items: lines += [f'### {label}','',', '.join(f'`{x}`' for x in items),'']
    lines += ['## Required maintainer review','',
              '- Review official release notes and CASA file diffs.',
              '- Validate parser output against the official specification and test guide.',
              '- Review scanner/control mappings and reporting language affected by changes.',
              '- Run repository validation and parser tests.',
              '- Merge only after a human confirms the generated baseline is accurate.','']
    (ROOT/'official/UPSTREAM_CHANGE_REVIEW.md').write_text('\n'.join(lines))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--sync',action='store_true'); ap.add_argument('--check',action='store_true'); args=ap.parse_args()
    release=get_json(f'https://api.github.com/repos/{UPSTREAM}/releases/latest')
    tag=release['tag_name']
    blobs={}; contents={}
    for upstream,local in FILES.items():
        api=get_json(f'https://api.github.com/repos/{UPSTREAM}/contents/{urllib.parse.quote(upstream, safe="/")}?ref={urllib.parse.quote(tag)}')
        raw=get(api['download_url'])
        contents[upstream]=raw
        blobs[upstream]={'git_blob_sha':api['sha'],'sha256':sha256(raw),'size':len(raw),'local_file':local}
    spec=contents['CASA/CASA Specification.md'].decode('utf-8')
    guide=contents['CASA/CASA Test Guide.md'].decode('utf-8')
    sv,sd=component_version(spec); gv,gd=component_version(guide)
    if (sv,sd)!=(gv,gd): raise ValueError(f'Spec/test-guide version mismatch: {sv} {sd} vs {gv} {gd}')
    controls=parse_spec(spec); tests=parse_test_guide(guide)
    spec_ids={c['id'] for c in controls}; guide_ids=set(tests)
    if spec_ids!=guide_ids:
        raise ValueError(f'Spec/test-guide control mismatch: only spec={sorted(spec_ids-guide_ids)}, only guide={sorted(guide_ids-spec_ids)}')
    old_manifest=json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    old_catalog=json.loads(CATALOG.read_text()) if CATALOG.exists() else {}
    new_manifest={
      'source_repository':UPSTREAM,
      'source_repository_url':f'https://github.com/{UPSTREAM}',
      'tracking_policy':'latest published GitHub release; compare CASA component files by content hash; human review required before baseline acceptance',
      'last_checked_utc':datetime.now(timezone.utc).isoformat(),
      'latest_repository_release':tag,
      'latest_repository_release_published_at':release.get('published_at'),
      'latest_repository_release_url':release.get('html_url'),
      'casa_component_version':sv,
      'casa_component_date':sd,
      'control_count':len(controls),
      'files':blobs
    }
    changed=any(old_manifest.get('files',{}).get(p,{}).get('git_blob_sha')!=v['git_blob_sha'] for p,v in blobs.items()) or old_manifest.get('casa_component_version')!=sv
    if args.check:
        print(json.dumps({'changed':changed,'release':tag,'casa_component_version':sv,'control_count':len(controls)},indent=2)); return 2 if changed else 0
    if not args.sync:
        print('Use --sync or --check',file=sys.stderr); return 64
    if changed:
        write_review(old_catalog,{'controls':controls},old_manifest,new_manifest)
    CURRENT.mkdir(parents=True,exist_ok=True)
    for upstream,local in FILES.items(): (CURRENT/local).write_bytes(contents[upstream])
    CATALOG.write_text(json.dumps({'source':'App Defense Alliance CASA Specification','source_repository':UPSTREAM,'source_release':tag,'casa_component_version':sv,'casa_component_date':sd,'generated_at':datetime.now(timezone.utc).isoformat(),'controls':controls},indent=2)+'\n')
    TEST_CASES.write_text(json.dumps({'source':'App Defense Alliance CASA Test Guide','source_repository':UPSTREAM,'source_release':tag,'casa_component_version':gv,'generated_at':datetime.now(timezone.utc).isoformat(),'controls':tests},indent=2)+'\n')
    MANIFEST.write_text(json.dumps(new_manifest,indent=2)+'\n')
    print(json.dumps({'changed':changed,'release':tag,'casa_component_version':sv,'control_count':len(controls)},indent=2))
    return 0
if __name__=='__main__':
    try: sys.exit(main() or 0)
    except Exception as e:
        print(f'ERROR: {type(e).__name__}: {e}',file=sys.stderr); sys.exit(1)
