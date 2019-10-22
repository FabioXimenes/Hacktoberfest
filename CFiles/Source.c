#include <iostream>

#include "opencv2\core\core.hpp"
#include "opencv2\highgui\highgui.hpp"
#include "opencv2\imgproc\imgproc.hpp"

#include "callBackFunc.h"

using namespace std;
using namespace cv;

Mat img;
int B, G, R;

int main(){

	img = imread("tucano.jpg", CV_LOAD_IMAGE_COLOR);
	//img = imread("tucano.jpg", CV_LOAD_IMAGE_GRAYSCALE); //Para imagem em tons de cinza.
	int tipo = img.type();
	if (img.empty())
		cout << "Error loading the image" << endl;
	else cout << "Image OK." << endl;
	
	namedWindow("Janela", CV_WINDOW_AUTOSIZE);
	
	if (img.type() == 0)
		//set the callback function for any mouse event
		setMouseCallback("Janela", CallBackFuncGraycv, NULL);
	else 
		setMouseCallback("Janela", CallBackFunc, NULL);
	
	imshow("Janela", img);
	cvWaitKey(0);

	system("pause");
	return EXIT_SUCCESS;
}
