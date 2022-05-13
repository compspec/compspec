typedef int foo;

struct N {
  struct N * next;
  foo left;
  foo right;
  char extra;  // change this to short
};

int fun(struct N x, struct N * z) {
  return &x == z;
}

