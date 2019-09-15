# 
# Build the Pascal answer program.
# 
# Copyright (C) 2019, Guillaume Gonnet
# This project is under the MIT license.


# GNU tools and others.
PYTHON := python3
FPC := fpc

# Pascal compiler configuration.
PFLAGS += -O2 -XS -Xt

# Object directory and target executable.
OBJDIR := objects
TARGET := answer

# Base source file and temporary source file.
BASESRC := base.pas
TMPSRC := finalcode.pas

# Cache file to use and default target scores.
CACHE := ../cache.json
SCORES := 111,111,111,111,111,111


# Compile all source files.
.PHONY: all code run clean
all: $(OBJDIR)/$(TARGET)

# Generate only the Pascal code.
code: $(OBJDIR)/$(TMPSRC)


# Build the temporary source file.
$(OBJDIR)/$(TMPSRC): $(BASESRC) $(CACHE)
	@mkdir -p $(OBJDIR)
	$(PYTHON) khpascal $(SCORES) -c $(CACHE) -i $< -o $@

# Build final COBOL executable.
$(OBJDIR)/$(TARGET): $(OBJDIR)/$(TMPSRC)
	$(FPC) -o$@ $(CFLAGS) $<


# Delete all generated objects.
clean:
	rm -rf $(OBJDIR)
