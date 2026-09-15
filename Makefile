.PHONY: list install new-skill sync-catalog validate test check

list:
	python3 scripts/stupid_skills.py list

install:
	@test -n "$(SKILL)" || (echo "usage: make install SKILL=stupid-<behavior>[-<locale>]" >&2; exit 2)
	python3 scripts/stupid_skills.py install "$(SKILL)"

new-skill:
	python3 scripts/new_skill.py

sync-catalog:
	python3 scripts/stupid_skills.py sync

validate:
	python3 scripts/validate_skills.py

test:
	python3 -m unittest discover -s tests -v

check: validate test
