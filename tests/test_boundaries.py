from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from new_skill import SkillInputError, create_skill  # noqa: E402
from validate_skills import validate  # noqa: E402


class BoundaryTests(unittest.TestCase):
    def test_malformed_quoted_frontmatter_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skills_dir = Path(temporary_directory) / "skills"
            output = create_skill(
                behavior="beep",
                locale="ko",
                description="Replace ordinary prose with a beep.",
                instructions=["Replace ordinary prose with beep."],
                example_input="안녕하세요",
                example_output="삐",
                family_description_en="A family of beeping skills.",
                family_description_ko="삐 소리를 내는 스킬 패밀리입니다.",
                skills_dir=skills_dir,
            )
            output.write_text(
                output.read_text(encoding="utf-8").replace(
                    'description: "Replace ordinary prose with a beep."',
                    'description: "unterminated',
                ),
                encoding="utf-8",
            )

            errors = validate(
                skills_dir,
                repository_root=Path(temporary_directory),
            )

            self.assertTrue(any("frontmatter" in error for error in errors))

    def test_generator_rejects_unsupported_locale(self) -> None:
        with (
            tempfile.TemporaryDirectory() as temporary_directory,
            self.assertRaises(SkillInputError),
        ):
            create_skill(
                behavior="beep",
                locale="xx",
                description="Replace ordinary prose with a beep.",
                instructions=["Replace ordinary prose with beep."],
                example_input="Hello",
                example_output="Beep",
                family_description_en="A family of beeping skills.",
                family_description_ko="삐 소리를 내는 스킬 패밀리입니다.",
                skills_dir=Path(temporary_directory) / "skills",
            )

    def test_generated_catalog_contains_skill_installer_url(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository_root = Path(temporary_directory)
            skills_dir = repository_root / "skills"
            for filename in ("README.md", "README.ko.md"):
                (repository_root / filename).write_text(
                    "# Catalog\n\n<!-- skills:start -->\n<!-- skills:end -->\n",
                    encoding="utf-8",
                )

            create_skill(
                behavior="tiny-yell",
                locale="ko",
                description="Turn ordinary prose into a tiny yell.",
                instructions=["Replace ordinary prose with a tiny yell."],
                example_input="안녕하세요",
                example_output="꺅!",
                family_description_en="A family of tiny yelling skills.",
                family_description_ko="작게 소리치는 스킬 패밀리입니다.",
                skills_dir=skills_dir,
            )

            catalog = (repository_root / "README.md").read_text(encoding="utf-8")
            self.assertIn(
                "$skill-installer install "
                "https://github.com/ium-mui/stupid-skills/tree/main/skills/"
                "tiny-yell/stupid-tiny-yell-ko",
                catalog,
            )


if __name__ == "__main__":
    unittest.main()
