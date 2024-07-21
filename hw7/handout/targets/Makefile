# Executables
CC := i686-linux-gnu-gcc
LD := $(CC)
RM := rm -f

# Compiler/linker flags
CFLAGS  := -ggdb -fno-stack-protector -z execstack -fno-pie -no-pie -mpreferred-stack-boundary=2 -static
LDFLAGS := $(CFLAGS)
LDLIBS  :=

# Sources/targets
sources := target1.c target2.c target3.c target4.c
objects := $(sources:.c=.o)
targets := $(sources:.c=)

.PHONY: default all setuid clean

default: all
all: $(targets)

setuid: $(targets)
ifeq ($(shell id -u),0)
	chown root:root $(targets)
	chmod 4755 $(targets)
else
	@echo "'make setuid' must be run as root -- use su or a root login!"
endif

clean:
	$(RM) $(targets) $(objects)
