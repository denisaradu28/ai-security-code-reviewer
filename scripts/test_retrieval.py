from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.tools.vector_tools import (
    EMBEDDING_MODEL,
    SECURITY_COLLECTION,
)


VECTORSTORE_DIRECTORY = Path("vectorstore")


TEST_QUERIES = [
    "Python SQL query built with user input using string formatting, no parameterized query",
    "Hardcoded API key or password stored directly in source code",
    "Python unsafe deserialization using pickle.loads on untrusted input",
    "Application running with DEBUG enabled in production",
    "Cross-site scripting caused by inserting untrusted user input into HTML",
]


def main():
    load_dotenv()

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
    )

    vectorstore = Chroma(
        collection_name=SECURITY_COLLECTION,
        persist_directory=str(VECTORSTORE_DIRECTORY),
        embedding_function=embeddings,
    )

    print("RAG RETRIEVAL TEST")

    for query in TEST_QUERIES:

        print()
        print(f"QUERY: {query}")

        results = vectorstore.similarity_search_with_relevance_scores(
            query,
            k=5,
        )

        for index, (document, score) in enumerate(
            results,
            start=1,
        ):
            print()
            print(f"RESULT #{index}")
            print(f"Score: {score:.4f}")
            print(
                "Type:",
                document.metadata.get("doc_type"),
            )
            print(
                "Source:",
                document.metadata.get("source"),
            )

            if document.metadata.get("cve_id"):
                print(
                    "CVE:",
                    document.metadata.get("cve_id"),
                )

            if document.metadata.get("owasp_category"):
                print(
                    "OWASP:",
                    document.metadata.get("owasp_category"),
                )

            print(
                "Text:",
                document.page_content[:300]
                .replace("\n", " "),
                "...",
            )


if __name__ == "__main__":
    main()