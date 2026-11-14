#!/usr/bin/env python3
"""Validate glyph specimen coordinates and retrieve source-exact IIIF crops.

A crop is a derivative image, never an authoritative glyph identification.
No OCR, no AI restoration, no unreviewed font contours are produced.
Annotations example:
{"specimens":[{"id":"GLYPH-001","page_id":"f1r","line_id":"f1r.1",
"x":120,"y":300,"w":50,"h":80,"candidate":"unknown","reviewers":[]}]}
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

def crop_url(page: dict, sample: dict) -> str:
    service = page.get("image_service")
    if not service:
        raise ValueError("Image service missing for page")
    coords = tuple(sample.get(k) for k in ("x","y","w","h"))
    if any(type(v) is not int for v in coords):
        raise ValueError("Pixel coordinates must be integers")
    x,y,w,h = coords
    if x < 0 or y < 0 or w < 1 or h < 1:
        raise ValueError("Invalid crop rectangle")
    if x+w > page["width"] or y+h > page["height"]:
        raise ValueError("Crop exceeds scan dimensions")
    return service.rstrip("/") + f"/{x},{y},{w},{h}/full/0/default.jpg"

def run(index: Path, annotation_path: Path, folder: Path, dry_run: bool=False):
    edition = json.loads(index.read_text(encoding="utf-8"))
    annotations = json.loads(annotation_path.read_text(encoding="utf-8"))
    pages = {p["id"]:p for p in edition["pages"]}
    result = []
    ids = set()
    folder.mkdir(parents=True, exist_ok=True)
    for sample in annotations.get("specimens", []):
        name = sample["id"]
        if name in ids or not name.replace("-","").isalnum():
            raise ValueError("Duplicate or invalid specimen ID: " + name)
        ids.add(name)
        page = pages[sample["page_id"]]
        url = crop_url(page, sample)
        record = {
            "id": name, "page_id": page["id"], "folio": page["folio"],
            "line_id": sample.get("line_id"),
            "source_canvas": page["canvas"],
            "source_image_service": page["image_service"],
            "source_index_sha256": edition["source_sha256"],
            "region_px": {k:sample[k] for k in ("x","y","w","h")},
            "candidate_unverified": sample.get("candidate","unknown"),
            "reviewers": sample.get("reviewers",[]),
            "status": "unreviewed_sample",
            "iiif_crop_url": url
        }
        if not dry_run:
            req = urllib.request.Request(url,headers={"User-Agent":"BrasALabsVoynichGlyphs/0.1 research"})
            with urllib.request.urlopen(req,timeout=90) as resp:
                data = resp.read()
            if not data.startswith(b"\xff\xd8") or not len(data)>100:
                raise ValueError("IIIF crop is not a valid JPEG: " + name)
            dest = folder / (name+".jpg")
            dest.write_bytes(data)
            record["file"] = dest.name
            record["sha256"] = hashlib.sha256(data).hexdigest()
            record["bytes"] = len(data)
        result.append(record)
    (folder/"glyph-crops-manifest.json").write_text(json.dumps({
        "source":str(index), "annotation_source":str(annotation_path),
        "dry_run":dry_run, "specimens":result},ensure_ascii=False,indent=2)+"\n")
    print("Validated specimens:", len(result), "dry_run:", dry_run)

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--index",type=Path,default=Path("web/data/folios.json"))
    p.add_argument("--annotations",type=Path,required=True)
    p.add_argument("--out",type=Path,default=Path("digital-edition/glyphs/generated"))
    p.add_argument("--dry-run",action="store_true")
    a=p.parse_args()
    run(a.index,a.annotations,a.out,a.dry_run)

