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

run-app:
	. .venv/bin/activate && python -m flask --app aid_directory --debug run

relationships: ${OUTPUTS_DIR}/relationships.csv

orgs: ${OUTPUTS_DIR}/orgs.csv

venv: .venv/bin/activate

clean:
	rm -rf .venv ${OUTPUTS_DIR}/*.csv

${OUTPUTS_DIR}/orgs.csv: venv extract/iati-extract.py ${METADATA}
	mkdir -p ${OUTPUTS_DIR}
	. .venv/bin/activate && python extract/iati-extract.py > $@

${OUTPUTS_DIR}/relationships.csv: ${OUTPUTS_DIR}/orgs.csv venv get-relationships.py
	. .venv/bin/activate && python get-relationships.py < $< > $@

.venv/bin/activate: requirements.txt
	python3 -m venv .venv && . .venv/bin/activate && pip3 install -r requirements.txt

tags:
	find . -name '*.py' -o -name '*.html' | xargs etags
