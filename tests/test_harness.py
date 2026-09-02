from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from new_skill import create_skill  # noqa: E402
from validate_skills import validate  # noqa: E402


class HarnessTests(unittest.TestCase):
    def test_repository_skills_are_valid(self) -> None:
        self.assertEqual(validate(REPO_ROOT / "skills"), [])

    def test_generated_skill_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skills_dir = Path(temporary_directory) / "skills"
            output = create_skill(
                behavior="tiny-yell",
                locale="ko",
                title="Tiny Yell",
                description="Turn ordinary prose into a tiny locale-specific yell.",
                instructions=["Replace ordinary prose with a tiny yell."],
                example_input="안녕하세요",
                example_output="꺅!",
                skills_dir=skills_dir,
            )
            self.assertEqual(output.parent.name, "stupid-tiny-yell-ko")
            self.assertEqual(validate(skills_dir), [])

    def test_existing_skill_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skills_dir = Path(temporary_directory) / "skills"
            arguments = dict(
                behavior="beep",
                locale="en-us",
                description="Replace ordinary prose with a beep.",
                instructions=["Replace ordinary prose with beep."],
                example_input="Hello",
                example_output="Beep",
                skills_dir=skills_dir,
            )
            create_skill(**arguments)
            with self.assertRaises(FileExistsError):
                create_skill(**arguments)


if __name__ == "__main__":
    unittest.main()
