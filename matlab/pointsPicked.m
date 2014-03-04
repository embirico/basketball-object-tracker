clear all; close all; clc;

% Constants
FT2MM = 304.8;

% Data points
pp = [534.2759, 432.3008, 310.1432, 687.2386, 988.9149;
      225.0643, 297.2967, 383.3382, 417.3299, 254.8071];

% In feet
pw = [0,   0,  0, 19, 28;  % x
      50, 17, 33, 17, 50;  % y
      0,   0,  0,  0,  0]; % z
pw = pw * FT2MM;

% Solve H
A = zeros(8, 8);
B = zeros(8,1);
for i = 1:4
  xp = pp(1,i);
  yp = pp(2,i);
  xw = pw(1,i);
  yw = pw(2,i);
  
  A(1+2*i,:) = [xp, yp, 1, 0, 0, 0, xp*xw, yp*xw];
  A(2+2*i,:) = [0, 0, 0, xp, yp, 1, xp*yw, yp*yw];

  B(1+2*i) = xw;
  B(2+2*i) = yw;
end

hList = [pinv(A) * B; 1];

H = reshape(hList, 3, 3)'

% Solve subvariables
% toGetHp = [1, 0, -1280/2;
%            0, 1, -720/2;
%            0, 0, 1];
toGetHp = [1, 0, 0;
           0, 1, 0;
           0, 0, 1];
Hp = toGetHp * H

f = sqrt(-(Hp(1,1)*Hp(1,2) + Hp(2,1)*Hp(2,2)) / (Hp(3,1)*Hp(3,2)))