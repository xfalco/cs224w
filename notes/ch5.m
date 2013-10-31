%% Ch5.pdf notes
format compact

%% Example 5.1
M = [0 1/3 1/3 1/3; 1/2 0 0 1/2; 1 0 0 0; 0 1/2 1/2 0]';
v = ones(length(M),1)/length(M);
M*v
M*M*v
M^75*v    % v0 is the principal eigenvector of M

%% Example 5.3
M = [0 1/3 1/3 1/3; 1/2 0 0 1/2; 0 0 0 0; 0 1/2 1/2 0]';
M^10*v

%% Example 5.5
M = [0 1/3 1/3 1/3; 1/2 0 0 1/2; 0 0 1 0; 0 1/2 1/2 0]';
M^50*v

%% Example 5.6
b = 0.8;
v = ones(4,1)/4;
M = [0 1/3 1/3 1/3; 1/2 0 0 1/2; 0 0 1 0; 0 1/2 1/2 0]';
for i = 1:50
    v = b*M*v + (1-b).*ones(4,1)/length(v);
end

%% Example 5.10
b = 0.8;
v = [0/2 1/2 0/2 1/2]';
for i = 1:50
    v = b*M*v+(1-b)/2*[0 1 0 1]';
end

%% Example 5.12
R = [3/9 2/9 2/9 2/9]';
T = [54/210 59/210 38/210 59/210]';
(R-T)./R

%% Example 5.14
L = [0 1 1 1 0; 1 0 0 1 0; 0 0 0 0 1; 0 1 1 0 0; 0 0 0 0 0];
h = ones(5,1);
for i = 1:100
    a = L'*h;
    a = a ./ max(a);
    h = L*a;
    h = h ./ max(h);
end
h
a
