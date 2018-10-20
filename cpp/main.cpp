#include <iostream>
#include "Eigen/Dense"
#include <vector>
#include <cmath>
#include <unistd.h>
#include <boost/tokenizer.hpp>
#include <fstream>


#define DT 0.001
#define G 1

using namespace Eigen;
using namespace std;
using namespace boost;

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

void read_universe(const char* path, vector<v3d> &pos, vector<v3d> &vel, vector<double> &mass)
{
    ifstream file(path);
    string star;
    while(getline(file, star))
    {
        char_separator<char> sep(",");
        tokenizer< char_separator<char> > tokens(star, sep);
        auto it = tokens.begin();
        pos.emplace_back(v3d(stod(*(it++)), stod(*(it++)), stod(*(it++))));
        vel.emplace_back(v3d(stod(*(it++)), stod(*(it++)), stod(*(it++))));
        mass.emplace_back(stod(*it)); //TODO fix mass being truncated to 1
    }
//    for(int i = 1; i < pos.size(); i++)
//    {
//        cout << pos[i][0] << "," << pos[i][1] << "," << pos[i][2] <<
//        "," << vel[i][0] << "," << vel[i][1] << "," << vel[i][2] <<
//        "," << mass[i] << endl;
//    }

}

void write_progress(ofstream &file, vector<vector<v3d>> &poses, vector<vector<v3d>> &vels,
        vector<vector<double>> &masses)
{
    u_long n_stars = poses[0].size();
    for(int step = 0; step < poses.size(); step++)
    {
        for (int star = 0; star<n_stars; ++star)
        {
            file << poses[step][star][0] << "," << poses[step][star][1] << "," << poses[step][star][2] << ","
            << vels[step][star][0] << "," << vels[step][star][1] << "," << vels[step][star][2] << ","
            << masses[step][star] << ",";
        }
        file << endl;
    }
}


int main()
{
    vector<v3d> pos;
    vector<v3d> vel;
    vector<double> mass(1000, 1);
    read_universe("../../universe.csv", pos, vel, mass);
    vector<v3d> acc(pos.size());

    // Progress vectors, to store steps
    vector<vector<v3d>> prog_pos;
    vector<vector<v3d>> prog_vel;
    vector<vector<double>> prog_mass;
    cout << "Started" << endl;
    ofstream file("../simulation.csv");
    time_t last_write = time(nullptr);
    for (int epoch = 0; epoch<200; ++epoch)
    {
        euler_step(pos, vel, acc, mass);
        prog_pos.push_back(pos);
        prog_vel.push_back(vel);
        prog_mass.push_back(mass);
        if (time(nullptr) - last_write > 120)
        {
            write_progress(file, prog_pos, prog_vel, prog_mass);
            last_write = time(nullptr);
            prog_pos.clear();
            prog_vel.clear();
            prog_mass.clear();
        }
        cout << epoch << endl;
    }
    write_progress(file, prog_pos, prog_vel, prog_mass);
    cout << "Finished" << endl;

    return 0;
}
