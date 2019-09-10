# 
# Build the Pascal answer program.
# 
# Copyright (C) 2019, Guillaume Gonnet
# This project is under the MIT license.


# GNU tools and others.
PYTHON := python3
FPC := fpc

# COBOL configuration.
PFLAGS += -O2 -XS -Xt

# TODO.
BASE := base.pas
OBJDIR := objects
TARGET := answer


# Compile all source files.
.PHONY: all run clean
all: $(OBJDIR)/$(TARGET)


# Build final COBOL executable.
$(OBJDIR)/$(TARGET): $(BASE)
	@mkdir -p $(OBJDIR)
	$(FPC) -o$@ $(CFLAGS) $<


# Delete all generated objects.
clean:
	rm -rf $(OBJDIR)
