### Augment Tool for automating Stage 2 of DeepDECS (Model augmentation)

A python tool was developed to automate the model augmentation stage of DeepDECS. The tool takes as input a perfect-perception pDTMC model, which needs to follow the structure shown in **generic-pDTMC.pdf**, along with the confusion matrices to output a DNN-perception pDTMC model. The tool is executed as
```
python deepDECSAugment.py perfect-perception-model.pm confusion_matrices.txt DNN-perception-model.pm
```
where ```perfect-perception-model.pm``` and ```confusion_matrices.txt``` are files containing the perfect-perception pDTMC model and the confusion matrix elements $\mathcal{C}_v\[k,k'\]$, $v\in \mathbb{B}^n$, $k\in\[K\]$, $k'\in\[K\]$.

The ```DNN-perception-model.pm``` is the name of the file in which the DNN-perception pDTMC model will be generated. The format of ```confusion_matrices.txt``` must only be the elements of the confusion matrices, with the following format:

```
C_[00...000]
C_[00...001]
C_[00...010]
C_[00...011]
...
C_[11...111]
```

I.e. representing the verifcation methods satisfied as a binary string. For more details on DeepDECS please refer to the [paper](https://arxiv.org/abs/2202.03360). You can also contact Calum Imrie (calum.imrie@york.ac.uk). 
