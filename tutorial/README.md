### DeepDECS tutorial

This tutorial on how to employ the DeepDECS process uses a car driving on a potentially icy road, where the iceness of the road is predicted by a DNN (**DeepDECS_tutorial.pdf**). From this a controller is to be synthesised that will trade off between speed and risk. To complete the tutorial you will be using the following files:

- **car.pm**: A file containing the DTMC model used for probabilistic model checking (the software [Prism](https://www.prismmodelchecker.org/) is used). The model is of a car that can perfectly predict if the road is icy or not. This will be used for Stage 2 of DeepDEDCS.
- **car.pctl**: The requirement properties of the system. This will be used for synthesising the controller in Stage 3 of DeepDECS.
- **conf_mat.txt**: The confusion matrix of the DNN that is assumed to be have been used in system. This file is formatted to be used by the automated [augment tool](https://github.com/ccimrie/DeepDECS/tree/master/augment_tool) for Stage 2 of DeepDECS.

If you have successfully followed the tutorial for Stage 2 (Model augmentation) you should have as an output an augmented model which you can use for producing pareto optimal controllers in Stage 3 of DeepDECS (Sec. 4 of the tutorial). This should look similar to the augmented file **car-DNN-mat.pm**.