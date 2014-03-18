MAGMA = ~/git/magma/bin/magma

TESTS = pico.xdl 

# testseq.xdl testlogic.xdl testarith.xdl

export PYTHONPATH=..

.PHONY: test gold clean

test: $(TESTS)

gold:
	for f in $(TESTS); do \
	        cp $$f $$f.gold; \
	done

clean: 
	rm -f *.pyc *.bit *.pcf *.xdl
	make -C build clean

%.xdl: %.py a.mem
	rm -fr $*.pcf $*.xdl
	${MAGMA} -o $@ -p $*.pcf $*
	if [ -e $@.gold ] ; then \
	    diff $@ $@.gold ; \
	fi

%.bit: %.xdl
	cp $< build/fpga.xdl
	cp $*.pcf build/fpga.pcf
	make -C build
	cp build/test.bit $@
