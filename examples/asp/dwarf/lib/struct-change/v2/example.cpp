typedef int foo;

struct N {
  struct N * next;
  foo left;
  foo right;
  short extra;
};

int fun(struct N x, struct N * z) {
  return &x == z;
}
