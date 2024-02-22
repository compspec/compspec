#include <iostream>

namespace Example
{
    double Add(double a, double b, double c)
    {
        return a + b + c;
    }

    double Remove(double a)
    {
        return a;
    }

    double Change(double a, int c)
    {
        return a * c;
    }

    int ReturnChange(double a, double b)
    {
        return a + b;
    }
    void ReturnRemove(double a, double b)
    {
        std::cout << a;
    }
}
