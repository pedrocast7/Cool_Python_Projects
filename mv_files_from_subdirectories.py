import argparse
import shutil
from pathlib import Path

"""
mv_files.py

Move every non-JSON file from each subdirectory of INPUT_DIR into a
corresponding subdirectory (same name) under OUTPUT_DIR. Create the
destination subdirectory if it doesn't exist. Immediate subdirectories only.
"""

def move_non_json(input_dir: Path, output_dir: Path):
    if not input_dir.exists() or not input_dir.is_dir():
        raise SystemExit(f"Input path does not exist or is not a directory: {input_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    for sub in input_dir.iterdir():
        if not sub.is_dir():
            continue  # skip files in the top-level input_dir
        dest_sub = output_dir / sub.name
        dest_sub.mkdir(parents=True, exist_ok=True)

        for item in sub.iterdir():
            if not item.is_file():
                continue
            if item.suffix.lower() == ".json":
                continue

            dest = dest_sub / item.name
            if dest.exists():
                # avoid overwrite: append numeric suffix before extension
                stem, suf = item.stem, item.suffix
                counter = 1
                while True:
                    new_name = f"{stem}_{counter}{suf}"
                    dest = dest_sub / new_name
                    if not dest.exists():
                        break
                    counter += 1

            shutil.move(str(item), str(dest))
            print(f"Moved: {item} -> {dest}")

def parse_args():
    p = argparse.ArgumentParser(description="Move non-JSON files from input subdirs to output subdirs.")
    p.add_argument("input_dir", help="Path to input directory containing subdirectories")
    p.add_argument("output_dir", help="Path to output directory where subdirectories will be created/mirrored")
    return p.parse_args()

def main():
    args = parse_args()
    input_dir = Path(args.input_dir).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    move_non_json(input_dir, output_dir)

if __name__ == "__main__":
    main()