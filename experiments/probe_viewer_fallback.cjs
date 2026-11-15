// deterministic mock-DOM contract, not a browser or network test.
function probe(src) {
 const nodes = new Map(), warnings=[], viewers=[];
 const make = tag => ({tag,children:[],append(...xs){this.children.push(...xs)},replaceChildren(){this.children=[]}});
 const document={createElement:make,getElementById(id){if(!nodes.has(id))nodes.set(id,make(id));return nodes.get(id)}};
 const window={}; const console={warn(...x){warnings.push(x)}};
 const api=new Function("document","window","console",src.replace(/init\(\);\s*$/,"")+"\nreturn {state,createViewer};")(document,window,console);
 const a={folio:"f1r",label:"a",image_info:"https://example.invalid/a/info.json",image_fallback:"https://example.invalid/a.jpg"};
 const b={folio:"f2r",label:"b",image_info:"https://example.invalid/b/info.json",thumbnail:"https://example.invalid/b.jpg"};
 const checks={};
 const image=()=>nodes.get("viewer").children[0]?.children[0]?.src;
 api.createViewer(a); checks.noLibrary=image()===a.image_fallback;
 api.createViewer(b); checks.thumbnail=image()===b.thumbnail;
 api.createViewer({label:"empty"}); checks.noImage=nodes.get("viewer").children[0]?.children[0]?.tag==="p";
 window.OpenSeadragon=()=>{throw Error("synthetic constructor failure")};
 api.createViewer(a); checks.constructorFailure=image()===a.image_fallback;
 window.OpenSeadragon=()=>{const v={events:{},destroyed:0,addHandler(n,fn){this.events[n]=fn},destroy(){this.destroyed++}};viewers.push(v);return v};
 api.createViewer(a); const old=viewers.at(-1);
 api.createViewer(b); const current=viewers.at(-1);
 old.events["open-failed"]({message:"stale"}); checks.staleIgnored=api.state.viewer===current && image()===undefined && old.destroyed===1;
 current.events["open-failed"]({message:"current"}); checks.currentFallback=api.state.viewer===null && image()===b.thumbnail && current.destroyed===1;
 api.createViewer(a); const tile=viewers.at(-1);
 checks.tileFailureHandler=typeof tile.events["tile-load-failed"]==="function";
 return checks;
}
// Observed on source blob fc71af007221e2ef4c31e4e95bfabc41e1b7c5b2, commit 94b2f033100f007cd2a94a3b33dd543579e81a0f.
// Runtime: V8, mock DOM. Seed: null. No network. Synthetic URLs only.
// Observed checks: {"noLibrary":true,"thumbnail":true,"noImage":true,"constructorFailure":true,"staleIgnored":true,"currentFallback":true,"tileFailureHandler":false}
// Negative observation: lack of tile-load-failed handler is not proof of a browser failure.
if(typeof require!=="undefined" && require.main===module){
 const fs=require("node:fs"),crypto=require("node:crypto"),assert=require("node:assert/strict");
 const raw=fs.readFileSync("web/app.js"); const checks=probe(raw.toString("utf8"));
 console.log(JSON.stringify({source_sha256:crypto.createHash("sha256").update(raw).digest("hex"),seed:null,checks},null,2));
 for(const [k,v] of Object.entries(checks)) if(k!=="tileFailureHandler") assert.equal(v,true,k);
}
