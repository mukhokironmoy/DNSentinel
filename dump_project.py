# dump_project.py
# Creates project_dump.txt in the chosen root folder, containing all text files
# with a header line showing each file's path relative to the chosen root.

import os
from pathlib import Path

# ---- Tweak these if you like ----
OUTPUT_FILENAME = "project_dump.txt"
MAX_FILE_SIZE_MB = 3  # skip very large files

IGNORE_DIRS = {
    ".git", ".hg", ".svn",
    "__pycache__", ".mypy_cache", ".pytest_cache",
    ".venv", "venv", "env",
    "node_modules", ".cache", ".parcel-cache", ".sass-cache",
    "build", "dist", ".next", ".turbo", "target", ".gradle",
    ".idea", ".vscode", ".terraform"
}

IGNORE_FILE_EXTS = {
    ".pyc", ".pyo", ".class", ".o", ".obj", ".a", ".lib",
    ".so", ".dylib", ".dll", ".exe",
    ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar",
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp",
    ".mp3", ".wav", ".flac", ".ogg",
    ".mp4", ".mov", ".avi", ".mkv", ".webm",
    ".ttf", ".otf", ".eot", ".woff", ".woff2",
    ".db", ".db3", ".sqlite", ".sqlite3", ".pdf", ".bin", ".iso",
    ".log"
}

IGNORE_FILE_NAMES = {
    OUTPUT_FILENAME,
    ".env", ".env.local", ".env.development", ".env.production",
    "Pipfile.lock", "poetry.lock", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "Thumbs.db", ".DS_Store"
}


def should_skip_file(path: Path) -> bool:
    name = path.name
    if name in IGNORE_FILE_NAMES:
        return True
    if path.suffix.lower() in IGNORE_FILE_EXTS:
        return True
    try:
        if path.stat().st_size > MAX_FILE_SIZE_MB * 1024 * 1024:
            return True
    except OSError:
        return True
    return False


def main():
    script_root = Path(__file__).resolve().parent

    # Prompt user
    user_input = input(
        "Enter folder path to dump (press Enter to dump project root): "
    ).strip()

    # Determine root directory
    if user_input:
        chosen_root = Path(user_input).expanduser().resolve()
        if not chosen_root.exists() or not chosen_root.is_dir():
            print("❌ Invalid directory path.")
            return
    else:
        chosen_root = script_root

    out_path = chosen_root / OUTPUT_FILENAME

    with out_path.open("w", encoding="utf-8") as out:
        for dirpath, dirnames, filenames in os.walk(chosen_root, topdown=True):
            dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

            for fname in filenames:
                fpath = Path(dirpath) / fname

                if should_skip_file(fpath):
                    continue

                rel = fpath.relative_to(chosen_root).as_posix()
                out.write(f"\n\n--- FILE: {rel} ---\n\n")

                try:
                    with fpath.open("r", encoding="utf-8") as f:
                        out.write(f.read())
                except UnicodeDecodeError:
                    try:
                        with fpath.open("r", encoding="latin-1") as f:
                            out.write(f.read())
                    except Exception as e:
                        out.write(f"[Could not read file: {e}]\n")
                except Exception as e:
                    out.write(f"[Could not read file: {e}]\n")

    print(f"✅ Dump complete → {out_path}")


if __name__ == "__main__":
    main()