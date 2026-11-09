
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from src.agents.feedback_agent import FeedbackAgent
from src.dtos import FeedbackDTO


def main():
    with TemporaryDirectory() as temp_dir:
        memory_path = str(Path(temp_dir) / "feedback.jsonl")
        agent = FeedbackAgent(memory_path)

        feedback = FeedbackDTO(
            feedback_id="FB-001",
            original_finding_id="SEC-001",
            file_path="test_vulnerable.py",
            code_snippet='query = f"SELECT * FROM users WHERE id={user_id}"',
            agent_verdict="SQL Injection",
            is_false_positive=False,
            human_comment="Confirmed SQL injection risk.",
            timestamp=datetime.now(timezone.utc).isoformat()
        )

        agent.save_feedback(feedback)

        new_agent = FeedbackAgent(memory_path)
        stored = new_agent.load_feedback()
        similar = new_agent.find_similar_feedback(
            'query = f"SELECT * FROM users WHERE id={user_id}"'
        )

        print(f"Stored feedback: {len(stored)}")
        print(f"Similar feedback: {len(similar)}")

        for item in similar:
            print(f"Verdict: {item.agent_verdict}")
            print(f"False positive: {item.is_false_positive}")
            print(f"Comment: {item.human_comment}")


if __name__ == "__main__":
    main()
