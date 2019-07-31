clean: 
	rm dist/*
test:
	tox
release: clean
	@python setup.py sdist bdist_wheel
	@twine upload dist/*

.PHONY: release
