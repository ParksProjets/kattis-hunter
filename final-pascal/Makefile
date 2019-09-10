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

# Object directory and target executable.
OBJDIR := objects
TARGET := answer

# Base source file and temporary source file.
BASESRC := base.pas
TMPSRC := finalcode.pas

# Cache file to use and target scores.
CACHE := ../cache.json
SCORES := 23,10,0,0,0,0


# Compile all source files.
.PHONY: all run clean
all: $(OBJDIR)/$(TARGET)


# Build the temporary source file.
$(OBJDIR)/$(TMPSRC): $(BASESRC)
	@mkdir -p $(OBJDIR)
	$(PYTHON) khpascal $(SCORES) -c $(CACHE) -i $< -o $@

# Build final COBOL executable.
$(OBJDIR)/$(TARGET): $(OBJDIR)/$(TMPSRC)
	$(FPC) -o$@ $(CFLAGS) $<


# Delete all generated objects.
clean:
	rm -rf $(OBJDIR)
