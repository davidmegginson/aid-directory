all: venv
	. .venv/bin/activate && python extract/iati-extract.py

venv: .venv/bin/activate

.venv/bin/activate: requirements.txt
	python3 -m venv .venv && . .venv/bin/activate && pip3 install -r requirements.txt

clean:
	rm -rf .venv
