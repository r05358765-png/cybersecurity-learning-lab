"""Compare a file with a saved SHA-256 fingerprint (Python 3.8+)."""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def sha256_file(path):
    """Read in chunks so large files do not need to fit in memory."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["baseline", "check"])
    parser.add_argument("file", type=Path)
    parser.add_argument("--baseline", type=Path, default=Path("baseline.json"))
    args = parser.parse_args()
    try:
        target = args.file.resolve()
        if target == args.baseline.resolve():
            raise ValueError("The baseline must be separate from the file being checked.")
        fingerprint = sha256_file(target)
        if args.action == "baseline":
            record = {"algorithm": "sha256", "file": str(target), "digest": fingerprint}
            # Exclusive creation prevents accidentally replacing a trusted baseline.
            with args.baseline.open("x", encoding="utf-8") as output:
                json.dump(record, output, indent=2)
                output.write("\n")
            print("BASELINE SAVED: " + args.baseline.name)
            return 0

        with args.baseline.open(encoding="utf-8") as source:
            record = json.load(source)
        if not isinstance(record, dict):
            raise ValueError("Invalid baseline format.")
        expected = record.get("digest")
        if (record.get("algorithm") != "sha256"
                or not isinstance(expected, str)
                or len(expected) != 64
                or any(c not in "0123456789abcdef" for c in expected)):
            raise ValueError("Invalid SHA-256 baseline.")
        if record.get("file") != str(target):
            raise ValueError("This baseline belongs to a different file.")
        if fingerprint == expected:
            print("UNCHANGED: File matches the saved baseline.")
            return 0
        print("CHANGED: File differs from the saved baseline.")
        return 1
    except (OSError, ValueError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
