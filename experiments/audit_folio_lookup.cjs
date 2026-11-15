// Deterministic audit; no source images or transcription redistributed.
// node experiments/audit_folio_lookup.cjs
const fs=require('node:fs'); const crypto=require('node:crypto'); const assert=require('node:assert/strict');
function audit(pages){const groups=new Map();for(const p of pages){if(!p.folio)continue;if(!groups.has(p.folio))groups.set(p.folio,[]);groups.get(p.folio).push(p.seq)}return [...groups].filter(([k,v])=>v.length>1).map(([folio,seq])=>({folio,seq,first:seq[0],shadowed:seq.slice(1)}));}
const raw=fs.readFileSync('web/data/folios.json'); const app=fs.readFileSync('web/app.js'); const pages=JSON.parse(raw).pages;
assert.equal(audit([{folio:null,seq:1},{folio:'f1r',seq:2}]).length,0);
assert.deepEqual(audit([{folio:'f1r',seq:1},{folio:'f1r',seq:2}])[0].shadowed,[2]);
const groups=audit(pages); for(const g of groups){assert.equal(pages.find(p=>p.folio===g.folio).seq,g.first);assert.ok(g.seq.every(s=>pages.find(p=>p.seq===s).folio===g.folio));}
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
console.log(JSON.stringify({seed:null,index_sha256:sha(raw),app_sha256:sha(app),selectorPresent:app.toString().includes('page.folio === clean')&&app.toString().includes('p.folio === requested'),count:pages.length,groups},null,2));
