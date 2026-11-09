
from pathlib import Path
import requests
from packaging.requirements import Requirement, InvalidRequirement
from cvss import CVSS3
from src.dtos import DependencyRiskDTO


class DependencyVulnerabilityAgent:
    OSV_URL = "https://api.osv.dev/v1/query"

    def parse_requirements(self, file_path: str) -> list[tuple[str, str]]:
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Requirements file not found: {file_path}")

        dependencies = []
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            line = line.strip()
            if not line or line.startswith(("#", "-")):
                continue

            try:
                requirement = Requirement(line)
            except InvalidRequirement:
                continue

            if requirement.marker and not requirement.marker.evaluate():
                continue

            specifiers = list(requirement.specifier)
            if len(specifiers) != 1 or specifiers[0].operator != "==":
                continue

            version = specifiers[0].version
            if "*" not in version:
                dependencies.append((requirement.name, version))

        return list(dict.fromkeys(dependencies))

    def get_cvss_score(self, vulnerability: dict) -> float:
        for severity in vulnerability.get("severity", []):
            if severity.get("type") == "CVSS_V3":
                try:
                    return float(CVSS3(severity["score"]).scores()[0])
                except (ValueError, KeyError, TypeError):
                    continue
        return 0.0

    def check_dependency(self, package_name: str, version: str) -> list[DependencyRiskDTO]:
        payload = {
            "package": {"name": package_name, "ecosystem": "PyPI"},
            "version": version
        }

        response = requests.post(self.OSV_URL, json=payload, timeout=30)
        response.raise_for_status()

        risks = []
        for vulnerability in response.json().get("vulns", []):
            aliases = vulnerability.get("aliases", [])
            cve_id = next(
                (alias for alias in aliases if alias.startswith("CVE-")),
                vulnerability["id"]
            )

            risks.append(DependencyRiskDTO(
                package_name=package_name,
                installed_version=version,
                vulnerable_version=[version],
                cve_id=cve_id,
                cvss_score=self.get_cvss_score(vulnerability)
            ))

        return risks

    def scan(self, requirements_path: str) -> list[DependencyRiskDTO]:
        dependencies = self.parse_requirements(requirements_path)
        risks = []

        print(f"Checking {len(dependencies)} pinned dependencies...")

        for name, version in dependencies:
            print(f"Checking {name}=={version}")
            risks.extend(self.check_dependency(name, version))

        return risks