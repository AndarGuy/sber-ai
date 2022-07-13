using System.Collections.Generic;
using System;
public class CannonAI : ICannonAI {
    
    double y = 0;
    double a, b, c;
    int counter = 0;
    double[] ex_degrs = {45, 75, 90};
    Dictionary<double, double> shoots = new Dictionary<double, double>(3);

    public void SetTarget(double distance) {
        y = distance;
    }

    public double GetShootAngle() {
        if (counter < 3) {
            return ex_degrs[counter];
        } else if (counter == 3) {
            double x1 = ex_degrs[0], x2 = ex_degrs[1], x3 = ex_degrs[2];
            double y1 = shoots[x1], y2 = shoots[x2], y3 = shoots[x3];
            a = ((-x1) * y2 + x1 * y3 + x2 * y1 - x2 * y3 - x3 * y1 + x3 * y2) / ((x2 - x1) * (x3 - x1) * (x2 - x3));
            b = (x1 * x1 * y2 - x1 * x1 * y3 - x2 * x2 * y1 + x2 * x2 * y3 + x3 * x3 * y1 - x3 * x3 * y2) / ((x1 - x2) * (x1 - x3) * (x2 - x3));
            c = (x1 * x1 * x2 * y3 + x1 * x1 * (-x3) * y2 - x1 * x2 * x2 * y3 + x1 * x3 * x3 * y2 + x2 * x2 * x3 * y1 - x2 * x3 * x3 * y1) / ((x1 - x2) * (x1 - x3) * (x2 - x3));
            double x = (-b - Math.Sqrt(b*b-4*a*(c-y))) / (2*a);
            return x;
        } else {
            double x = (-b - Math.Sqrt(b*b-4*a*(c-y))) / (2*a);
            return x;
        }
    }

    public void FeedbackHitDistance(double distance) {
        if (counter < 3) {
            shoots.Add(ex_degrs[counter], distance);
        }

        counter += 1;
    }
}
