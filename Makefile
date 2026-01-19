\
PY := python

.PHONY: all synth extract transform features anomalies visualize test clean-db

all: synth

synth:
	$(PY) -m src.main --synthetic

extract:
	$(PY) -m src.main --stage extract --synthetic

transform:
	$(PY) -m src.main --stage transform

features:
	$(PY) -m src.main --stage features

anomalies:
	$(PY) -m src.main --stage anomalies

visualize:
	$(PY) -m src.main --stage visualize

test:
	pytest -q

clean-db:
	@rm -f commute.db
