// Issue #7/#1: synthetic regression probe of the actual browser parser.
// Run: node experiments/probe_reader_ivtff.cjs
// No seed; synthetic fixtures, not manuscript readings.
const fs = require("node:fs");
const vm = require("node:vm");
const crypto = require("node:crypto");
const assert = require("node:assert/strict");
const raw = fs.readFileSync("web/app.js");
const src = raw.toString("utf8");
assert.match(src, /init\(\);\s*$/);
const document = {getElementById(){return {replaceChildren(){},append(){}}}};
const ctx = vm.createContext({document,setTimeout:()=>0,clearTimeout:()=>{}});
vm.runInContext(src.replace(/init\(\);\s*$/,"") + "\nstate.edition={pages:[{folio:'none'}]};",ctx);
const fixture = " <f1r.1,@P0> abc\n<fRos.1,@P0> def\n<f72v1.2,@P0> ghi\n<f1r.3,@P0> [a:b]\n<f1r.3,@P0> duplicate\n";
ctx.fixture=fixture;
const actual = JSON.parse(vm.runInContext("parseIvTff(fixture,'synthetic'); JSON.stringify([...state.corpus])",ctx));
const map = new Map(actual);
const checks = {rosettes:map.has("fRos"),foldout:map.has("f72v1"),literal:map.get("f1r")?.some(x=>x.raw==="[a:b]"),leadingWhitespace:map.get("f1r")?.some(x=>x.line==="1")||false,duplicateRetained:map.get("f1r")?.filter(x=>x.line==="3").length===2};
console.log(JSON.stringify({source_sha256:crypto.createHash("sha256").update(raw).digest("hex"),fixture_sha256:crypto.createHash("sha256").update(fixture).digest("hex"),seed:null,checks,actual},null,2));
assert.ok(checks.rosettes && checks.foldout && checks.literal && checks.leadingWhitespace,"Parser must retain recognized loci including indented lines");
