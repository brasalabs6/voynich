#!/usr/bin/env python3
"""Build a provenance-aware digital reading index from Yale IIIF.

Images are never regenerated, repainted or manipulated: use Yale originals.
Supports IIIF presentation v2 and v3; gracefully retains unzoomable canvases.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import urllib.request

MANIFEST = "https://collections.library.yale.edu/manifests/2002046"
CATALOG = "https://collections.library.yale.edu/catalog/2002046"

def label(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(label(v) for v in value)
    if isinstance(value, dict):
        return label(value.get("en") or value.get("none") or next(iter(value.values()), ""))
    return ""

def url(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return next((v for item in value if (v := url(item))), None)
    if isinstance(value, dict):
        return value.get("id") or value.get("@id")
    return None

def svc(body):
    if isinstance(body, list):
        return next((x for b in body if (x := svc(b))), None)
    if isinstance(body, dict):
        return url(body.get("service")) or svc(body.get("items"))
    return None

def image(canvas):
    for ann in canvas.get("images", []):
        body = ann.get("resource") or {}
        if svc(body) or url(body):
            return svc(body), url(body)
    for group in canvas.get("items", []):
        for ann in group.get("items", []):
            if ann.get("motivation") not in (None, "painting"):
                continue
            body = ann.get("body") or {}
            if svc(body) or url(body):
                return svc(body), url(body)
    return None, None

def normalize(manifest: dict, sha: str, origin: str) -> dict:
    if "sequences" in manifest:
        canvases = (manifest["sequences"] or [{}])[0].get("canvases", [])
        version = "IIIF Presentation v2"
    elif "items" in manifest:
        canvases = manifest["items"]
        version = "IIIF Presentation v3"
    else:
        raise ValueError("Not a IIIF Presentation manifest")
    if not canvases:
        raise ValueError("Manifest contains no canvases")
    output, used = [], set()
    for seq, canvas in enumerate(canvases, 1):
        source_label = label(canvas.get("label")) or ("Imagem digital " + str(seq))
        match = re.search(r"(?<![A-Za-z0-9])f?(\d{1,3}[rv](?:\d+)?)(?![A-Za-z0-9])", source_label, re.I)
        folio = ("f" + match.group(1).lower()) if match else None
        base = folio or "canvas-" + str(seq).zfill(3)
        slug = base if base not in used else base + "-" + str(seq).zfill(3)
        used.add(slug)
        service, source_image = image(canvas)
        service = service.rstrip("/") if service else None
        thumbnail = url(canvas.get("thumbnail")) or (
            service + "/full/!240,350/0/default.jpg" if service else source_image
        )
        output.append({
            "id": slug, "seq": seq, "label": source_label, "folio": folio,
            "canvas": url(canvas), "width": canvas.get("width"),
            "height": canvas.get("height"),
            "image_service": service,
            "image_info": service + "/info.json" if service else None,
            "image_fallback": source_image, "thumbnail": thumbnail,
            "status": "unaltered_Yale_source"
        })
    return {
        "schema": "edition-1.0",
        "title": "Manuscrito Voynich — MS 408",
        "institution": "Yale Beinecke",
        "source": origin,
        "source_sha256": sha,
        "catalog": CATALOG,
        "presentation": version,
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "canvas_count": len(output),
        "zoomable_count": sum(bool(p["image_info"]) for p in output),
        "pages": output
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", help="local JSON source for offline testing")
    p.add_argument("--out", type=Path, default=Path("web/data/folios.json"))
    a = p.parse_args()
    if a.manifest:
        data = Path(a.manifest).read_bytes()
        origin = a.manifest
    else:
        request = urllib.request.Request(MANIFEST, headers={"User-Agent": "BrasALabs-Voynich-Edition/1.0 academic research"})
        with urllib.request.urlopen(request, timeout=120) as resp:
            data = resp.read()
        origin = MANIFEST
    if not 30 < len(data) < 40_000_000:
        raise ValueError("Invalid manifest size")
    result = normalize(json.loads(data), hashlib.sha256(data).hexdigest(), origin)
    if not a.manifest and (result["canvas_count"] < 200 or result["zoomable_count"] < 190):
        raise ValueError("Incomplete Yale manifest or unexpected IIIF schema; do not publish")
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "canvas_count": result["canvas_count"],
        "zoomable_count": result["zoomable_count"],
        "sha256": result["source_sha256"],
        "first": result["pages"][:2]
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
