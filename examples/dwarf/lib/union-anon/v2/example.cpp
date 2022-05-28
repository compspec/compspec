union U {
  struct {
    float x;
    float y;
    float z;
  };
  float v[3];
};

struct vector3 {
   U u;
};

int fun(struct vector3 x, struct vector3 * y) {
  return &x == y;
}

