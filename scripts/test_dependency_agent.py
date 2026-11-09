from pathlib import Path
from tempfile import TemporaryDirectory
from src.agents.dependency_agent import DependencyVulnerabilityAgent


def main():
    with TemporaryDirectory() as tmpdir:
        requirements_path = Path(tmpdir) / "requirements.txt"
        requirements_path.write_text("Django==2.2.0\nrequests==2.19.1\n", encoding="utf-8")

        agent = DependencyVulnerabilityAgent()
        risks = agent.scan(requirements_path)

        print(f"\nTotal dependency risks: {len(risks)}")

        for risk in risks[:10]:
            print("=" * 50)
            print(f"Package: {risk.package_name}")
            print(f"Version: {risk.installed_version}")
            print(f"Vulnerability ID: {risk.cve_id}")
            print(f"CVSS: {risk.cvss_score}")


if __name__ == "__main__":
    main()
