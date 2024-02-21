typedef int foo;

struct N {
  struct N * next;
  foo one;
  foo two;
};

int fun(struct N x, struct N * z) {
  return &x == z;
}
