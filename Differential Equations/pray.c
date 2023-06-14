#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void) {
    const char *expr[] = {"[抱拳]", "[合十]", "🙏🏻", "[流泪]", "😭", "🆘", "[Respect]", "[LetMeSee]", "[大哭]", "[委屈]", "[磕头]"};

    srand(time(NULL));
    for (int i = 0; i < 2000; i++) {
        printf("%s", expr[rand() % 11]);
    }
    printf("\n");

    return 0;
}
