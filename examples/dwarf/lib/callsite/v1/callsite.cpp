#include <unistd.h>

static int inline_this()
{
  return getpid();
}

int main(int argc, char *argv[])
{
  return inline_this();
}
