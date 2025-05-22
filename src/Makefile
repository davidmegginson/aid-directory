VENV=.venv/bin/activate
INPUTS_DIR=../inputs
TAXONOMIES_DIR=${INPUTS_DIR}/taxonomies
OUTPUTS_DIR=../outputs
METADATA=${TAXONOMIES_DIR}/OrganisationRole.json \
  ${TAXONOMIES_DIR}/OrganisationType.json \
  ${TAXONOMIES_DIR}/Country.json \
  ${TAXONOMIES_DIR}/SectorCategory.json \
  ${TAXONOMIES_DIR}/SectorVocabulary.json \
  ${TAXONOMIES_DIR}/SectorVocabulary.json \
  ${TAXONOMIES_DIR}/UNSDG-Goals.json \
  ${TAXONOMIES_DIR}/UNSDG-Targets.json \
  ${TAXONOMIES_DIR}/Humanitarian-Clusters.json

all: run-app

orgs: ${OUTPUTS_DIR}/orgs.csv

orgs-norm: ${OUTPUTS_DIR}/orgs-norm.csv

ref: ${OUTPUTS_DIR}/orgs-ref.csv

relationships: ${OUTPUTS_DIR}/relationships.csv

run-app:
	. ${VENV} && python -m flask --app aid_directory --debug run

venv: ${VENV}

clean:
	rm -rf .venv ${OUTPUTS_DIR}/*.csv

${OUTPUTS_DIR}/orgs.csv: venv iati-extract.py ${METADATA}
	mkdir -p ${OUTPUTS_DIR}
	. ${VENV} && python iati-extract.py > $@

${OUTPUTS_DIR}/orgs-ref.csv: build-reference-table.py ../inputs/all_org_variants_expanded.csv venv
	. ${VENV} && python build-reference-table.py > $@

${OUTPUTS_DIR}/orgs-norm.csv: normalise-orgs.py ${OUTPUTS_DIR}/orgs-variants.csv venv
	. ${VENV} && python normalise-orgs.py > $@

${OUTPUTS_DIR}/relationships.csv: ${OUTPUTS_DIR}/orgs-norm.csv venv get-relationships.py
	. ${VENV} && python get-relationships.py < $< > $@

${VENV}: requirements.txt
	python3 -m venv .venv && . ${VENV} && pip3 install -r requirements.txt

tags:
	find . -name '*.py' -o -name '*.html' | xargs etags
