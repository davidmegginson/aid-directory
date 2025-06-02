VENV=.venv/bin/activate
INPUTS_DIR=../inputs
TAXONOMIES_DIR=${INPUTS_DIR}/taxonomies
OUTPUTS_DIR=../outputs
SCRIPTS_DIR=scripts/
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

import: ${SCRIPTS_DIR}/import-org-data.py ${VENV}
	. ${VENV} && python -m scripts.import-org-data

run-app:
	. ${VENV} && python -m flask --app aid_directory --debug run

load-taxonomies:
	. ${VENV} && python -m scripts.import-iati-taxonomy Countries ${TAXONOMIES_DIR}/Country.json
	. ${VENV} && python -m scripts.import-iati-taxonomy OrgRoles ${TAXONOMIES_DIR}/OrganisationRole.json
	. ${VENV} && python -m scripts.import-iati-taxonomy OrgTypes ${TAXONOMIES_DIR}/OrganisationType.json
	. ${VENV} && python -m scripts.import-iati-taxonomy SectorVocabularies ${TAXONOMIES_DIR}/SectorVocabulary.json
	. ${VENV} && python -m scripts.import-iati-taxonomy Sectors ${TAXONOMIES_DIR}/Sector.json 1
	. ${VENV} && python -m scripts.import-iati-taxonomy Sectors ${TAXONOMIES_DIR}/SectorCategory.json 2
	. ${VENV} && python -m scripts.import-iati-taxonomy Sectors ${TAXONOMIES_DIR}/UNSDG-Goals.json 7
	. ${VENV} && python -m scripts.import-iati-taxonomy Sectors ${TAXONOMIES_DIR}/UNSDG-Targets.json 8
	. ${VENV} && python -m scripts.import-iati-taxonomy Sectors ${TAXONOMIES_DIR}/Humanitarian-Clusters.json 10

venv: ${VENV}

clean:
	rm -rf .venv ${OUTPUTS_DIR}/*.csv

${OUTPUTS_DIR}/orgs.csv: ${SCRIPTS_DIR}/iati-extract.py ${METADATA} ${VENV}
	mkdir -p ${OUTPUTS_DIR}
	. ${VENV} && python -m scripts.iati-extract > $@

${OUTPUTS_DIR}/orgs-ref.csv: ${SCRIPTS_DIR}/build-reference-table.py ../inputs/all_org_variants_expanded.csv ${VENV}
	. ${VENV} && python -m scripts.build-reference-table > $@

${OUTPUTS_DIR}/orgs-norm.csv: ${SCRIPTS_DIR}/normalise-orgs.py ${OUTPUTS_DIR}/orgs-variants.csv ${VENV}
	. ${VENV} && python -m scripts.normalise-orgs > $@

${OUTPUTS_DIR}/relationships.csv: ${SCRIPTS_DIR}/get-relationships.py ${OUTPUTS_DIR}/orgs-norm.csv ${VENV}
	. ${VENV} && python -m scripts.get-relationships < ${OUTPUTS_DIR}/orgs-norm.csv > $@

${VENV}: requirements.txt
	python3 -m venv .venv && . ${VENV} && pip3 install -r requirements.txt

tags:
	find . -name '*.py' -o -name '*.html' | xargs etags
