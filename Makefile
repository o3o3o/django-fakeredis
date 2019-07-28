test:
	tox
release:
	@python setup.py sdist bdist_wheel
	@twine upload dist/*

.PHONY: release
