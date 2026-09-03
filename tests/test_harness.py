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
                family_description_en="A family of tiny yelling skills.",
                family_description_ko="작게 소리치는 스킬 패밀리입니다.",
                skills_dir=skills_dir,
            )
            self.assertEqual(output.parent.name, "stupid-tiny-yell-ko")
            self.assertEqual(output.parent.parent.name, "tiny-yell")
            self.assertTrue((output.parent.parent / "README.md").is_file())
            self.assertTrue((output.parent.parent / "README.ko.md").is_file())
            self.assertIn(
                "stupid-tiny-yell-ko",
                (output.parent.parent / "README.md").read_text(encoding="utf-8"),
            )
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
                family_description_en="A family of beeping skills.",
                family_description_ko="삐 소리를 내는 스킬 패밀리입니다.",
                skills_dir=skills_dir,
            )
            create_skill(**arguments)
            with self.assertRaises(FileExistsError):
                create_skill(**arguments)

    def test_flat_skill_layout_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skills_dir = Path(temporary_directory) / "skills"
            flat_skill = skills_dir / "stupid-beep-ko"
            flat_skill.mkdir(parents=True)
            (flat_skill / "SKILL.md").write_text(
                '---\nname: "stupid-beep-ko"\ndescription: "Beep."\n---\n',
                encoding="utf-8",
            )
            self.assertNotEqual(validate(skills_dir), [])

    def test_language_neutral_skill_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skills_dir = Path(temporary_directory) / "skills"
            output = create_skill(
                behavior="shrug",
                locale=None,
                description="Reply with a language-neutral shrug.",
                instructions=["Reply with the shrug token."],
                example_input="Anything",
                example_output="¯\\_(ツ)_/¯",
                family_description_en="A family of shrugging skills.",
                family_description_ko="어깨를 으쓱하는 스킬 패밀리입니다.",
                skills_dir=skills_dir,
            )
            self.assertEqual(output.parent.name, "stupid-shrug")
            self.assertEqual(validate(skills_dir), [])

    def test_family_without_bilingual_readmes_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skills_dir = Path(temporary_directory) / "skills"
            skill_dir = skills_dir / "beep" / "stupid-beep-ko"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                '---\nname: "stupid-beep-ko"\ndescription: "Beep."\n---\n',
                encoding="utf-8",
            )
            errors = validate(skills_dir)
            self.assertTrue(any("README.md" in error for error in errors))
            self.assertTrue(any("README.ko.md" in error for error in errors))

    def test_stale_family_catalog_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skills_dir = Path(temporary_directory) / "skills"
            output = create_skill(
                behavior="blink",
                locale="en-us",
                description="Reply with a blink.",
                instructions=["Reply with one blink."],
                example_input="Hello",
                example_output="blink",
                family_description_en="A family of blinking skills.",
                family_description_ko="눈을 깜빡이는 스킬 패밀리입니다.",
                skills_dir=skills_dir,
            )
            readme = output.parent.parent / "README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8").replace(
                    "<!-- variants:end -->",
                    "- [`stupid-blink-ko`](stupid-blink-ko)\n<!-- variants:end -->",
                ),
                encoding="utf-8",
            )
            self.assertTrue(any("variant catalog" in error for error in validate(skills_dir)))


if __name__ == "__main__":
    unittest.main()
