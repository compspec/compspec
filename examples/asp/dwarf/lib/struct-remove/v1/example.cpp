typedef int foo;

struct N {
  struct N * next;
  foo remains;
  foo removed;
};

int fun(struct N x, struct N * z) {
  return &x == z;
}

