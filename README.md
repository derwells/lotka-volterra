# Lotka-Volterra Root Finding Solution
Predator-prey dynamics of the Lotka-Volterra model are normally worked out by solving the differential equations numerically (Runge-Kutta). This alternative, however, applies Regula-Falsi root finding.

Made for the completion of CS 136 (Elementary Numerical Methods I).

## Documentation
Found [here](https://drive.google.com/file/d/1qumwxmLpMo7Z_LwizRqNo_AprVtUJzze/view?usp=sharing).

## Installation

Clone this git repo into desired folder then run commands below.

```bash
pip install numpy
pip install matplotlib
```

## Usage
Running command below will output plots into ``/plots``directory.
```python
py -3 main.py
```
Default initial values are ``x=50, y=40``.
