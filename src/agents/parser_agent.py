import ast
import json
from pathlib import Path
from urllib.parse import urlparse

from src.dtos import (CodeFileDTO, FunctionDTO, Language, RepositoryDTO,)
from src.tools.repo_tools import (clone_repo, list_code_files, read_file, list_dependency_files,)

class CodeParserAgent:

    def __init__(self, repos_directory: str = "data/repos"):
        self.repos_directory = Path(repos_directory)

    def parse(self, repo_url: str) -> RepositoryDTO:
        """
        Clone and analyze a GitHub repository. Return a valid RepositoryDTO.
        """
        repo_name = self._extract_repo_name(repo_url)

        local_path = self.repos_directory / repo_name
        print(f"[Parser] Cloning repository: {repo_url}")

        clone_repo(repo_url, local_path)
        print(f"Repository cloned to: {local_path}")

        code_files = list_code_files(local_path)

        dependency_files = list_dependency_files(local_path)
        repository_dependencies = []

        for dependency_file in dependency_files:
            if dependency_file.name == "requirements.txt":
                repository_dependencies.extend(self._parse_requirements(dependency_file))
            elif dependency_file.name == "package.json":
                repository_dependencies.extend(self._parse_package_json(dependency_file))

        parsed_files : list[CodeFileDTO] = []

        detected_language : set[Language] = set()

        total_loc = 0

        for file_path in code_files:

            try:
                file_dto = self._parse_file(file_path=file_path, repo_path=local_path)
                if file_dto is None:
                    continue
                parsed_files.append(file_dto)
                detected_language.add(file_dto.language)
                total_loc += file_dto.lines_of_code
            except Exception as e:
                print(f"[WARNING] Could not parse {file_path}: {e}")

        repository = RepositoryDTO(
            url=repo_url,
            name=repo_name,
            local_path=str(local_path),
            files=parsed_files,
            total_loc=total_loc,
            languages=list(detected_language),
        )

        return repository

    def _parse_file(self, file_path:Path, repo_path:Path) -> CodeFileDTO | None:
        content = read_file(file_path)

        if content is None:
            return None

        language = self._detect_language(file_path)

        relative_path = file_path.relative_to(repo_path)

        functions = []
        imports = []

        if language == Language.PYTHON:
            functions, imports = self._parse_python(content)

        lines_of_code = len(content.splitlines())

        return CodeFileDTO(
            file_path=str(relative_path),
            language=language,
            content=content,
            lines_of_code=lines_of_code,
            functions=functions,
            imports=imports,
            dependencies=[],
        )

    def _parse_python(self, content:str) -> tuple[list[FunctionDTO], list[str]]:

        functions = []
        imports = []

        try:
            tree = ast.parse(content)

        except SyntaxError as e:
            print(f"[WARNING] Syntax Error: {e}")
            return functions, imports

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                params = [arg.arg for arg in node.args.args]
                end_line = getattr(node, "end_lineno", node.lineno,)

                function = FunctionDTO(
                    name=node.name,
                    start_line=node.lineno,
                    end_line=end_line,
                    params=params,
                )

                functions.append(function)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        return functions, sorted(set(imports))

    def _detect_language(self, file_path:Path) -> Language:
        extension_map = {
            ".py": Language.PYTHON,
            ".js": Language.JAVASCRIPT,
            ".ts": Language.TYPESCRIPT,
            ".java": Language.JAVA,
            ".go": Language.GO,
        }

        return extension_map.get(file_path.suffix.lower(), Language.OTHER)

    def _extract_repo_name(self, repo_url:str) -> str:
        path = urlparse(repo_url).path
        repo_name = Path(path).name

        if repo_name.endswith(".git"):
            repo_name = repo_name[:-len(".git")]

        if not repo_name:
            raise ValueError("Could not determine repo name")

        return repo_name

    def _parse_requirements(self, path: Path) -> list[str]:
        content = read_file(path)

        if content is None:
            return []

        dependencies = []

        for line in content.splitlines():

            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            dependencies.append(line)
        return dependencies

    def _parse_package_json(self, path: Path) -> list[str]:

        content = read_file(path)
        if content is None:
            return []

        try:
            data = json.loads(content)

        except json.JSONDecodeError as e:
            print(f"[WARNING] Invalid package.json {path}: {e}")
            return []
        dependencies = []

        for section in ("dependencies", "devDependencies"):
            packages = data.get(section, [])

            for name, version in packages.items():
                dependencies.append(f"{name}@{version}")

        return dependencies