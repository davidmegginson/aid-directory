INPUTS_DIR=../inputs
OUTPUTS_DIR=../outputs
METADATA=${INPUTS_DIR}/OrganisationRole.json \
  ${INPUTS_DIR}/OrganisationType.json \
  ${INPUTS_DIR}/Country.json \
  ${INPUTS_DIR}/SectorCategory.json \
  ${INPUTS_DIR}/SectorVocabulary.json


all: ${OUTPUTS_DIR}/orgs.csv

${OUTPUTS_DIR}/orgs.csv: venv extract/iati-extract.py ${METADATA}
	mkdir -p ${OUTPUTS_DIR}
	. .venv/bin/activate && python extract/iati-extract.py > ${OUTPUTS_DIR}/orgs.csv

show-org: venv
	. .venv/bin/activate && python show-org.py

venv: .venv/bin/activate

.venv/bin/activate: requirements.txt
	python3 -m venv .venv && . .venv/bin/activate && pip3 install -r requirements.txt

clean:
	rm -rf .venv ${OUTPUTS_DIR}/*.csv
