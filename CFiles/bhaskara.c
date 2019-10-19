#include <stdio.h>
#define _USE_MATH_DEFINES
#include <math.h>

double calculateFirstPart(double a, double b, double c) {
    double x = (b * b) + (-4 * (a * c));
    return x;
}

double calculatePositivePart(double a, double b, double c) {
    double x = (-b + (sqrt(calculateFirstPart(a, b, c)))) / 2 * a;
    return x;
}

double calculateNegativePart(double a, double b, double c) {
    double x = (-b - (sqrt(calculateFirstPart(a, b, c)))) / 2 * a;
    return x;
}

int main() {
    double a, b, c, x, y, z;
    scanf("%lf %lf %lf", &a, &b, &c);
    x = calculateFirstPart(a, b, c);
    y = calculatePositivePart(a, b, c);
    z = calculateNegativePart(a, b, c);
    if (x == 0 || x < 0) {
        printf("Negative number\n");
    } else {
        printf("%f\n", x);
        printf("%f\n", y);
        printf("%f\n", z);
    }
    return 0;
}

// x = (-b +- raiz de b^2 - 4ac )/ 2a