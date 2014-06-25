MAGMA=~/git/magma/bin/magma
DEVICE=xc3s250e

TESTS = pico.xdl

.PHONY: test gold clean

test: $(TESTS)

gold:
	for f in $(TESTS); do \
		cp $$f $$f.gold; \
	done

clean:
	rm -f *.pyc *.xdl *.pcf *.bit
	make -C build clean

%.xdl: %.py
	rm -f $*.pcf $*.xdl
	${MAGMA} -d ${DEVICE} -o $@ -p $*.pcf $*
	if [ -e $@.gold ] ; then \
		diff $@ $@.gold ; \
	fi

%.bit: %.xdl
	make -C build clean
	cp $< build/fpga.xdl
	cp $*.pcf build/fpga.pcf
	make -C build
	cp build/test.bit $@
