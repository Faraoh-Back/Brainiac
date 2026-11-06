#!/usr/bin/env python3
"""Prepare n8n workflow exports for human review. Does not certify all text/code."""
import argparse
import copy
import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

SENSITIVE=re.compile(r'^(authorization|proxy-authorization|x-api-key|apikey|api_key|api-key|password|passwd|secret|client_secret|access_token|refresh_token|token|appid)$',re.I)
REMOVED='CONFIGURAR_EM_CREDENCIAL_N8N'

def scrub(value):
    if isinstance(value,list):
        return [scrub(v) for v in value]
    if not isinstance(value,dict):
        return value
    result={}
    for k,v in value.items():
        if SENSITIVE.fullmatch(k) and isinstance(v,str):
            result[k]=REMOVED
        elif k=='url' and isinstance(v,str) and v.startswith(('http://','https://')):
            u=urlsplit(v)
            if u.username or u.password:
                raise ValueError('URL com credencial embutida: mova-a para credencial n8n antes de exportar.')
            if any(SENSITIVE.fullmatch(name) for name,_ in parse_qsl(u.query,keep_blank_values=True)):
                query=urlencode([(name,REMOVED if SENSITIVE.fullmatch(name) else val) for name,val in parse_qsl(u.query,keep_blank_values=True)])
                result[k]=urlunsplit((u.scheme,u.netloc,u.path,query,u.fragment))
            else: result[k]=v
        else:
            result[k]=scrub(v)
    if isinstance(value.get('name'),str) and SENSITIVE.fullmatch(value['name']):
        if 'value' in result: result['value']=REMOVED
    return result

def sanitize(workflow):
    if not isinstance(workflow,dict) or not isinstance(workflow.get('nodes'),list):
        raise ValueError('Esperado workflow n8n; não processe exports de credenciais com este script.')
    wf=scrub(copy.deepcopy(workflow))
    for k in ['pinData','staticData','meta','shared','tags','versionId','activeVersionId','activeVersion','versionMetadata']:
        wf.pop(k,None)
    wf['pinData']={}
    wf['active']=False
    return wf

def public_template(workflow):
    """Remove known personal configuration in addition to explicit secrets."""
    wf=sanitize(workflow)
    wf.pop('id',None)
    for node in wf['nodes']:
        node.pop('credentials',None)
        node.pop('webhookId',None)
        p=node.get('parameters',{})
        if isinstance(p.get('calendar'),dict):
            p['calendar']={'__rl':True,'value':'primary','mode':'id'}
        if isinstance(p.get('documentId'),dict):
            p['documentId']={'__rl':True,'value':'CONFIGURAR_PLANILHA_ID','mode':'id'}
        if isinstance(p.get('sheetName'),dict) and p['sheetName'].get('cachedResultName'):
            p['sheetName']={'__rl':True,'value':p['sheetName']['cachedResultName'],'mode':'name'}
        if 'googleTasks' in node.get('type','') and isinstance(p.get('task'),str) and not p['task'].startswith('='):
            p['task']='CONFIGURAR_LISTA_'+re.sub(r'[^A-Z0-9]+','_',node['name'].upper()).strip('_')
        if isinstance(p.get('jsCode'),str):
            p['jsCode']=re.sub(r'fallbackIds:\s*\{[^{}]*\}', 'fallbackIds: {}', p['jsCode'])
    def redact(value):
        if isinstance(value,dict):return {k:redact(v) for k,v in value.items() if not k.startswith('cachedResult')}
        if isinstance(value,list):return [redact(v) for v in value]
        if not isinstance(value,str):return value
        value=re.sub(r'(?<!\d)55\d{10,11}(?!\d)','CONFIGURAR_NUMERO_WHATSAPP',value)
        value=re.sub(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', 'usuario@example.com',value)
        value=value.replace('evolution.ghunicamp.com.br','evolution.example.com').replace('n8n.ghunicamp.com.br','n8n.example.com')
        return value
    return redact(wf)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--public',action='store_true',help='Também remove configurações pessoais conhecidas para template público')
    args=parser.parse_args()
    data=json.loads(args.input.read_text())
    workflows=data if isinstance(data,list) else [data]
    prepared=[public_template(w) if args.public else sanitize(w) for w in workflows]
    args.output.mkdir(parents=True,exist_ok=True)
    for i,w in enumerate(prepared):
        name=re.sub(r'[^a-zA-Z0-9_-]+','-',str(w.get('name','workflow'))).strip('-')[:100] or 'workflow'
        ident=re.sub(r'[^a-zA-Z0-9_-]+','-',str(w.get('id',i)))[:80]
        (args.output/f'{name}-{ident}.json').write_text(json.dumps(w,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(prepared)} workflow(s) preparado(s). Revise código, URLs, textos e dados pessoais antes do commit.')

if __name__=='__main__':
    main()
