#include <unistd.h>

static int inline_that()
{
  return getpid();
}

int main(int argc, char *argv[])
{
  return inline_that();
}
