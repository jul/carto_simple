DEST=build


all: serve

serve: wo_notes
	cd ${DEST} && python -m SimpleHTTPServer

pygment:
	mkdir -p ${DEST}/html
	touch ${DEST}/html/gen_map.html ; \
	pygmentize  -f html -l python -O  style=colorful,linenos=1,full -o ${DEST}/html/gen_map.html ./gen_map.py ; 

html:
	mkdir -p ${DEST}/html ; \
	cp assets/html/* ${DEST}/html/

with_notes: pygment html
	@echo "Passetsentation with notes (wo_notes else)" ; \
	hovercraft carto.rst ${DEST}  -c assets/custom.css ;  \

clean:
	rm -rf ${DEST}/* 

wo_notes: pygment html
	hovercraft carto.rst ${DEST} -n -c assets/custom.css ;  \
	echo "Passetsentation with notes ready to be served in ${DEST}"
