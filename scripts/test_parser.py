from src.agents.parser_agent import CodeParserAgent
from pathlib import Path

REPO_URL = "https://github.com/psf/requests"


parser = CodeParserAgent()

repository = parser.parse(REPO_URL)

print()
print("==========================")
print("REPOSITORY SUMMARY")
print("==========================")

print(f"Name: {repository.name}")
print(f"Local path: {repository.local_path}")
print(f"Files parsed: {len(repository.files)}")
print(f"Total LOC: {repository.total_loc}")

print(
    "Languages:",
    [language.value for language in repository.languages]
)


total_functions = sum(
    len(file.functions)
    for file in repository.files
)

print(
    f"Functions found: {total_functions}"
)


print()
print("==========================")
print("FIRST 3 FILES")
print("==========================")


for file in repository.files[:3]:

    print()
    print(file.model_dump_json(indent=2))

output_path = Path("data/review_example.json")
output_path.parent.mkdir(parents=True, exist_ok=True)

output_path.write_text(repository.model_dump_json(indent=2), encoding="utf-8")
print(f"\nSaved parser output to: {output_path}")
