#!/usr/bin/env python3
"""Diagnóstico no destructivo de encabezados y pies de las 23 páginas."""
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

BASE=Path(__file__).resolve().parent/"target-site"
CATS=["inclusion-accesibilidad","bienestar-personal","desarrollo-espiritual","educacion-aprendizaje"]
APPS={"inclusion-accesibilidad":["brailux","rutinago","comunicago"],"bienestar-personal":["motiva"],"desarrollo-espiritual":["quizbible","mimomento"],"educacion-aprendizaje":["englishfast","crucilux","sudolux"]}
PAGES=[("matriz","index.html")]
PAGES += [("categoria",f"{c}/index.html") for c in CATS]
PAGES += [("aplicacion",f"{c}/{a}/index.html") for c,apps in APPS.items() for a in apps]
PAGES += [("privacidad",f"privacy/{a}/index.html") for apps in APPS.values() for a in apps]
class Reader(HTMLParser):
 def __init__(self):
  super().__init__();self.stack=[];self.headers=[];self.footers=[];self.mains=0;self.navs=0;self.links=[];self.headings=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in ("header","footer"): (self.headers if tag=="header" else self.footers).append({"class":a.get("class",""),"id":a.get("id","")})
  if tag=="main":self.mains+=1
  if tag=="nav":self.navs+=1
  if tag=="h1":self.headings+=1
  if tag=="a":self.links.append(a.get("href",""))
def main():
 out=[];findings=[]
 for group,path in PAGES:
  filename=BASE/path
  if not filename.exists():
   findings.append({"path":path,"finding":"archivo ausente","level":"error"});continue
  parser=Reader();parser.feed(filename.read_text(encoding="utf-8",errors="replace"))
  record={"page":path,"group":group,"header":parser.headers,"footer":parser.footers,"main_count":parser.mains,"h1_count":parser.headings,"nav_count":parser.navs,"local_links":sum(not x.startswith(("https:","http:","mailto:","#")) for x in parser.links)}
  out.append(record)
  for tag,count in (("header",len(parser.headers)),("footer",len(parser.footers)),("main",parser.mains)):
   if count!=1:findings.append({"path":path,"finding":f"{tag}: {count} (referencia esperada: 1)","level":"review"})
  if parser.headings!=1:findings.append({"path":path,"finding":f"h1: {parser.headings}","level":"review"})
 classes=lambda item,key:Counter(" ".join(x[key] for x in item.get("header" if key=="class" else "footer",[])) for item in out)
 report={"pages":out,"findings":findings,"summary":{"inspected":len(out),"expected":len(PAGES),"observations":len(findings),"by_group":dict(Counter(x["group"] for x in out))},"limits":"Auditoría HTML; no demuestra dimensiones, contraste, reflujo, foco ni equivalencia visual"}
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
