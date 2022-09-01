node1:
	python3 PoRNode.py --port 5000

node2:
	python3 PoRNode.py --port 5001

goenv: # activate local enviroment
	. ./env/bin/activate

requirements:
	pip3 freeze > requirements.txt

installrequirements:
	pip3 install -r requirements.txt