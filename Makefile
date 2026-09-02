.PHONY: new-skill validate test check

new-skill:
	python3 scripts/new_skill.py

validate:
	python3 scripts/validate_skills.py

test:
	python3 -m unittest discover -s tests -v

check: validate test
