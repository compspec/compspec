struct A {
 int x;
};

struct B {
 int y;
};

struct C {
 int z;
};

struct D: A, B, C {
 int d;
};

int func(struct A a, struct B * b, struct C c, struct D d) {
  return 1;
}

int changed_order(struct B b, struct A a) {
  return 1;
}

