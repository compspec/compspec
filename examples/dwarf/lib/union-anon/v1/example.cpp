struct vector3 {
  union {
    struct {
      float x;
      float y;
      float z;
    };
    float v[3];
  };
};

int fun(struct vector3 x, struct vector3 * y) {
  return &x == y;
}

