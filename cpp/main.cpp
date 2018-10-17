#include <iostream>
#include "Eigen/Dense"
#include <vector>
#include <cmath>
#include <unistd.h>


#define DT 0.001
#define G 1

using namespace Eigen;
using namespace std;

typedef Vector3d v3d;

v3d acceleration(const vector<v3d> &pos, const vector<double> &mass, int i)
{
    v3d acc;

    for (int j = 0; j<pos.size(); ++j)
    {
        if (i == j) continue;
        v3d d = pos[j] - pos[i];
        acc += G * mass[j] * (d)/pow(d.norm(), 3);
    }
    return acc;
}

void euler_step(vector<v3d> &pos, vector<v3d> &vel, vector<v3d> &acc, const vector<double> &mass)
{
    u_long n_stars = pos.size();
    vector<v3d> n_pos(n_stars, v3d());
    vector<v3d> n_vel(n_stars, v3d());
    vector<v3d> n_acc(n_stars, v3d());
#pragma omp parallel for
    for (int i = 0; i<pos.size(); ++i)
    {
        n_acc[i] = acceleration(pos, mass, i);
        n_pos[i] = pos[i] + vel[i]*DT + 1/2 * acc[i]*pow(DT, 2);
        n_vel[i] = vel[i] + 1/2 * (acc[i] + n_acc[i]) * DT;
    }
    pos = n_pos;
    vel = n_vel;
    acc = n_acc;
}


int main()
{
    u_long n_stars = 100;
    vector<v3d> pos(n_stars, v3d::Random());
    vector<v3d> vel(n_stars, v3d::Random());
    vector<v3d> acc(n_stars, v3d());
    vector<double> mass(1000, 1);

    for (int epoch = 0; epoch<200; ++epoch)
    {
        euler_step(pos, vel, acc, mass);
        cout << epoch << endl;
    }

    return 0;
}