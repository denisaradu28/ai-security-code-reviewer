from pathlib import Path
import shutil

from git import Repo

EXCLUDED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "dist",
    "build",
    ".idea",
    ".vscode",
}


SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".go",
}

DEPENDENCY_FILES = {
    "requirements.txt",
    "pyproject.toml",
    "package.json",
}

def clone_repo(repo_url: str, destination: Path) -> Path:
    """
    Clone a Git repository using a shallow clone.

    If the repository was already cloned, the old copy is removed first.
    """

    if destination.exists():
        shutil.rmtree(destination)

    destination.parent.mkdir(parents=True, exist_ok=True)

    Repo.clone_from(repo_url, destination, depth=1,)
    return destination

def is_excluded(path: Path) -> bool:
    """
    Check if the path contains a directory that should not be analyzed.
    """
    return any(part is EXCLUDED_DIRECTORIES for part in path.parts)

def list_code_files(repo_path: Path) -> list[Path]:
    """
    Recursively find supported source code files.
    """

    files = []

    for path in repo_path.rglob("*"):
        if not path.is_file():
            continue
        if is_excluded(path):
            continue
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        files.append(path)
    return files

def read_file(path: Path) -> str | None:
    """
    Read a source file safely.

    Returns None if the file cannot be decoded.
    """

    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as error:
        print(f"[WARNING] Could not read {path}: {error}")
        return None

def list_dependency_files(repo_path: Path) -> list[Path]:
    files = []

    for path in repo_path.rglob("*"):
        if not path.is_file():
            continue

        if is_excluded(path):
            continue
        if path.name in DEPENDENCY_FILES:
            files.append(path)

    return files