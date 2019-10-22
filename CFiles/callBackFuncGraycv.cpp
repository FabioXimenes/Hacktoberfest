#include <iostream>

#include "opencv2\core\core.hpp"
#include "opencv2\highgui\highgui.hpp"
#include "opencv2\imgproc\imgproc.hpp"

#include "callBackFunc.h"

using namespace cv;
using namespace std;

void CallBackFuncGraycv(int event, int x, int y, int flags, void* userdata){

	if (event == EVENT_LBUTTONDOWN){
		cout << "Left button of the mouse is clicked - position (" << x << ", " << y << ")" << endl;
		Scalar intensity = img.at<uchar>(y, x);
		cout << "Pixel intensity values: " << intensity.val[0] << endl;
	}
	else if (event == EVENT_RBUTTONDOWN)
		cout << "Right button of the mouse is clicked - position (" << x << ", " << y << ")" << endl;

	else if (event == EVENT_MBUTTONDOWN)
		cout << "Middle button of the mouse is clicked - position (" << x << ", " << y << ")" << endl;

	else if (event == EVENT_MOUSEMOVE)
		cout << "Mouse move over the window - position (" << x << ", " << y << ")" << endl;
}
