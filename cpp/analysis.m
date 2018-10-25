clear; close all; clc;

sim = csvread('simulation.csv');
sim = sim(:, 1:end-1);
n_stars = size(sim,2)/7;
initial = reshape(sim(1,:), 7, n_stars)';
figure;
for epoch = 1:size(sim,1)
    status = reshape(sim(epoch,:), 7, n_stars)';
    scatter3(status(:,1), status(:,2), status(:,3), 2, 'b');
    axis([1.5*min(initial(:,1)), 1.5*max(initial(:,1)), 1.5*min(initial(:,2)), 1.5*max(initial(:,2)), -1, 1])
    title(['Epoch ' num2str(epoch)])
    pause(0.01);
end