all: serve

serve: wo_notes
	cd hover && python -m SimpleHTTPServer

pygment:
	mkdir -p hover/html
	touch hover/html/gen_map.html ; \
	pygmentize  -f html -l python -O  style=colorful,linenos=1,full -o hover/html/gen_map.html ~/src/jul/src/gen_map.py ; 

html:
	mkdir -p hover/html ; \
	cp assets/html/* hover/html/

with_notes: pygment html
	@echo "Passetsentation with notes (wo_notes else)" ; \
	hovercraft carto.rst hover  -c assets/custom.css ;  \

clean:
	rm -rf hover/* 

wo_notes: pygment html
	hovercraft carto.rst hover -n -c assets/custom.css ;  \
	echo "Passetsentation with notes ready to be served in hover"
