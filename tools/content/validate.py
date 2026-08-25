from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CONCEPT_SCHEMA = REPOSITORY_ROOT / "schemas/content/concept.schema.json"
CONCEPT_DIRECTORY = REPOSITORY_ROOT / "content/concepts"


@dataclass(frozen=True)
class ConceptDocument:
    path: Path
    metadata: dict[str, Any]
    body: str


class ContentValidationError(ValueError):
    """Raised when one or more content invariants are violated."""


def parse_front_matter(path: Path) -> ConceptDocument:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or lines[0].strip() != "---":
        raise ContentValidationError(f"{path}: missing opening front-matter delimiter")

    try:
        closing_index = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration as error:
        raise ContentValidationError(
            f"{path}: missing closing front-matter delimiter"
        ) from error

    raw_metadata = "\n".join(lines[1:closing_index])
    metadata = yaml.safe_load(raw_metadata)
    if not isinstance(metadata, dict):
        raise ContentValidationError(f"{path}: front matter must be a YAML mapping")

    body = "\n".join(lines[closing_index + 1 :]).strip()
    return ConceptDocument(path=path, metadata=metadata, body=body)


def discover_concepts(directory: Path) -> list[ConceptDocument]:
    if not directory.exists():
        return []

    documents = []
    for path in sorted(directory.glob("*.mdx")):
        if not path.name.startswith("_"):
            documents.append(parse_front_matter(path))
    return documents


def load_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _json_path(parts: Iterable[Any]) -> str:
    rendered = "".join(f"[{part}]" if isinstance(part, int) else f".{part}" for part in parts)
    return rendered.removeprefix(".") or "<root>"


def validate_concepts(
    documents: list[ConceptDocument],
    *,
    schema_path: Path = CONCEPT_SCHEMA,
    repository_root: Path = REPOSITORY_ROOT,
) -> list[str]:
    validator = Draft202012Validator(load_schema(schema_path))
    errors: list[str] = []

    for document in documents:
        for error in sorted(
            validator.iter_errors(document.metadata), key=lambda item: list(item.path)
        ):
            errors.append(
                f"{document.path}: {_json_path(error.path)}: {error.message}"
            )

    concepts_by_id: dict[str, ConceptDocument] = {}
    for document in documents:
        concept_id = document.metadata.get("id")
        if not isinstance(concept_id, str):
            continue
        if concept_id in concepts_by_id:
            errors.append(
                f"{document.path}: duplicate id '{concept_id}' also used by "
                f"{concepts_by_id[concept_id].path}"
            )
            continue
        concepts_by_id[concept_id] = document

        if document.path.stem != concept_id:
            errors.append(
                f"{document.path}: filename must match concept id '{concept_id}'"
            )

    known_ids = set(concepts_by_id)
    for concept_id, document in concepts_by_id.items():
        metadata = document.metadata
        for field in ("prerequisites", "related", "unlocks"):
            references = metadata.get(field, [])
            if not isinstance(references, list):
                continue
            for reference in references:
                if reference == concept_id:
                    errors.append(
                        f"{document.path}: {field} must not reference itself"
                    )
                elif isinstance(reference, str) and reference not in known_ids:
                    errors.append(
                        f"{document.path}: {field} references unknown concept "
                        f"'{reference}'"
                    )

        implementations = metadata.get("implementations", [])
        if isinstance(implementations, list):
            for implementation in implementations:
                if not isinstance(implementation, dict):
                    continue
                source_path = implementation.get("path")
                if isinstance(source_path, str) and not (repository_root / source_path).is_file():
                    errors.append(
                        f"{document.path}: implementation path does not exist: "
                        f"{source_path}"
                    )

    errors.extend(_find_prerequisite_cycles(concepts_by_id))
    return sorted(errors)


def _find_prerequisite_cycles(
    concepts_by_id: dict[str, ConceptDocument],
) -> list[str]:
    visited: set[str] = set()
    active: list[str] = []
    active_set: set[str] = set()
    cycles: set[tuple[str, ...]] = set()

    def visit(concept_id: str) -> None:
        if concept_id in active_set:
            cycle_start = active.index(concept_id)
            cycles.add(tuple(active[cycle_start:] + [concept_id]))
            return
        if concept_id in visited:
            return

        active.append(concept_id)
        active_set.add(concept_id)
        prerequisites = concepts_by_id[concept_id].metadata.get("prerequisites", [])
        if isinstance(prerequisites, list):
            for prerequisite in prerequisites:
                if prerequisite in concepts_by_id:
                    visit(prerequisite)
        active.pop()
        active_set.remove(concept_id)
        visited.add(concept_id)

    for concept_id in sorted(concepts_by_id):
        visit(concept_id)

    return [
        "prerequisite cycle detected: " + " -> ".join(cycle)
        for cycle in sorted(cycles)
    ]


def validate_repository(
    *,
    concept_directory: Path = CONCEPT_DIRECTORY,
    schema_path: Path = CONCEPT_SCHEMA,
    repository_root: Path = REPOSITORY_ROOT,
) -> list[str]:
    try:
        documents = discover_concepts(concept_directory)
    except (ContentValidationError, yaml.YAMLError) as error:
        return [str(error)]
    return validate_concepts(
        documents,
        schema_path=schema_path,
        repository_root=repository_root,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Krybor RL structured learning content."
    )
    parser.parse_args()

    errors = validate_repository()
    if errors:
        print("Content validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    concept_count = len(discover_concepts(CONCEPT_DIRECTORY))
    print(f"Content validation passed ({concept_count} concepts).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
