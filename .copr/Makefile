.PHONY: srpm

srpm:
	rpmbuild -bs "$(spec)" \
		--define "_sourcedir $(CURDIR)/sources" \
		--define "_srcrpmdir $(outdir)"
