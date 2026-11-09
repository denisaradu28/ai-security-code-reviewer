import argparse
import json
from pathlib import Path

from src.dtos import CodeFileDTO, RepositoryDTO, Language
from src.agents.security_agent import RAGSecurityAgent
from src.agents.dependency_agent import DependencyVulnerabilityAgent
from src.graph.workflow import build_workflow


def load_repo(path: Path, limit: int) -> RepositoryDTO:
    files = []
    for file in sorted(path.rglob("*.py")):
        if any(part in {".venv", "venv", ".git", "__pycache__"} for part in file.relative_to(path).parts):
            continue
        try:
            content = file.read_text(encoding="utf-8-sig")
        except (UnicodeError, OSError):
            continue
        files.append(CodeFileDTO(file_path=str(file.relative_to(path)), language=Language.PYTHON, content=content, lines_of_code=len(content.splitlines()), functions=[], imports=[], dependencies=[]))
        if len(files) >= limit:
            break

    if not files:
        raise ValueError("No Python files found.")

    return RepositoryDTO(url="", name=path.name, local_path=str(path), files=files, total_loc=sum(f.lines_of_code for f in files), languages=[Language.PYTHON])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_path")
    parser.add_argument("--limit", type=int, default=1)
    args = parser.parse_args()

    path = Path(args.repo_path).resolve()
    if not path.is_dir():
        raise FileNotFoundError(path)
    if args.limit < 1:
        raise ValueError("--limit must be at least 1")

    repo = load_repo(path, args.limit)
    security_agent = RAGSecurityAgent()
    dependency_agent = DependencyVulnerabilityAgent()

    def scan_dependencies(repo_dto: RepositoryDTO):
        requirements = Path(repo_dto.local_path) / "requirements.txt"
        return dependency_agent.scan(str(requirements)) if requirements.is_file() else []

    workflow = build_workflow(security_agent.scan, scan_dependencies)
    result = workflow.invoke({"repo": repo})

    report = result["report"]
    risks = result["dependency_risks"]
    output = {"report": report.model_dump(mode="json"), "dependency_risks": [risk.model_dump(mode="json") for risk in risks]}

    Path("reports").mkdir(exist_ok=True)
    output_path = Path("reports") / f"{repo.name}_review.json"
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Reviewed files: {report.reviewed_files}")
    print(f"Security score: {report.overall_security_score}")
    print(f"Dependency risks: {len(risks)}")
    print(f"Report saved: {output_path}")


if __name__ == "__main__":
    main()
