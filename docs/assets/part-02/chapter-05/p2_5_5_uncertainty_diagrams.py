"""Reproducible population/mean distributions and repeated t intervals."""
from pathlib import Path
import os
import xml.etree.ElementTree as ET
OUT=Path(__file__).resolve().parent
CACHE=OUT.parents[3]/'.tmp'/'p2-5-5-diagrams'
CACHE.mkdir(parents=True,exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR',str(CACHE/'mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
from scipy.stats import norm,t
LABELS={
 'ko':['개별 응답 시간','표본평균 (n=100)','확률밀도','시간 (초)','표준편차 = 10초','표준오차 = 1초','표본 번호','평균 추정값 (초)','포함','미포함','모집단 평균 = 50초'],
 'en':['Individual response times','Sample means (n=100)','Density','Time (seconds)','SD = 10 seconds','SE = 1 second','Sample number','Estimated mean (seconds)','Covers','Misses','Population mean = 50 seconds'],
 'zh':['单次响应时间','样本均值 (n=100)','概率密度','时间（秒）','标准差 = 10秒','标准误 = 1秒','样本编号','均值估计值（秒）','包含','未包含','总体均值 = 50秒']}

def save(fig,name,lang,title,desc):
 path=OUT/f'{name}-{lang}.svg'
 fig.savefig(path,metadata={'Date':None})
 fig.savefig(CACHE/f'{name}-{lang}.png',dpi=110)
 plt.close(fig)
 ns='http://www.w3.org/2000/svg';ET.register_namespace('',ns)
 tree=ET.parse(path);root=tree.getroot()
 root.set('role','img');root.set('aria-labelledby','title desc')
 for tag,value in [('title',title),('desc',desc)]:
  el=ET.Element('{'+ns+'}'+tag,id=tag);el.text=value;root.insert(0,el)
 tree.write(path,encoding='utf-8',xml_declaration=True)
 path.write_text('\n'.join(l.rstrip() for l in path.read_text().splitlines())+'\n')

def draw(lang,samples):
 labels=LABELS[lang]
 fonts={f.name for f in font_manager.fontManager.ttflist}
 font=next(n for n in ['Noto Sans CJK KR','Noto Sans CJK JP','DejaVu Sans'] if n in fonts)
 plt.rcParams.update({'font.family':font,'font.size':13,'svg.hashsalt':'p2-5-5','axes.unicode_minus':False})
 x=np.linspace(15,85,1401)
 fig,axes=plt.subplots(2,1,figsize=(8,6.4),layout='constrained',sharex=True)
 for i,(ax,sd) in enumerate(zip(axes,[10,1])):
  ax.plot(x,norm.pdf(x,50,sd),color='#2563eb',lw=2)
  ax.axvline(50,color='#64748b',ls='--',lw=1)
  ax.axvspan(50-sd,50+sd,color='#2563eb',alpha=.12)
  ax.set_title(labels[i],fontsize=15,loc='left')
  ax.text(.97,.83,labels[4+i],transform=ax.transAxes,ha='right')
  ax.set_ylabel(labels[2]);ax.set_ylim(bottom=0)
  ax.grid(alpha=.2);ax.set_xlim(15,85)
 axes[-1].set_xlabel(labels[3])
 save(fig,'sd-se-comparison',lang,labels[0]+' / '+labels[1],labels[4]+'; '+labels[5])
 means=samples.mean(axis=1);width=t.ppf(.975,99)*samples.std(axis=1,ddof=1)/10
 covered=(means-width<=50)&(means+width>=50)
 fig,ax=plt.subplots(figsize=(8,7.5),layout='constrained')
 seen=set()
 for i,(m,h,c) in enumerate(zip(means,width,covered),1):
  color='#2563eb' if c else '#b91c1c'
  label=labels[8] if c else labels[9]
  ax.plot([m-h,m+h],[i,i],color=color,ls='-' if c else '--',lw=2,
          label=label if label not in seen else None)
  ax.plot(m,i,'o' if c else 'x',color=color,ms=5);seen.add(label)
 ax.axvline(50,color='#334155',ls='--',label=labels[10])
 ax.set(xlabel=labels[7],ylabel=labels[6],ylim=(20.7,.3))
 ax.set_yticks(range(1,21));ax.grid(alpha=.2)
 ax.legend(loc='upper center',bbox_to_anchor=(.5,1.13),fontsize=11,ncol=2)
 save(fig,'repeated-confidence-intervals',lang,labels[10],f'n=100; 20; 95%; {labels[8]}: {covered.sum()}/20')
 return int(covered.sum())

if __name__=='__main__':
 samples=np.random.default_rng(20260915).normal(50,10,size=(20,100))
 for lang in LABELS:
  print(lang,'coverage:',draw(lang,samples),'/20')
