"""Download the complete original MS408 PDF for publication as a GitHub Release."""
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen, Request

SOURCES = [
 "https://collections.library.yale.edu/pdfs/2002046.pdf",
 "https://archive.org/download/voynich_MS_408/voynich.pdf",
]

def main():
    from pypdf import PdfReader
    folder = Path("manuscript/downloads")
    folder.mkdir(parents=True, exist_ok=True)
    pdf = folder / "MS408-Yale-2002046.pdf"
    failures = []
    for url in SOURCES:
        try:
            req = Request(url, headers={"User-Agent":"BrasALabsVoynichArchive/1.0"})
            with urlopen(req, timeout=240) as response, pdf.open("wb") as dest:
                while True:
                    block = response.read(1024 * 1024)
                    if not block:
                        break
                    dest.write(block)
                    if dest.tell() > 400_000_000:
                        raise ValueError("Unexpectedly large file")
            size = pdf.stat().st_size
            if not 10_000_000 < size < 400_000_000:
                raise ValueError("Unexpected byte count")
            with pdf.open("rb") as stream:
                if stream.read(5) != b"%PDF-":
                    raise ValueError("Missing PDF magic")
            pages = len(PdfReader(str(pdf), strict=False).pages)
            if pages != 214:
                raise ValueError(f"214 PDF pages expected, got {pages}")
            with pdf.open("rb") as stream:
                sha = hashlib.file_digest(stream, "sha256").hexdigest()
            manifest = {
                "title":"Voynich MS 408 — full Yale facsimile",
                "catalog":"https://collections.library.yale.edu/catalog/2002046",
                "source_url_actually_downloaded":url,
                "source_candidates":SOURCES,
                "sha256":sha, "bytes":size, "pdf_pages":pages,
                "filename":pdf.name,
                "notes":"214 PDF pages is not the number of physical folios",
                "failed_previous_candidates":failures,
            }
            (folder/"manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True)+"\n")
            print(json.dumps(manifest,indent=2))
            return
        except Exception as exc:
            failures.append({"url":url,"error":type(exc).__name__+": "+str(exc)})
    raise RuntimeError("No source yielded a valid PDF: "+str(failures))

if __name__ == "__main__":
    main()

