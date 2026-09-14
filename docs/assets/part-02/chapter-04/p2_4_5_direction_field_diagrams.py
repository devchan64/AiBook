"""Generate coordinate-based P2-4.5 diagrams in three languages."""
from pathlib import Path
import os
import xml.etree.ElementTree as ET
OUT=Path(__file__).resolve().parent
CACHE=OUT.parents[3]/'.tmp'/'p2-4-5-diagrams';CACHE.mkdir(parents=True,exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR',str(CACHE/'mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
T={
'ko':['증가','감소','상쇄','현재','다음','손실 Q(w)','모든 화살표 = 0.1 × 그래디언트','파라미터 이동'],
'en':['Increase','Decrease','Cancellation','Current','Next','Loss Q(w)','All arrows = 0.1 × gradient','Parameter displacement'],
'zh':['增加','减少','抵消','当前','下一步','损失 Q(w)','所有箭头 = 0.1 × 梯度','参数位移']}

def save(fig,name,lang,desc):
 p=OUT/f'{name}-{lang}.svg';fig.savefig(p,metadata={'Date':None});fig.savefig(CACHE/f'{name}-{lang}.png',dpi=110);plt.close(fig)
 ns='http://www.w3.org/2000/svg';ET.register_namespace('',ns);tree=ET.parse(p);r=tree.getroot();r.set('role','img');r.set('aria-labelledby','title desc')
 for tag,txt in [('title',desc),('desc',desc)]:
  n=ET.Element('{'+ns+'}'+tag,id=tag);n.text=txt;r.insert(0,n)
 tree.write(p,encoding='utf-8',xml_declaration=True);p.write_text('\n'.join(l.rstrip() for l in p.read_text().splitlines())+'\n')

def draw(lang):
 a,b,c,current,nxt,loss,note,move=T[lang]
 names={f.name for f in font_manager.fontManager.ttflist};font=next(n for n in ['Noto Sans CJK KR','Noto Sans CJK JP','DejaVu Sans'] if n in names)
 plt.rcParams.update({'font.family':font,'font.size':13,'axes.unicode_minus':False,'svg.hashsalt':'p2-4-5'})
 fig,ax=plt.subplots(figsize=(7.6,6.1),layout='constrained')
 v=np.linspace(-.5,2.5,301);xx,yy=np.meshgrid(v,v)
 cs=ax.contour(xx,yy,3*xx+4*yy,levels=[2,7,12],colors='#94a3b8');ax.clabel(cs,fmt=lambda z:f'F={z:g}',fontsize=12,manual=[(-.1,.575),(-.1,1.825),(2.3,1.275)])
 for d,col,label,pos in [([.6,.8],'#b91c1c',a,(1.65,1.9)),([-.6,-.8],'#2563eb',b,(-.3,-.25)),([.8,-.6],'#15803d',c,(1.8,.15))]:
  end=np.array([1,1])+d;ax.annotate('',xy=end,xytext=(1,1),arrowprops={'arrowstyle':'->','color':col,'lw':2.5})
  ax.text(*pos,label+'\n'+str(d),color=col,bbox={'facecolor':'white','edgecolor':'none','pad':2})
 ax.scatter(1,1,c='black');ax.text(.5,1.15,'[1, 1]',bbox={'facecolor':'white','edgecolor':'none'})
 ax.set(xlim=(-.4,2.5),ylim=(-.4,2.5),xlabel='x',ylabel='y',aspect='equal');ax.grid(alpha=.2)
 save(fig,'partial-vs-directional-derivative',lang,'F=3x+4y; '+a+' / '+b+' / '+c)
 fig,ax=plt.subplots(figsize=(7.6,6.4),layout='constrained')
 v=np.linspace(-2.5,2.5,301);xx,yy=np.meshgrid(v,v);cs=ax.contour(xx,yy,xx**2+2*yy**2,levels=[1,3,6,10],colors='#93c5fd');ax.clabel(cs,fmt=lambda z:f'L={z:g}',fontsize=12)
 q=np.linspace(-1.5,1.5,7);qx,qy=np.meshgrid(q,q);mask=(qx!=0)|(qy!=0)
 ax.quiver(qx[mask],qy[mask],.2*qx[mask],.4*qy[mask],angles='xy',scale_units='xy',scale=1,color='#b91c1c',width=.004)
 ax.scatter(0,0,c='black',s=18);ax.set(xlim=(-2.3,2.3),ylim=(-2.3,2.3),xlabel='x',ylabel='y',aspect='equal');ax.set_title(note,fontsize=13);ax.grid(alpha=.2)
 save(fig,'vector-calculus-context',lang,'L=x²+2y²; '+note)
 fig,ax=plt.subplots(figsize=(7.6,5.7),layout='constrained')
 w=np.linspace(1.6,4.4,301);ax.plot(w,(w-3)**2,color='#2563eb',lw=2,label='Q(w)=(w−3)²')
 for x,y,col,label,xy in [(4,1,'#111827',current,(3.65,1.3)),(3.8,.64,'#15803d',nxt,(2.9,.72))]:
  ax.scatter(x,y,color=col,zorder=5);ax.plot([x,x],[0,y],':',color=col)
  ax.annotate(label+f' ({x}, {y})',xy=(x,y),xytext=xy,color=col,arrowprops={'arrowstyle':'-','color':col},bbox={'facecolor':'white','edgecolor':'none'})
 ax.annotate('',xy=(3.8,-.15),xytext=(4,-.15),arrowprops={'arrowstyle':'->','color':'#15803d','lw':2})
 ax.text(2.7,-.4,move+' Δw=−0.2',color='#15803d')
 ax.axhline(0,color='#64748b',lw=1);ax.set(xlim=(1.6,4.5),ylim=(-.55,2.2),xlabel='w',ylabel=loss)
 ax.legend(loc='upper center');ax.grid(alpha=.2)
 save(fig,'gradient-descent-update-intuition',lang,move+' Δw=−0.2; ΔQ=−0.36')

if __name__=='__main__':
 for language in T:draw(language)
