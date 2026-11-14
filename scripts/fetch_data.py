#!/usr/bin/env python3
"""Fetch scholarly transcriptions and record SHA-256; do not silently replace."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

SOURCES = {
    "ZL3b-n.txt": "https://www.voynich.nu/data/ZL3b-n.txt",
    "IT2a-n.txt": "https://www.voynich.nu/data/IT2a-n.txt",
}


def fetch(out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, url in SOURCES.items():
        path = out / name
        if not path.exists():
            req = urllib.request.Request(url, headers={"User-Agent": "BrasALabs-Voynich-Research/0.1"})
            with urllib.request.urlopen(req, timeout=120) as response:
                raw = response.read()
            if not raw.startswith(b"#=IVTFF"):
                raise ValueError("Unexpected IVTFF input: " + name)
            path.write_bytes(raw)
        raw = path.read_bytes()
        manifest[name] = {"source_url": url, "sha256": hashlib.sha256(raw).hexdigest(),
                          "bytes": len(raw), "header": raw.splitlines()[0].decode("utf-8", "replace")}
    (out / "provenance.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=Path("data/raw"))
    args = p.parse_args()
    print(json.dumps(fetch(args.out), indent=2))

