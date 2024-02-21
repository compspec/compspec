LIBS = ./lib

all: compile

compile: $(LIBS)/*
	for dir in $^ ; do \
		echo "Building" $${dir} ; \
		$(MAKE) -C $${dir}/v1; \
		$(MAKE) -C $${dir}/v2; \
	done
