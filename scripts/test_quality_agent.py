from src.agents.quality_agent import CodeQualityAgent
from src.dtos import CodeFileDTO, Language

TEST_CODE = """
def process_data(items=[], a=1, b=2, c=3, d=4, e=5, f=6):
    try:
        for item in items:
            if item > 0:
                print(item)
    except:
        pass
"""

file_dto = CodeFileDTO(
    file_path="test_quality.py",
    language=Language.PYTHON,
    content=TEST_CODE,
    lines_of_code=len(TEST_CODE.splitlines()),
    functions=[],
    imports=[],
    dependencies=[]
)

agent = CodeQualityAgent()
smells, score = agent.scan(file_dto)

print(f"Quality score: {score}/100")
print(f"Total code smells: {len(smells)}")

for smell in smells:
    print("=" * 50)
    print(f"Type: {smell.smell_type}")
    print(f"Description: {smell.description}")
    print(f"Line: {smell.line_start}")
    print(f"Fix: {smell.fix_suggestion}")
