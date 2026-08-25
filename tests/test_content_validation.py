import json
import tempfile
import unittest
from pathlib import Path

from tools.content.validate import discover_concepts, validate_concepts


SCHEMA_PATH = Path(__file__).parents[1] / "schemas/content/concept.schema.json"


def write_concept(directory: Path, concept_id: str, **overrides: object) -> Path:
    metadata: dict[str, object] = {
        "id": concept_id,
        "kind": "concept",
        "title": concept_id.replace("-", " ").title(),
        "summary": f"A test definition of {concept_id}.",
        "status": "draft",
        "prerequisites": [],
        "related": [],
        "mastery": [f"explain {concept_id}"],
    }
    metadata.update(overrides)
    path = directory / f"{concept_id}.mdx"
    yaml_lines = ["---"]
    for key, value in metadata.items():
        yaml_lines.append(f"{key}: {json.dumps(value)}")
    yaml_lines.extend(["---", "", "## Intuition", "", "Test body."])
    path.write_text("\n".join(yaml_lines), encoding="utf-8")
    return path


class ContentValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.concepts = self.root / "content/concepts"
        self.concepts.mkdir(parents=True)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def validate(self) -> list[str]:
        return validate_concepts(
            discover_concepts(self.concepts),
            schema_path=SCHEMA_PATH,
            repository_root=self.root,
        )

    def test_accepts_a_valid_graph(self) -> None:
        source = self.root / "src/example.py"
        source.parent.mkdir()
        source.write_text("VALUE = 1\n", encoding="utf-8")
        write_concept(self.concepts, "agent", related=["environment"])
        write_concept(
            self.concepts,
            "environment",
            prerequisites=["agent"],
            implementations=[{"path": "src/example.py", "symbol": "VALUE"}],
        )

        self.assertEqual(self.validate(), [])

    def test_rejects_an_unknown_relationship(self) -> None:
        write_concept(self.concepts, "agent", related=["missing-concept"])

        errors = self.validate()

        self.assertTrue(any("unknown concept 'missing-concept'" in error for error in errors))

    def test_rejects_a_prerequisite_cycle(self) -> None:
        write_concept(self.concepts, "agent", prerequisites=["environment"])
        write_concept(self.concepts, "environment", prerequisites=["agent"])

        errors = self.validate()

        self.assertTrue(any("prerequisite cycle detected" in error for error in errors))

    def test_rejects_a_missing_implementation_path(self) -> None:
        write_concept(
            self.concepts,
            "agent",
            implementations=[{"path": "src/missing.py"}],
        )

        errors = self.validate()

        self.assertTrue(any("implementation path does not exist" in error for error in errors))

    def test_rejects_a_filename_that_differs_from_the_id(self) -> None:
        path = write_concept(self.concepts, "agent")
        path.rename(self.concepts / "wrong-name.mdx")

        errors = self.validate()

        self.assertTrue(any("filename must match concept id 'agent'" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
