#!/usr/bin/env python3
"""Fase 2: inventario comparativo no destructivo de identidad y accesibilidad."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import json
ROOT=Path(__file__).resolve().parent/"target-site"
GROUPS={
 "matriz":["index.html"],
 "categorias":["inclusion-accesibilidad/index.html","bienestar-personal/index.html","desarrollo-espiritual/index.html","educacion-aprendizaje/index.html"],
 "aplicaciones":["inclusion-accesibilidad/brailux/index.html","inclusion-accesibilidad/rutinago/index.html","inclusion-accesibilidad/comunicago/index.html","bienestar-personal/motiva/index.html","desarrollo-espiritual/quizbible/index.html","desarrollo-espiritual/mimomento/index.html","educacion-aprendizaje/englishfast/index.html","educacion-aprendizaje/crucilux/index.html","educacion-aprendizaje/sudolux/index.html"],
 "privacidad":["privacy/"+app+"/index.html" for app in ("brailux","rutinago","comunicago","motiva","quizbible","mimomento","englishfast","crucilux","sudolux")]}
class Inspector(HTMLParser):
 def __init__(self):
  super().__init__();self.tags=Counter();self.css=[];self.nav=0;self.skip=False;self.lang="";self.viewport=False;self.buttons=0;self.unlabeled_buttons=0;self.images=0;self.images_without_alt=0;self.icons=0;self.main_ids=set();self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags[tag]+=1
  if tag=="html":self.lang=a.get("lang","")
  if tag=="meta" and a.get("name")=="viewport":self.viewport=True
  if tag=="link" and a.get("rel")=="stylesheet":self.css.append(a.get("href",""))
  if tag=="nav":self.nav+=1
  if tag=="button":
   self.buttons+=1
   if not a.get("aria-label") and not a.get("title"):self.unlabeled_buttons+=1 # Heurística: puede tener texto o icono accesible
  if tag=="img":
   self.images+=1
   if "alt" not in a:self.images_without_alt+=1
  if a.get("id"):self.main_ids.add(a["id"])
  if tag=="a":
   href=a.get("href","");self.links.append(href)
   if href.startswith("#") and any(k in href.lower() for k in ("contenido","main","principal")):self.skip=True
def main():
 records=[];findings=[]
 for group,paths in GROUPS.items():
  for path in paths:
   file=ROOT/path
   if not file.is_file():
    findings.append({"level":"error","path":path,"rule":"file_missing"});continue
   i=Inspector();i.feed(file.read_text(encoding="utf-8",errors="replace"))
   row={"path":path,"group":group,"lang":i.lang,"header":i.tags["header"],"main":i.tags["main"],"footer":i.tags["footer"],"nav":i.nav,"h1":i.tags["h1"],"skip_link_heuristic":i.skip,"viewport":i.viewport,"stylesheets":i.css,"images_without_alt":i.images_without_alt,"buttons_without_aria_label_or_title_heuristic":i.unlabeled_buttons}
   records.append(row)
   for rule,bad in (("lang_missing",not i.lang),("viewport_missing",not i.viewport),("header_missing",not i.tags["header"]),("main_missing",not i.tags["main"]),("footer_missing",not i.tags["footer"]),("h1_count_not_one",i.tags["h1"]!=1),("skip_link_not_found",not i.skip),("img_alt_missing",i.images_without_alt>0)):
    if bad:findings.append({"level":"review","path":path,"rule":rule})
 summary={"pages_inspected":len(records),"group_counts":dict(Counter(r["group"] for r in records)),"review_findings":len(findings),"scope":"Heurística HTML estática; no mide contraste, reflujo visual ni navegación real por teclado"}
 print(json.dumps({"summary":summary,"pages":records,"findings":findings},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
