// Gmsh project created on Sat Oct 11 17:40:24 2025
//+
SetFactory("OpenCASCADE");

N_radial = 15;
N_downstream_x = 30;
N_outer_band = 4;
N_ring_outer = 7; p_ring_outer = 0.95;
N_ring_middle = 20; p_ring_middle = 0.95;
N_ring_inner = 15; 

N_injector_layers = 20;
N_domain_layers = 100;

Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {-0.25, 0, 0, 1.0};
//+
Point(3) = {0.25, 0, 0, 1.0};
//+
Point(4) = {0.25, 0.25, 0, 1.0};
//+
Point(5) = {0.25, -0.25, 0, 1.0};
//+
Point(6) = {-0.25, -0.25, 0, 1.0};
//+
Point(7) = {-0.25, 0.25, 0, 1.0};
//+
Point(8) = {0, 0.25, 0, 1.0};
//+
Point(9) = {0, -0.25, 0, 1.0};
//+
Line(1) = {1, 3};
//+
//+
Line(2) = {1, 8};
//+
Line(3) = {1, 9};
//+
Line(4) = {1, 2};
//+
Line(5) = {9, 5};
//+
Line(6) = {5, 3};
//+
Line(7) = {3, 4};
//+
Line(8) = {4, 8};
//+
Line(9) = {8, 7};
//+
Line(10) = {7, 2};
//+
Line(11) = {2, 6};
//+
Line(12) = {6, 9};
//+
Curve Loop(1) = {2, 9, 10, -4};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {8, -2, 1, 7};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {6, -1, 3, 5};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {3, -12, -11, -4};
//+
Plane Surface(4) = {4};
//+
Point(10) = {0.5, 0, -0, 1.0};
//+
Point(11) = {-0.5, 0, -0, 1.0};
//+
Point(12) = {0, 0.5, -0, 1.0};
//+
Point(13) = {0, -0.5, -0, 1.0};
//+
Line(13) = {9, 13};
//+
Line(14) = {3, 10};
//+
Line(15) = {8, 12};
//+
Line(16) = {2, 11};
//+
Point(14) = {0.3535533905932737, 0.3535533905932737, -0, 1.0};
//+
Point(15) = {-0.3535533905932737, 0.3535533905932737, -0, 1.0};
//+
Point(16) = {-0.3535533905932737, -0.3535533905932737, -0, 1.0};
//+
Point(17) = {0.3535533905932737, -0.3535533905932737, -0, 1.0};
//+
Line(17) = {4, 14};
//+
Line(18) = {5, 17};
//+
Line(19) = {6, 16};
//+
Line(20) = {7, 15};
//+
Circle(21) = {12, 1, 14};
//+
Circle(22) = {14, 1, 10};
//+
Circle(23) = {10, 1, 17};
//+
Circle(24) = {17, 1, 13};
//+
Circle(25) = {13, 1, 16};
//+
Circle(26) = {16, 1, 11};
//+
Circle(27) = {11, 1, 15};
//+
Circle(28) = {15, 1, 12};
//+
Curve Loop(5) = {28, -15, 9, 20};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {27, -20, 10, 16};
//+
Plane Surface(6) = {6};
//+
Curve Loop(7) = {16, -26, -19, -11};
//+
Plane Surface(7) = {7};
//+
Curve Loop(8) = {19, -25, -13, -12};
//+
Plane Surface(8) = {8};
//+
Curve Loop(9) = {13, -24, -18, -5};
//+
Plane Surface(9) = {9};
//+
Curve Loop(10) = {6, 14, 23, -18};
//+
Plane Surface(10) = {10};
//+
Curve Loop(11) = {7, 17, 22, -14};
//+
Plane Surface(11) = {11};
//+
Curve Loop(12) = {15, 21, -17, 8};
//+
Plane Surface(12) = {12};
//+
Point(18) = {-3, 0, 0, 1.0};
//+
Point(19) = {9, 0, 0, 1.0};
//+
Point(20) = {-3, 3.5, 0, 1.0};
//+
Point(21) = {-3, -3.5, 0, 1.0};
//+
Point(22) = {9, -3.5, 0, 1.0};
//+
Point(23) = {9, 3.5, 0, 1.0};
//+
Point(24) = {-2.5, 0, 0, 1.0};
//+
Point(25) = {2.5, 0, 0, 1.0};
//+
Point(26) = {0, 2.5, 0, 1.0};
//+
Point(27) = {0, -2.5, 0, 1.0};
//+
Point(28) = {1.7677669529663687, 1.7677669529663687, 0, 1.0};
//+
Point(29) = {-1.7677669529663687, 1.7677669529663687, 0, 1.0};
//+
Point(30) = {1.7677669529663687, -1.7677669529663687, 0, 1.0};
//+
Point(31) = {-1.7677669529663687, -1.7677669529663687, 0, 1.0};
//+
Line(29) = {14, 28};
//+
Line(30) = {10, 25};
//+
//+
Line(31) = {30, 17};
//+
Line(32) = {27, 13};
//+
Line(33) = {31, 16};
//+
Line(34) = {24, 11};
//+
Line(35) = {29, 15};
//+
Line(36) = {26, 12};
//+
Circle(37) = {26, 1, 28};
//+
Circle(38) = {28, 1, 25};
//+
Circle(39) = {25, 1, 30};
//+
Circle(40) = {30, 1, 27};
//+
Circle(41) = {27, 1, 31};
//+
Circle(42) = {31, 1, 24};
//+
Circle(43) = {24, 1, 29};
//+
Circle(44) = {29, 1, 26};
//+
Point(32) = {-3, 3, 0, 1.0};
//+
Point(33) = {-3, -3, 0, 1.0};
//+
Point(34) = {0, -3, 0, 1.0};
//+
Point(35) = {0, 3, 0, 1.0};
//+
Point(36) = {3, 3, 0, 1.0};
//+
Point(37) = {3, -3, 0, 1.0};
//+
Point(38) = {3, 0, 0, 1.0};
//+
Line(45) = {29, 32};
//+
Line(46) = {31, 33};
//+
Line(47) = {27, 34};
//+
Line(48) = {30, 37};
//+
Line(49) = {25, 38};
//+
Line(50) = {28, 36};
//+
Line(51) = {26, 35};
//+
Line(52) = {18, 32};
//+
Line(53) = {32, 35};
//+
Line(54) = {35, 36};
//+
Line(55) = {36, 38};
//+
Line(56) = {38, 37};
//+
Line(57) = {37, 34};
//+
Line(58) = {34, 33};
//+
Line(59) = {33, 18};
//+
Point(39) = {0, 3.5, 0, 1.0};
//+
Point(40) = {3, 3.5, 0, 1.0};
//+
Point(41) = {3, -3.5, 0, 1.0};
//+
Point(42) = {0, -3.5, 0, 1.0};
//+
Line(60) = {32, 20};
//+
Line(61) = {20, 39};
//+
Line(62) = {35, 39};
//+
Line(63) = {39, 40};
//+
Line(64) = {40, 36};
//+
Line(65) = {41, 37};
//+
Line(66) = {42, 34};
//+
Line(67) = {21, 33};
//+
Line(68) = {21, 42};
//+
Line(69) = {42, 41};
//+
Point(43) = {9, 3.0, 0, 1.0};
//+
Point(44) = {9, -3.0, 0, 1.0};
//+
Line(70) = {40, 23};
//+
Line(71) = {23, 43};
//+
Line(73) = {44, 22};
//+
Line(74) = {22, 41};
//+
Line(75) = {37, 44};
//+
Line(76) = {38, 19};
//+
Line(77) = {36, 43};
//+
Curve Loop(13) = {35, 28, -36, -44};
//+
Plane Surface(13) = {13};
//+
Curve Loop(14) = {36, 21, 29, -37};
//+
Plane Surface(14) = {14};
//+
Curve Loop(15) = {29, 38, -30, -22};
//+
Plane Surface(15) = {15};
//+
Curve Loop(16) = {30, 39, 31, -23};
//+
Plane Surface(16) = {16};
//+
Curve Loop(17) = {24, -32, -40, 31};
//+
Plane Surface(17) = {17};
//+
Curve Loop(18) = {32, 25, -33, -41};
//+
Plane Surface(18) = {18};
//+
Curve Loop(19) = {33, 26, -34, -42};
//+
Plane Surface(19) = {19};
//+
Curve Loop(20) = {43, 35, -27, -34};
//+
Plane Surface(20) = {20};
//+
Curve Loop(21) = {51, 54, -50, -37};
//+
Plane Surface(21) = {21};
//+
Curve Loop(22) = {50, 55, -49, -38};
//+
Plane Surface(22) = {22};
//+
Curve Loop(23) = {49, 56, -48, -39};
//+
Plane Surface(23) = {23};
//+
Curve Loop(24) = {40, 47, -57, -48};
//+
Plane Surface(24) = {24};
//+
Curve Loop(25) = {41, 46, -58, -47};
//+
Plane Surface(25) = {25};
//+
Line(78) = {24, 18};
//+
Curve Loop(26) = {78, -59, -46, 42};
//+
Plane Surface(26) = {26};
//+
Curve Loop(27) = {52, -45, -43, 78};
//+
Plane Surface(27) = {27};
//+
Curve Loop(28) = {53, -51, -44, 45};
//+
Plane Surface(28) = {28};
//+
Curve Loop(29) = {60, 61, -62, -53};
//+
Plane Surface(29) = {29};
//+
Curve Loop(30) = {63, 64, -54, 62};
//+
Plane Surface(30) = {30};
//+
Curve Loop(31) = {58, -67, 68, 66};
//+
Plane Surface(31) = {31};
//+
Curve Loop(32) = {57, -66, 69, 65};
//+
Plane Surface(32) = {32};
//+
Curve Loop(33) = {70, 71, -77, -64};
//+
Plane Surface(33) = {33};
//+
Curve Loop(34) = {75, 73, 74, 65};
//+
Plane Surface(34) = {34};
//+
Line(79) = {43, 19};
//+
Line(80) = {19, 44};
//+
Curve Loop(35) = {77, 79, -76, -55};
//+
Plane Surface(35) = {35};
//+
Curve Loop(36) = {76, 80, -75, -56};
//+
Plane Surface(36) = {36};
//+
Transfinite Curve {79, 80, 55, 56, 38, 39, 40, 41, 42, 43, 44, 37, 54, 53, 52, 59, 58, 57, 28, 27, 26, 25, 24, 23, 22, 21, 7, 6, 5, 12, 4, 1, 3, 2, 8, 9, 10, 11, 63, 61, 69, 68} = N_radial Using Progression 1;
//+
Transfinite Curve {74, 75, 76, 77, 70} = N_downstream_x Using Progression 1;
//+
Transfinite Curve {60, 62, 64, 71, 73, 65, 66, 67} = N_outer_band Using Progression 1;
//+
Transfinite Curve {-45, -51, -50, -49, -48, -47, -46, -78} = N_ring_outer Using Progression p_ring_outer;
//+
Transfinite Curve {35, 34, 33, 32, 31, -30, -29, 36} = N_ring_middle Using Progression p_ring_middle;
//+
Transfinite Curve {20, 16, 19, 13, 18, 14, 17, 15} = N_ring_inner Using Progression 1;
//+
Transfinite Surface {35} = {38, 19, 43, 36};
//+
Transfinite Surface {33} = {36, 43, 23, 40};
//+
Transfinite Surface {36} = {37, 44, 19, 38};
//+
Transfinite Surface {34} = {41, 22, 44, 37};
//+
Transfinite Surface {30} = {35, 36, 40, 39};
//+
Transfinite Surface {29} = {32, 35, 39, 20};
//+
Transfinite Surface {32} = {42, 41, 37, 34};
//+
Transfinite Surface {31} = {21, 42, 34, 33};
//+
Transfinite Surface {21} = {26, 28, 36, 35};
//+
Transfinite Surface {28} = {29, 26, 35, 32};
//+
Transfinite Surface {27} = {18, 24, 29, 32};
//+
Transfinite Surface {26} = {18, 33, 31, 24};
//+
Transfinite Surface {25} = {33, 34, 27, 31};
//+
Transfinite Surface {24} = {34, 37, 30, 27};
//+
Transfinite Surface {23} = {30, 37, 38, 25};
//+
Transfinite Surface {22} = {25, 38, 36, 28};
//+
Transfinite Surface {13} = {15, 12, 26, 29};
//+
Transfinite Surface {20} = {24, 11, 15, 29};
//+
Transfinite Surface {19} = {24, 31, 16, 11};
//+
Transfinite Surface {18} = {31, 27, 13, 16};
//+
Transfinite Surface {17} = {27, 30, 17, 13};
//+
Transfinite Surface {16} = {17, 30, 25, 10};
//+
Transfinite Surface {15} = {10, 25, 28, 14};
//+
Transfinite Surface {14} = {12, 14, 28, 26};
//+
Transfinite Surface {5} = {7, 8, 12, 15};
//+
Transfinite Surface {6} = {11, 2, 7, 15};
//+
Transfinite Surface {7} = {16, 6, 2, 11};
//+
Transfinite Surface {8} = {16, 13, 9, 6};
//+
Transfinite Surface {9} = {13, 17, 5, 9};
//+
Transfinite Surface {10} = {5, 17, 10, 3};
//+
Transfinite Surface {11} = {3, 10, 14, 4};
//+
Transfinite Surface {12} = {8, 4, 14, 12};
//+
Transfinite Surface {1} = {2, 1, 8, 7};
//+
Transfinite Surface {4} = {6, 9, 1, 2};
//+
Transfinite Surface {3} = {9, 5, 3, 1};
//+
Transfinite Surface {2} = {1, 3, 4, 8};
//+
Recombine Surface {27, 29, 28, 20, 13, 6, 5, 26, 19, 1, 7, 12, 4, 2, 30, 14, 21, 8, 3, 11, 9, 10, 18, 25, 15, 22, 31, 17, 16, 24, 23, 32, 33, 35, 36, 34};
//+
//+
Extrude {0, 0, -2} {
  Surface{5}; Surface{6}; Surface{7}; Surface{8}; Surface{9}; Surface{10}; Surface{11}; Surface{12}; Surface{2}; Surface{1}; Surface{4}; Surface{3}; Layers {N_injector_layers}; Recombine;
}
//+
Extrude {0, 0, 10} {
  Surface{27}; Surface{28}; Surface{29}; Surface{30}; Surface{33}; Surface{35}; Surface{36}; Surface{34}; Surface{32}; Surface{31}; Surface{26}; Surface{19}; Surface{20}; Surface{13}; Surface{14}; Surface{15}; Surface{21}; Surface{22}; Surface{16}; Surface{23}; Surface{24}; Surface{25}; Surface{18}; Surface{17}; Surface{6}; Surface{5}; Surface{12}; Surface{11}; Surface{10}; Surface{9}; Surface{8}; Surface{7}; Surface{4}; Surface{1}; Surface{2}; Surface{3}; Layers {N_domain_layers}; Recombine;
}
//+
Physical Volume("fluid", 249) = {22, 21, 20, 34, 33, 23, 35, 36, 32, 24, 19, 31, 43, 42, 44, 45, 41, 48, 46, 37, 47, 40, 38, 39, 25, 28, 13, 26, 27, 30, 18, 14, 29, 4, 5, 3, 11, 6, 12, 15, 10, 2, 9, 7, 16, 1, 8, 17};
//+
Physical Surface("inletWater") = {41, 45, 49, 53, 57, 61, 65, 68, 71, 73, 75, 76};
Physical Surface("inletAir") = {77, 86, 115, 118};
Physical Surface("outlet") = {95, 98, 102, 106};
Physical Surface("side1") = {87, 90, 94};
Physical Surface("side2") = {107, 112, 116};
Physical Surface("top") = {81, 85, 89, 93, 97, 101, 105, 109, 113, 117, 121, 125, 128, 131, 135, 139, 141, 143, 147, 149, 152, 154, 157, 159, 163, 166, 169, 172, 175, 178, 181, 183, 186, 188, 190, 191};
Physical Surface("bottomWall") = {13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36};
Physical Surface("injectorWalls") = {60, 46, 64, 42, 37, 66, 50, 54};
