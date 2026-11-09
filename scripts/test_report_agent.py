from src.agents.report_agent import ReportGenerator
from src.dtos import (RepositoryDTO, CodeFileDTO, FileReviewDTO, VulnerabilityDTO, VulnerabilitySeverity, IssueType, Language)

code_file = CodeFileDTO(
    file_path="app.py",
    language=Language.PYTHON,
    content="print('hello')",
    lines_of_code=1,
    functions=[],
    imports=[],
    dependencies=[]
)

repo = RepositoryDTO(
    url="https://github.com/example/test-repo",
    name="test-repo",
    local_path="data/repos/test-repo",
    files=[code_file],
    total_loc=1,
    languages=[Language.PYTHON]
)

vulnerability = VulnerabilityDTO(
    id="SEC-001",
    issue_type=IssueType.SECURITY_VULN,
    title="Example SQL Injection",
    description="Unsafe SQL query construction.",
    severity=VulnerabilitySeverity.RIDICAT,
    file_path="app.py",
    line_number=1,
    fix_suggestion="Use parameterized queries.",
    cited_source="https://cwe.mitre.org/data/definitions/89.html"
)

file_review = FileReviewDTO(
    file_path="app.py",
    vulnerabilities=[vulnerability],
    code_smells=[],
    quality_score=100.0
)

report = ReportGenerator().generate(repo, [file_review])

print("Repository:", report.repo_name)
print("Files reviewed:", report.reviewed_files)
print("High severity:", report.high_count)
print("Security score:", report.overall_security_score)
print("Summary:", report.executive_summary)
