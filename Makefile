.PHONY: test demo up golden
test:   ; cd backend && python -m pytest -q
demo:   ; cd backend && python -m app.cli_demo
golden: ; cd backend && python ../mlops/evaluate_golden.py ../mlops/golden_dataset/sample_PLACEHOLDER.csv
up:     ; cp -n .env.example .env; docker compose up --build
