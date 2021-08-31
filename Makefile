# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = doc-src
BUILDDIR      = doc-out
PYPATH	      = $(shell pwd)/lib

# Put it first so that "make" without argument is like "make help".
.PHONY: all html github clean

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).

all:
	make github
	python3 setup.py sdist

html: Makefile
	env PYTHONPATH="$(PYPATH)" $(SPHINXBUILD) -M html \
		"$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

github: Makefile
	#cd lib && sphinx-apidoc -T -o ../doc-src  influxdb2 && cd ..
	rm -rf doc-src doc-out docs
	env PYTHONPATH="$(PYPATH)" sphinx-apidoc \
		--extensions sphinx.ext.napoleon,sphinx_autodoc_typehints \
		-M -e -T -A "Hoplite Industries, Inc." \
		-V 1.0 -R 1.0.1 -H InfluxDB2 -F  -o doc-src  lib
	sed -i "/sphinx-quickstart on/d" doc-src/index.rst
	sed -i "/sphinx.ext.viewcode/d" doc-src/conf.py
	env PYTHONPATH="$(PYPATH)" $(SPHINXBUILD) -M html \
		"$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	mv doc-out/html docs
	touch docs/.nojekyll
clean:
	$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	rm -rf build
	rm -rf dist
	rm -rf doc-out
	rm -rf lib/*.egg-info
