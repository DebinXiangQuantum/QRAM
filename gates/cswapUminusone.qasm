OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
rx(pi) q[0];
rz(2.1666156231653746) q[1];
rx(2.96705972839036) q[1];
rz(2.1666156231653746) q[2];
rx(pi/2) q[2];
cz q[1],q[2];
rz(pi) q[1];
rx(3*pi/4) q[1];
rz(-pi) q[2];
rx(4*pi/9) q[2];
cz q[1],q[2];
rx(2.3409883975982666) q[1];
cz q[0],q[1];
rx(pi) q[0];
rz(pi) q[0];
rz(pi) q[1];
rx(0.8006000518798828) q[1];
cz q[1],q[2];
rz(-pi) q[1];
rx(3*pi/4) q[1];
rx(4*pi/9) q[2];
cz q[1],q[2];
rx(pi/18) q[1];
rz(-2.1666156231653746) q[1];
rx(pi/2) q[2];
rz(0.9749770304244186) q[2];
