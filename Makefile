test:
	bash -c 'cd tests && exec make'

clean:
	find . -type f -name \*.pyc -exec rm '{}' ';'
