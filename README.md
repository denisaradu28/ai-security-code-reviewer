
# AI Security Code Reviewer

An AI-powered security code review application built with Python, Google Gemini, Retrieval-Augmented Generation (RAG), and LangGraph.

The system analyzes Python repositories, identifies potential security vulnerabilities, detects code quality issues, checks dependencies against vulnerability databases, and generates structured security reports.

## Features

- **AI Security Analysis** — Detects potential vulnerabilities using Google Gemini.
- **RAG-Based Analysis** — Retrieves relevant security documentation from ChromaDB.
- **Static Code Analysis** — Detects code smells using Python AST.
- **Dependency Scanning** — Checks Python packages against the OSV API.
- **Multi-Agent Architecture** — Coordinates agents using LangGraph.
- **Feedback Memory** — Stores human feedback for future reference.
- **Security Reports** — Generates structured JSON reports.
- **Streamlit Dashboard** — Interactive interface for reviewing results.
- **Docker Support** — Containerized application.
- **RAGAS Evaluation** — Preliminary evaluation of document retrieval.

##  Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 |
| LLM | Google Gemini 2.5 Flash |
| Embeddings | Google Gemini Embeddings |
| AI Framework | LangChain |
| Vector Database | ChromaDB |
| Agent Orchestration | LangGraph |
| Static Analysis | Python AST |
| Dependency Scanning | OSV API |
| Data Validation | Pydantic |
| Frontend | Streamlit |
| Evaluation | RAGAS |
| Containerization | Docker |
| Package Management | uv |

## Architecture

```text
                 Python Repository
                         |
                         v
                  Repository Parser
                         |
                         v
                      LangGraph
                         |
                         v
                   Quality Agent
                         |
                         v
                   Security Agent
                         |
                  RAG Retrieval
                         |
                      ChromaDB
                         |
                     Gemini LLM
                         |
                         v
                  Dependency Agent
                         |
                         v
                  Report Generator
                         |
                         v
                     JSON Report
                         |
                         v
                 Streamlit Dashboard
```

## Project Structure

```text
ai-security-code-reviewer/
├── src/
│   ├── agents/
│   │   ├── security_agent.py
│   │   ├── dependency_agent.py
│   │   ├── quality_agent.py
│   │   ├── feedback_agent.py
│   │   └── report_agent.py
│   ├── graph/
│   │   └── workflow.py
│   ├── tools/
│   │   └── vector_tools.py
│   ├── dtos.py
│   └── app.py
├── scripts/
│   ├── run_review.py
│   ├── test_security_agent.py
│   ├── test_dependency_agent.py
│   ├── test_quality_agent.py
│   ├── test_feedback_agent.py
│   ├── test_report_agent.py
│   └── evaluate_rag.py
├── data/
│   └── repos/
├── vectorstore/
├── memory/
├── reports/
├── Dockerfile
├── .dockerignore
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## Installation

### Prerequisites

- Python 3.11
- Git
- uv
- Google Gemini API key
- Docker Desktop (optional)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-security-code-reviewer.git
cd ai-security-code-reviewer
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Install Dependencies

```bash
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMENI_CHAT_MODEL=gemini-2.5-flash
```

The `GEMENI_CHAT_MODEL` spelling matches the current Security Agent implementation.

Never commit `.env` or API keys to GitHub.

### 4. Prepare the RAG Database

The Security Agent requires an initialized ChromaDB collection containing security documentation.

The security corpus includes:

- CVE vulnerability references
- OWASP Top 10 documentation
- CWE security weaknesses
- Python security guidance
- Framework security documentation
- Secure coding recommendations

Run the project's corpus ingestion and vector indexing scripts before starting a security review.

The persistent vector database is stored in `vectorstore/`.

## Usage

### Streamlit Dashboard

Start the application:

```bash
uv run python -m streamlit run src/app.py
```

Open:

http://localhost:8501

The dashboard allows users to:

1. Enter a local repository path.
2. Select the number of Python files to analyze.
3. Run the security review.
4. Inspect security findings and code quality issues.
5. View dependency vulnerabilities.
6. Download the JSON report.

### Command-Line Interface

Clone a public Python repository:

```bash
git clone --depth 1 https://github.com/pallets/flask.git data/repos/flask
```

Run the review:

```bash
uv run python -m scripts.run_review data/repos/flask --limit 1
```

The `--limit` option controls how many Python files are analyzed.

The generated report is saved to:

```text
reports/flask_review.json
```

## Security Agent

The Security Agent uses Google Gemini with retrieved security documentation to identify potential vulnerabilities.

Supported risk patterns include:

- SQL Injection
- Unsafe Deserialization
- Code Injection
- Hardcoded Secrets
- Debug Configuration Risks
- Potential Cross-Site Scripting

Each security finding can include:

- Vulnerability title
- Description
- Severity
- File path and line number
- Suggested remediation
- Supporting documentation citation

The agent validates citations against retrieved sources.

When relevant documentation is unavailable, it can generate a coverage-gap finding requiring manual review.

## Code Quality Agent

The Code Quality Agent performs static analysis using Python AST.

It detects:

- Long Functions
- High Cyclomatic Complexity
- Too Many Parameters
- Mutable Default Arguments
- Bare Except Handlers

The agent generates a heuristic quality score between 0 and 100.

Example output:

```text
Quality score: 70.0/100
Total code smells: 3

