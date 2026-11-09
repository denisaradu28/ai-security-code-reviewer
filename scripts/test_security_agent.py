
from src.agents.security_agent import RAGSecurityAgent
from src.dtos import CodeFileDTO, Language

TEST_CODE = """
import pickle

API_KEY = "super-secret-api-key-12345"
DEBUG = True

def get_user(cursor, user_id):
    query = f"SELECT * FROM users WHERE id={user_id}"
    return cursor.execute(query)

def deserialize(data):
    return pickle.loads(data)
"""

file_dto = CodeFileDTO(
    file_path="test_vulnerable.py",
    language=Language.PYTHON,
    content=TEST_CODE,
    lines_of_code=len(TEST_CODE.splitlines()),
    functions=[],
    imports=["pickle"],
    dependencies=[],
)

agent = RAGSecurityAgent(relevance_threshold=0.5)

print("=== DETECTED RISK PATTERNS ===")
patterns = agent.detect_risk_patterns(file_dto)

for pattern in patterns:
    print("-", pattern)

print("\n=== RETRIEVED CONTEXT ===")
context_map = agent.retrieve_for_file(file_dto, k=5)

for pattern, results in context_map.items():
    print(f"\nPATTERN: {pattern}")

    if not results:
        print("NO RELEVANT CONTEXT")
        continue

    for result in results:
        print(
            f"{result.score:.4f} | "
            f"{result.doc_type} | "
            f"{result.source}"
        )


print("\n=== GEMINI SECURITY SCAN ===")

vulnerabilities = agent.scan(file_dto, k=5)

print(f"\nTotal findings: {len(vulnerabilities)}")

for vulnerability in vulnerabilities:
    print("\n" + "=" * 60)
    print("Title:", vulnerability.title)
    print("Severity:", vulnerability.severity.value)
    print("File:", vulnerability.file_path)
    print("Line:", vulnerability.line_number)
    print("Description:", vulnerability.description)
    print("Fix:", vulnerability.fix_suggestion)
    print("Source:", vulnerability.cited_source)
    print("Coverage empty:", vulnerability.coverage_empty)
