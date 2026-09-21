.PHONY: validate sync init

validate:
	python scripts/validate_repo.py
	python -m unittest discover -s tests -p 'test_*.py'

sync:
	python scripts/sync_official_spec.py --sync
	python scripts/validate_repo.py

init:
	@test -n "$(PROJECT)" || (echo "PROJECT is required" && exit 2)
	@test -n "$(COMMIT)" || (echo "COMMIT is required" && exit 2)
	python scripts/init_assessment.py --project "$(PROJECT)" --commit "$(COMMIT)" $(ARGS)
