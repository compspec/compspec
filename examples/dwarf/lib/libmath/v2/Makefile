all:
	g++ -g -Wall -fPIC -shared -o libmath.v2.so MathLibrary.cpp
	g++ -g -Wall -o math-client MathClient.cpp -I . -L. libmath.v2.so