TOO_MANY_PARAMETERS
MUTABLE_DEFAULT
BARE_EXCEPT
```

## Dependency Vulnerability Agent

The Dependency Agent analyzes pinned packages in `requirements.txt`.

It queries the OSV API to identify known vulnerabilities affecting installed package versions.

Reported information includes:

- Package name
- Installed version
- Vulnerability identifier
- CVSS score, when available

The current implementation supports pinned PyPI dependencies.

## Feedback and Episodic Memory

The Feedback Agent stores human review feedback in persistent JSONL storage.

Feedback records include:

- Original finding identifier
- Code snippet
- Agent verdict
- False-positive status
- Human comment
- Timestamp

Historical feedback can be retrieved using lexical similarity.

Automatic use of feedback to adjust future security findings is not yet integrated into the LangGraph workflow.

## LangGraph Workflow

The application uses LangGraph to coordinate the analysis pipeline.

The workflow consists of:

```text
START
  |
  v
Quality Agent
  |
  v
Security Agent + RAG
  |
  v
Dependency Agent
  |
  v
Report Generator
  |
  v
END
```

The final workflow state contains the generated review report and dependency vulnerability results.

## Docker

### Build the Image

```bash
docker build -t ai-security-code-reviewer .
```

### Run the Container

On Windows PowerShell:

```powershell
docker run --rm -p 8501:8501 --env-file .env --mount "type=bind,source=${PWD}\vectorstore,target=/app/vectorstore" --mount "type=bind,source=${PWD}\data\repos,target=/app/data/repos" ai-security-code-reviewer
```

Open:

http://localhost:8501

The application uses bind mounts for the persistent vector database and local repositories.

API keys are supplied through environment variables rather than embedded in the Docker image.

## Testing

Run individual component tests:

```bash
python -m scripts.test_security_agent
python -m scripts.test_dependency_agent
python -m scripts.test_quality_agent
python -m scripts.test_feedback_agent
python -m scripts.test_report_agent
```

Run an end-to-end security review:

```bash
python -m scripts.run_review data/repos/flask --limit 1
```

The workflow has been tested against a locally cloned Flask repository.

## RAG Evaluation

The retrieval system was evaluated using RAGAS 0.4.3 with non-LLM context precision and recall metrics.

### Evaluation Results

| Query | Retrieved Documents | Precision | Recall |
|---|---:|---:|---:|
| SQL Injection Prevention | 5 | 0.000 | 0.000 |
| Unsafe Pickle Deserialization | 5 | 0.000 | 0.000 |

Results are stored in:

```text
reports/rag_evaluation.json
```

### Interpretation

The retrieval system returned five documents for each test query.

However, the non-LLM evaluation metrics returned zero scores.

The preliminary evaluation used short reference strings rather than fully annotated reference documents. Therefore, these results are insufficient to establish retrieval accuracy.

A more comprehensive evaluation should include:

- A larger evaluation dataset
- Human-annotated reference contexts
- Additional security categories
- More robust relevance metrics

RAGAS was executed in an isolated environment due to dependency compatibility issues.

## Limitations

- The security analysis currently focuses on Python repositories.
- AI findings may contain false positives or miss vulnerabilities.
- Gemini API rate limits can restrict the number of files analyzed.
- Dependency scanning requires pinned PyPI package versions.
- The security score is heuristic.
- Dependency risks are not currently included in the overall security score.
- Feedback is stored but not automatically applied to future AI verdicts.
- The RAG evaluation is preliminary.
- Large repositories may require significant processing time and API usage.

## Security Considerations

- Analyze only repositories you are authorized to review.
- Treat repository source code as untrusted input.
- Do not execute untrusted repository code.
- Never commit credentials or API keys.
- Avoid storing sensitive information in feedback memory.
- Manually verify AI-generated findings before acting on them.

## Future Improvements

- Multi-language support
- AI request batching and caching
- Semantic episodic memory
- Automated feedback integration
- GitHub Actions integration
- SARIF and PDF reports
- Expanded RAGAS evaluation
- Automated regression testing
- Improved vulnerability prioritization

## Project Goals

This project demonstrates practical experience with:

- Large Language Models
- Retrieval-Augmented Generation
- Multi-Agent AI Systems
- Application Security
- Static Code Analysis
- Vulnerability Databases
- Vector Databases
- API Integration
- Docker Deployment
- AI Evaluation

## Disclaimer

AI Security Code Reviewer is an educational and experimental application security tool.

It is not a replacement for professional security auditing. All identified vulnerabilities should be manually verified before remediation decisions are made.
