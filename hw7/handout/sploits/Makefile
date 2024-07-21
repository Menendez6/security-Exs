# Executables
CC := gcc
LD := $(CC)
RM := rm -f
CP := cp

# Compiler/linker flags
CFLAGS := -ggdb
LDFLAGS := $(CFLAGS)
LDLIBS :=

# Sources/targets
sources := sploit1.c sploit2.c sploit3.c sploit4.c
objects := $(sources:.c=.o)
targets := $(sources:.c=)

.PHONY: default all clean

default: all
all: $(targets)

clean:
	$(RM) $(targets) $(sources:.c=.o)

# Dependencies
$(objects): shellcode.h
