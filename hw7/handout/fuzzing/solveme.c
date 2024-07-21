#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_CHARS 20

int foo(char *buf) {
    if (buf[6] + 27 < buf[2]) {
        if (!feof(stdin)) {
            return 1;
        } else {
            return 42;
        }
    } else if (buf[1] < 'M') {
        return 1;
    }
    if (buf[4] > 52) {
        return 42;
    } else {
        if (buf[1] >= 0 && buf[1] < 10) {
        reset:
            memset(buf, 0, MAX_CHARS);
            return 1;
        }
        if (buf[3] + buf[5] > buf[4] + 41) {
            goto reset;
        }
        if (buf[1] <= 79) {
            puts(
                "Congrats, you found a secret input that crashes the program!");
            abort();
        }
    }
    return 0;
}

int main(int argc, char *argv[]) {
    char buf[MAX_CHARS] = {0};
start:
    if (read(STDIN_FILENO, buf, MAX_CHARS - 1) <= 0) {
        goto end;
    }

    if (buf[0] == 'C' && buf[2] > buf[0]) {
        if (buf[5] > '9') {
            if (buf[6] <= '9') {
                buf[5] = buf[6] - 2;
            }
        } else {
            if (buf[3] < 0 && buf[6] < 0) {
                buf[3] = -buf[3];
                buf[6] = -buf[6];
            } else {
                if (buf[1] >= buf[3] + 34 && buf[4] > 51) {
                    if (buf[6] >= 51) {
                        for (size_t i = 0; i < MAX_CHARS; i++) {
                            if (!isascii(buf[i])) {
                                break;
                            }
                            printf("%c", buf[i]);
                        }
                        printf("\n");
                    } else {
                        if (buf[1] > 0 && buf[1] < 32) {
                            goto end;
                        }
                        if (buf[3] > 45) {
                            goto end;
                        }
                        if (buf[5] <= buf[4] - 4 && buf[4] < 54
                            && buf[6] >= 50) {
                            if (buf[4] <= ' ') {
                                puts("You've made it quite far already!");
                            } else {
                                if (buf[6] >= buf[4] - buf[5] - 2) {
                                    if (buf[5] >= '0') {
                                        if (buf[5] >= buf[0] - 18) {
                                            char tmp = buf[5];
                                            buf[5] = buf[0];
                                            buf[0] = buf[5];
                                        } else {
                                            if (buf[4] > buf[0] - 16) {
                                                if (buf[2] < 77) {
                                                    while (buf[2] < 77) {
                                                        buf[2]++;
                                                    }
                                                } else {
                                                    int i = foo(buf);
                                                    switch (i) {
                                                        case 1:
                                                            goto start;
                                                        case 42:
                                                            goto end;
                                                        default:
                                                            return i;
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
end:
    printf("%s\n", buf);
    return 0;
}
