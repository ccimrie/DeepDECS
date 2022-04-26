# DeepDECS: Capturing the uncertainity of Deep Neural Networks

This repo contains the code used for acquiring the results for [Discrete-Event Controller Synthesis for Autonomous Systems with Deep-Learning Perception Components](https://arxiv.org/abs/2202.03360).

There are two case studies explored:

- A robot mitigating collisions with a DNN to predict said collisions

- [Perceiving a human driver's state while in a self-driving car](https://www.york.ac.uk/assuring-autonomy/demonstrators/autonomous-driving/)

The **DNN** contains the DNN used for both setups. The specific models trained can be found in the respective directories. Please refer to the individual directories for more details on running the separate experiments.

### Prerequisites
#### DNN
- tensorflow>=2.2
- pandas
- sklearn
- netcal==1.1.3
- scriptify
- matplotlib
- statsmodels
- tensorflow-probability 

### Robot collision mitigation
- box2d
- PRISM
- python3
- numpy
- matplotlib

### SafeSCAD
- PRISM
- python3
- matplotlib
