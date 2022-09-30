"""
Command line executable allowing to update binary_hashes.json given a CastXML version.
"""

import argparse
from pathlib import Path
import json
import hashlib

def compute_hashes(version, binary_dir):
    hashes = {}
    # (system_id, machine_id)
    binaries = [
        ('linux', '.tar.gz'), # amd64
        ('macosx', '.tar.gz'), # amd64
        ('windows', '.zip'), # amd64
    ]
    for binary in binaries:
        if binary[0] not in hashes:
            hashes[binary[0]] = {}
        hasher = hashlib.sha256()
        with open(Path(binary_dir) / f"v{version}" / f"castxml-{binary[0]}{binary[1]}", 'rb') as fp:
            data = fp.read()
        hasher.update(data)
        hashes[binary[0]][binary[1]] = hasher.hexdigest()
        
    output_file = Path(__file__).resolve().parent / "binary_hashes.json"
    with open(output_file, 'w') as fp:
        json.dump(hashes, fp)

def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        'version', metavar='CASTXML_VERSION', type=str,
        help='CastXML version of the form X.Y.Z'
    )

    parser.add_argument("binary_dir", metavar="BINARY_DIR", type=str, help='Directory containing the castxml binaries in the form f"castxml/v{__version__}/castxml-{system_id}{machine_id}')

    args = parser.parse_args()

    compute_hashes(args.version, args.binary_dir)


if __name__ == "__main__":
    main()
