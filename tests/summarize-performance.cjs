const fs=require('fs');const r=JSON.parse(fs.readFileSync('artifacts/lighthouse-mobile.json','utf8'));
const scores=Object.fromEntries(Object.entries(r.categories).map(([k,v])=>[k,Math.round(v.score*100)]));
const metrics=Object.fromEntries(['first-contentful-paint','largest-contentful-paint','total-blocking-time','cumulative-layout-shift','speed-index'].map(k=>[k,{value:r.audits[k]?.numericValue,unit:r.audits[k]?.numericUnit,display:r.audits[k]?.displayValue}]));
const output={kind:'Lighthouse laboratory measurement, not real-user Core Web Vitals',fetchTime:r.fetchTime,requestedUrl:r.requestedUrl,scores,metrics,warnings:r.runWarnings};fs.writeFileSync('artifacts/performance-summary.json',JSON.stringify(output,null,2));console.log(JSON.stringify(output,null,2));
