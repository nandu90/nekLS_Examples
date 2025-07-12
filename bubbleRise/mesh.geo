// Gmsh project created on Sat May 17 19:46:23 2025
//+
Point(1) = {-2.0, 2.0, 8, 1.0};
//+
Point(2) = {-2.0, 0, 8, 1.0};
//+
//+
Point(3) = {-2.0, -2.0, 8, 1.0};
//+
Point(4) = {0, -2.0, 8, 1.0};
//+
Point(5) = {0, 0, 8, 1.0};
//+
Point(6) = {0, 2.0, 8, 1.0};
//+
Point(7) = {2.0, 2.0, 8, 1.0};
//+
Point(8) = {2.0, 0, 8, 1.0};
//+
Point(9) = {2.0, -2.0, 8, 1.0};
//+
Line(1) = {6, 7};
//+
Line(2) = {7, 8};
//+
Line(3) = {8, 9};
//+
Line(4) = {9, 4};
//+
Line(5) = {4, 3};
//+
Line(6) = {3, 2};
//+
Line(7) = {2, 1};
//+
Line(8) = {1, 6};
//+
Line(9) = {6, 5};
//+
Line(10) = {5, 4};
//+
Line(11) = {2, 5};
//+
Line(12) = {5, 8};
//+
Curve Loop(1) = {5, 6, 11, 10};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {10, -4, -3, -12};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {9, 12, -2, -1};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {11, -9, -8, -7};
//+
Plane Surface(4) = {4};
//+
//+
Point(10) = {-10, 0, 8, 1.0};
//+
Point(11) = {-10, 10, 8, 1.0};
//+
Point(12) = {-10, -10, 8, 1.0};
//+
Point(13) = {0, -10, 8, 1.0};
//+
Point(14) = {0, 10, 8, 1.0};
//+
Point(15) = {10, 10, 8, 1.0};
//+
Point(16) = {10, 0, 8, 1.0};
//+
Point(17) = {10, -10, 8, 1.0};
//+
Line(13) = {1, 11};
//+
Line(14) = {7, 15};
//+
Line(15) = {9, 17};
//+
Line(16) = {3, 12};
//+
Line(17) = {12, 10};
//+
Line(18) = {10, 11};
//+
Line(19) = {11, 14};
//+
Line(20) = {14, 15};
//+
Line(21) = {15, 16};
//+
Line(22) = {16, 17};
//+
Line(23) = {17, 13};
//+
Line(24) = {13, 12};
//+
Line(25) = {13, 4};
//+
Line(26) = {16, 8};
//+
Line(27) = {6, 14};
//+
Line(28) = {2, 10};
//+
Curve Loop(5) = {13, -18, -28, 7};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {17, -28, -6, 16};
//+
Plane Surface(6) = {6};
//+
Curve Loop(7) = {16, -24, 25, 5};
//+
Plane Surface(7) = {7};
//+
Curve Loop(8) = {25, -4, 15, 23};
//+
Plane Surface(8) = {8};
//+
Curve Loop(9) = {15, -22, 26, 3};
//+
Plane Surface(9) = {9};
//+
Curve Loop(10) = {2, -26, -21, -14};
//+
Plane Surface(10) = {10};
//+
Curve Loop(11) = {14, -20, -27, 1};
//+
Plane Surface(11) = {11};
//+
Curve Loop(12) = {8, 27, -19, -13};
//+
Plane Surface(12) = {12};
//+
Transfinite Curve {5, 4, 3, 2, 1, 8, 7, 6, 9, 11, 10, 12} = 40 Using Progression 1;
//+
Transfinite Curve {18, 17, 24, 23, 22, 21, 20, 19} = 40 Using Progression 1;
//+
Transfinite Curve {-13, -28, -16, 25, -15, 26, -14, -27} = 10 Using Progression 0.8;
//+
Transfinite Surface {7} = {12, 13, 4, 3};
//+
Transfinite Surface {8} = {13, 17, 9, 4};
//+
Transfinite Surface {9} = {17, 16, 8, 9};
//+
Transfinite Surface {10} = {8, 16, 15, 7};
//+
Transfinite Surface {11} = {7, 15, 14, 6};
//+
Transfinite Surface {12} = {1, 6, 14, 11};
//+
Transfinite Surface {5} = {11, 10, 2, 1};
//+
Transfinite Surface {6} = {10, 12, 3, 2};
//+
Transfinite Surface {1} = {3, 4, 5, 2};
//+
Transfinite Surface {2} = {4, 9, 8, 5};
//+
Transfinite Surface {3} = {5, 8, 7, 6};
//+
Transfinite Surface {4} = {2, 5, 6, 1};
//+
Recombine Surface {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
//+
//+
Extrude {0, 0, 6} {
  Point{17}; Point{13}; Point{12}; Point{9}; Point{4}; Point{3}; Point{16}; Point{8}; Point{5}; Point{2}; Point{10}; Point{7}; Point{6}; Point{1}; Point{15}; Point{14}; Point{11}; Curve{23}; Curve{24}; Curve{15}; Curve{4}; Curve{25}; Curve{16}; Curve{5}; Curve{22}; Curve{26}; Curve{3}; Curve{12}; Curve{10}; Curve{11}; Curve{6}; Curve{28}; Curve{17}; Curve{2}; Curve{9}; Curve{1}; Curve{7}; Curve{8}; Curve{21}; Curve{14}; Curve{27}; Curve{20}; Curve{19}; Curve{18}; Curve{13}; Surface{8}; Surface{7}; Surface{9}; Surface{2}; Surface{1}; Surface{6}; Surface{3}; Surface{4}; Surface{10}; Surface{5}; Surface{11}; Surface{12}; Layers {120}; Recombine;
}

Extrude {0, 0, -1} {
  Point{17}; Point{13}; Point{12}; Point{9}; Point{4}; Point{3}; Point{16}; Point{8}; Point{5}; Point{2}; Point{10}; Point{7}; Point{6}; Point{1}; Point{15}; Point{14}; Point{11}; Curve{23}; Curve{24}; Curve{15}; Curve{4}; Curve{25}; Curve{16}; Curve{5}; Curve{22}; Curve{26}; Curve{3}; Curve{12}; Curve{10}; Curve{11}; Curve{6}; Curve{28}; Curve{17}; Curve{2}; Curve{9}; Curve{1}; Curve{7}; Curve{8}; Curve{21}; Curve{14}; Curve{27}; Curve{20}; Curve{19}; Curve{18}; Curve{13}; Surface{8}; Surface{7}; Surface{9}; Surface{2}; Surface{1}; Surface{6}; Surface{3}; Surface{4}; Surface{10}; Surface{5}; Surface{11}; Surface{12}; Layers {20}; Recombine;
}
//+
Extrude {0, 0, 6} {
  Surface{377}; Surface{421}; Surface{399}; Surface{355}; Surface{223}; Surface{333}; Surface{311}; Surface{289}; Surface{267}; Surface{245}; Surface{201}; Surface{179}; Layers{10}; Recombine;
}
//+
Extrude {0, 0, -7} {
  Surface{814}; Surface{792}; Surface{748}; Surface{616}; Surface{770}; Surface{682}; Surface{594}; Surface{572}; Surface{660}; Surface{726}; Surface{704}; Surface{638}; Layers{15}; Recombine;
}
//+
Physical Volume("fluid", 1343) = {32, 36, 29, 34, 35, 28, 33, 1, 3, 31, 27, 30, 4, 2, 9, 5, 25, 26, 7, 6, 13, 15, 11, 8, 16, 44, 40, 14, 10, 12, 21, 17, 19, 18, 48, 23, 43, 20, 39, 45, 47, 42, 38, 22, 24, 46, 41, 37};
//+
//+
Physical Surface("outlet") = {858, 880, 902, 836, 990, 924, 1078, 968, 1034, 946, 1012, 1056};
//+
Physical Surface("wall") = {1100, 1122, 1144, 1166, 1188, 1210, 1232, 1254, 1320, 1342, 1298, 1276};
//+
Physical Surface("sym") = {1179, 546, 153, 827, 1197, 502, 109, 977, 145, 1113, 538, 871, 1095, 542, 149, 853, 1157, 1139, 470, 77, 915, 897, 133, 526, 1047, 53, 446, 1223, 1253, 1077, 49, 442};
