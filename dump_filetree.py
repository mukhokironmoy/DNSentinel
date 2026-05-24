import os
from pathlib import Path

# ---- Config ----
OUTPUT_FILENAME = "filetree.txt"

IGNORE_DIRS = {
    ".git", ".hg", ".svn",
    "__pycache__", ".mypy_cache", ".pytest_cache",
    ".venv", "venv", "env",
    "node_modules", ".cache", ".parcel-cache", ".sass-cache",
    "build", "dist", ".next", ".turbo", "target", ".gradle",
    ".idea", ".vscode", ".terraform",
    "docs", "doc", "documentation"
}

IGNORE_FILE_EXTS = {
    ".pyc", ".pyo", ".class", ".o", ".obj", ".a", ".lib",
    ".so", ".dylib", ".dll", ".exe",
    ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar",
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp",
    ".mp3", ".wav", ".flac", ".ogg",
    ".mp4", ".mov", ".avi", ".mkv", ".webm",
    ".ttf", ".otf", ".eot", ".woff", ".woff2",
    ".db", ".sqlite", ".sqlite3", ".pdf", ".bin", ".iso",
    ".log"
}

IGNORE_FILE_NAMES = {
    OUTPUT_FILENAME,
    ".env", ".env.local", ".env.development", ".env.production",
    "Pipfile.lock", "poetry.lock",
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "Thumbs.db", ".DS_Store"
}


def should_skip_file(path: Path) -> bool:
    if path.name in IGNORE_FILE_NAMES:
        return True
    if path.suffix.lower() in IGNORE_FILE_EXTS:
        return True
    return False


def build_tree(root: Path, prefix=""):
    entries = []
    try:
        items = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    except PermissionError:
        return [prefix + "⚠️ [Permission Denied]"]

    for i, path in enumerate(items):
        is_last = i == len(items) - 1
        connector = "└── " if is_last else "├── "

        if path.is_dir():
            if path.name in IGNORE_DIRS:
                continue

            entries.append(prefix + connector + path.name + "/")

            extension = "    " if is_last else "│   "
            entries.extend(build_tree(path, prefix + extension))

        else:
            if should_skip_file(path):
                continue

            entries.append(prefix + connector + path.name)

    return entries


def main():
    script_root = Path(__file__).resolve().parent

    user_input = input(
        "Enter folder path (press Enter for current project): "
    ).strip()

    if user_input:
        chosen_root = Path(user_input).expanduser().resolve()
        if not chosen_root.exists() or not chosen_root.is_dir():
            print("❌ Invalid directory.")
            return
    else:
        chosen_root = script_root

    out_path = chosen_root / OUTPUT_FILENAME

    tree_lines = [chosen_root.name + "/"]
    tree_lines.extend(build_tree(chosen_root))

    with out_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(tree_lines))

    print(f"✅ File tree written to {out_path}")


if __name__ == "__main__":
    main()