# Executables
CC := afl-clang-fast
RM := rm -f

# Compiler/linker flags
CFLAGS  :=
LDFLAGS :=
LDLIBS  :=

# Sources/targets
sources := solveme.c
targets := $(sources:.c=)

.PHONY: default all clean

default: all
all: $(targets)

clean:
	$(RM) $(targets)
