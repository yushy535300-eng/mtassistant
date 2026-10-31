(function websiteScript(){
  "use strict";
  const byId = id => document.getElementById(id);
  // Demonstration only; never imply these are actual provider outcomes.
  const samples=[
    "BPBBPPBPPPBBBPPBPBBBPBBPPPBPPBBBPBPPBP",
    "PBBPPPPBPPBBBPBBBPBBPPPBBPPBBPBBPPBPP",
    "BBBPBBPPBBPPPPBBBPBPBBPBBPPPPBBPPBBB"
  ].map(s=>s.split(""));
  function makeDot(kind,bead=false){
    if(bead)return `<span class="cell"><i class="${kind.toLowerCase()}">${kind==="B"?"莊":kind==="P"?"閒":"和"}</i></span>`;
    return `<span class="cell"><i class="road-dot ${kind.toLowerCase()}"></i></span>`;
  }
  function drawBeads(element,sample){
    if(!element)return;
    element.innerHTML=Array.from({length:36},(_,i)=>sample[i]?makeDot(sample[i],true):'<span class="cell"></span>').join("");
  }
  function drawRoad(element,sample,colsCount=15){
    if(!element)return;
    const cols=Array.from({length:colsCount},()=>Array(6).fill(null));
    let col=-1,row=0,last="";
    for(const kind of sample){
      if(kind==="T")continue;
      if(kind!==last){col++;row=0;last=kind}
      else row++;
      if(col>=colsCount)break;
      if(row<6)cols[col][row]=kind;
    }
    element.innerHTML=cols.flat().map(kind=>kind?makeDot(kind):'<span class="cell"></span>').join("");
  }
  function drawLower(element,sample){
    if(!element)return;
    element.innerHTML=Array.from({length:3},(_,group)=>{
      const outcomes=sample.slice(group*3+2,group*3+32);
      return `<div aria-hidden="true">${Array.from({length:30},(_,i)=>{
        const kind=outcomes[i];
        return kind?makeDot(i%5===4?(kind==="B"?"P":"B"):kind):'<span class="cell"></span>';
      }).join("")}</div>`;
    }).join("");
  }
  drawBeads(byId("heroBead"),samples[0]);
  drawRoad(byId("heroRoad"),samples[0]);
  drawRoad(byId("productRoad"),samples[1]);
  function selectDemo(index){
    const sample=samples[index]||samples[0];
    drawBeads(byId("deepBead"),sample);
    drawRoad(byId("deepRoad"),sample);
    drawLower(byId("deepLower"),sample);
    document.querySelectorAll("[data-table]").forEach(button=>{
      const active=Number(button.getAttribute("data-table"))===index;
      button.classList.toggle("active",active);
      button.setAttribute("aria-pressed",String(active));
    });
  }
  document.querySelectorAll("[data-table]").forEach(button=>button.addEventListener("click",()=>{
    selectDemo(Number(button.getAttribute("data-table"))||0);
  }));
  selectDemo(0);
  const menu=byId("menuButton"),nav=byId("nav");
  function closeMenu(){
    nav?.classList.remove("is-open");
    menu?.setAttribute("aria-expanded","false");
  }
  if(menu&&nav){
    menu.addEventListener("click",()=>{
      const opening=!nav.classList.contains("is-open");
      nav.classList.toggle("is-open",opening);
      menu.setAttribute("aria-expanded",String(opening));
    });
    nav.querySelectorAll("a").forEach(a=>a.addEventListener("click",closeMenu));
    window.addEventListener("keydown",e=>{if(e.key==="Escape")closeMenu()});
    window.addEventListener("resize",()=>{if(window.innerWidth>960)closeMenu()},{passive:true});
  }
  if("IntersectionObserver" in window){
    const links=[...document.querySelectorAll(".nav a[href^='#']")];
    const observer=new IntersectionObserver(entries=>{
      const target=entries.filter(entry=>entry.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio)[0];
      if(!target)return;
      for(const link of links)link.classList.toggle("nav-active",link.hash==="#"+target.target.id);
    },{rootMargin:"-15% 0px -55% 0px",threshold:[0,.1,.3,.6]});
    for(const id of ["home","systems","live-preview","how-it-works","questions"]){
      const target=byId(id);
      if(target)observer.observe(target);
    }
  }
})();