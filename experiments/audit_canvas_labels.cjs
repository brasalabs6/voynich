// Issue #7: deterministic label audit only; no IVTFF assertions.
// Run: node experiments/audit_canvas_labels.cjs web/data/folios.json > audit.json
// No random seed (deterministic).
const fs=require("node:fs");
const crypto=require("node:crypto");
function audit(index) {
  const rows = index.pages.map(p => {
    const simple = /^\d+[rv]$/.test(p.label);
    const sides = [...p.label.matchAll(/\b(\d+[rv])\b/g)].map(m => "f"+m[1]);
    return {seq:p.seq, id:p.id, canvas:p.canvas, label:p.label, sides:[...new Set(sides)],
      classification:simple?"single_label_candidate":sides.length?"complex_label_review":"non_folio_view",
      ivtff_verified:false, reviewers:[]};
  });
  const counts = {};
  for (const row of rows) counts[row.classification]=(counts[row.classification]||0)+1;
  const omitted = rows.filter((row,i)=>row.sides.some(s=>s!==index.pages[i].folio)).map(row=>row.seq);
  return {rows,counts,omitted};
}
const assert=(ok,msg)=>{if(!ok)throw Error(msg)};
const tests=()=>{
 const a=audit({pages:[{seq:1,label:"85r (part) 86v (part) (part of 85-86 foldout)",folio:"f85r"},{seq:2,label:"[Spine]",folio:null},{seq:3,label:"1r",folio:"f1r"}]});
 assert(a.rows[0].sides.join(",")==="f85r,f86v","compound");
 assert(a.rows[1].sides.length===0,"nonfolio");
 assert(a.rows[2].classification==="single_label_candidate","simple");
 assert(a.rows.every(r=>!r.ivtff_verified&&r.reviewers.length===0),"review");
 assert(a.omitted.join(",")==="1","omission");
};
tests();
const raw=fs.readFileSync(process.argv[2]);
const index=JSON.parse(raw);
const result=audit(index);
assert(result.rows.length===index.canvas_count,"coverage");
assert(new Set(result.rows.map(r=>r.canvas)).size===result.rows.length,"unique canvas");
assert(result.rows.every((r,i)=>r.seq===i+1),"sequence");
console.log(JSON.stringify({input_sha256:crypto.createHash("sha256").update(raw).digest("hex"),manifest_sha256:index.source_sha256,...result},null,2));
