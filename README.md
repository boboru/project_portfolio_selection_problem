# Project Portfolio Selection Problem (PPSP)
 Efficient formulations for PPSP problem considering cardinality and interdependency

## Introduction
In the project portfolio selection problem (PPSP), a decision maker must select a set of projects to launch and try to maximize the profit. Meanwhile, there are some factors considered by a DM. In this study, we consider (1.) project interdependency and (2.) cardinality constraint only.

1. Project Interdependency: PPSP may be affected by synergy effect from the various combinations of different projects. For instance, if we launch 2 projects simultaneously, then it may earn you additional benefits a.k.a. synergestic benefit. Moreover, resource interdependency occurs when common resources are shared by various projects. Thus, to find a novel combinations of projects may increase the potential benefit.
2. Cardinality Constraint: Cardinality is the number of projects selected in the portfolio. Thus, this number is restricted below a given numbr in this constraint.

In the rest of this tutorial, there are model formulation, Python + Gurobi implementation, an example and advanced topics.

## Model Formulaton
In the original paper, both equality and inequality cardinality constraint cases are considered, but I will demostrate the equality constraint cases only in this tutorial. You can find inequality constraint cases referred to the paper [[2]](#2).

We first introduce some notations.

![Notations](./image/notations.png)

For instance,
if project <!-- $i, j$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?i%2C%20j"> and <!-- $k$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?k"> are selected, which means <!-- $x_i=x_j=x_k=1$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x_i%3Dx_j%3Dx_k%3D1">. Then, the total benefit will be <!-- $(r_i+r_j+r_k)+(r_{i,j}+r_{i,k}+r_{j,k})+(r_{i,j,k})$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?(r_i%2Br_j%2Br_k)%2B(r_%7Bi%2Cj%7D%2Br_%7Bi%2Ck%7D%2Br_%7Bj%2Ck%7D)%2B(r_%7Bi%2Cj%2Ck%7D)">, and this combination will consume <!-- $(d_i+d_j+d_k)-(d_{i,j}+d_{i,k}+d_{j,k})+(d_{i,j,k})$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?(d_i%2Bd_j%2Bd_k)-(d_%7Bi%2Cj%7D%2Bd_%7Bi%2Ck%7D%2Bd_%7Bj%2Ck%7D)%2B(d_%7Bi%2Cj%2Ck%7D)"> resoure in the mean time. One can notice that there is a minus sign in the equation about resource, since shared-used concept is considered here. This concept follows standard Venn diagram (文氏圖).

### Nonlinear Model

Nonlinear model is quite simple in this problem. Our objective is to maximize the total benefit subject to cardinality and resource constraints.

<!-- $
\begin{aligned}
Max ~ & \underbrace{\sum\limits_{i = 1}^N r_i x_i + 
\sum\limits_{i = 1}^{N-1} \sum\limits_{j = 1+1}^N  r_{i,j}x_i x_j + 
\sum\limits_{i = 1}^{N-2} \sum\limits_{j = i+1}^{N-1} \sum\limits_{k = j+1}^N r_{i,j,k} x_i x_j x_k}_{\text{total benefit}} 
\\
s.t. ~ & \underbrace{\sum\limits_{i = 1}^N x_i = m}_{\text{cardinality constraint}} \\
        & \underbrace{\sum\limits_{i = 1}^N d_i x_i -
\sum\limits_{i = 1}^{N-1} \sum\limits_{j = 1+1}^N  d_{i,j}x_i x_j + 
\sum\limits_{i = 1}^{N-2} \sum\limits_{j = i+1}^{N-1} \sum\limits_{k = j+1}^N d_{i,j,k} x_i x_j x_k \leq b}_{\text{resource constraint}} \\
& x_i \in \{0, 1\},\; i = 1, \ldots ,N 
\end{aligned}
$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Cbegin%7Baligned%7D%0AMax%20~%20%26%20%5Cunderbrace%7B%5Csum%5Climits_%7Bi%20%3D%201%7D%5EN%20r_i%20x_i%20%2B%20%0A%5Csum%5Climits_%7Bi%20%3D%201%7D%5E%7BN-1%7D%20%5Csum%5Climits_%7Bj%20%3D%201%2B1%7D%5EN%20%20r_%7Bi%2Cj%7Dx_i%20x_j%20%2B%20%0A%5Csum%5Climits_%7Bi%20%3D%201%7D%5E%7BN-2%7D%20%5Csum%5Climits_%7Bj%20%3D%20i%2B1%7D%5E%7BN-1%7D%20%5Csum%5Climits_%7Bk%20%3D%20j%2B1%7D%5EN%20r_%7Bi%2Cj%2Ck%7D%20x_i%20x_j%20x_k%7D_%7B%5Ctext%7Btotal%20benefit%7D%7D%20%0A%5C%5C%0As.t.%20~%20%26%20%5Cunderbrace%7B%5Csum%5Climits_%7Bi%20%3D%201%7D%5EN%20x_i%20%3D%20m%7D_%7B%5Ctext%7Bcardinality%20constraint%7D%7D%20%5C%5C%0A%20%20%20%20%20%20%20%20%26%20%5Cunderbrace%7B%5Csum%5Climits_%7Bi%20%3D%201%7D%5EN%20d_i%20x_i%20-%0A%5Csum%5Climits_%7Bi%20%3D%201%7D%5E%7BN-1%7D%20%5Csum%5Climits_%7Bj%20%3D%201%2B1%7D%5EN%20%20d_%7Bi%2Cj%7Dx_i%20x_j%20%2B%20%0A%5Csum%5Climits_%7Bi%20%3D%201%7D%5E%7BN-2%7D%20%5Csum%5Climits_%7Bj%20%3D%20i%2B1%7D%5E%7BN-1%7D%20%5Csum%5Climits_%7Bk%20%3D%20j%2B1%7D%5EN%20d_%7Bi%2Cj%2Ck%7D%20x_i%20x_j%20x_k%20%5Cleq%20b%7D_%7B%5Ctext%7Bresource%20constraint%7D%7D%20%5C%5C%0A%26%20x_i%20%5Cin%20%5C%7B0%2C%201%5C%7D%2C%5C%3B%20i%20%3D%201%2C%20%5Cldots%20%2CN%20%0A%5Cend%7Baligned%7D">

Although this model is quite simple to understand, it's inefficient due to the polynomial integer programming property. Thus, its implementaion is omitted. 

### Conventional Model (Equality Cardinality Constraint)
In thish model, we introduce 2 set of decicsion variables <!-- $\mathbf{y} = (y_{1,2}, \ldots, y_{1,N}, y_{2,3}, \ldots, y_{N-1, N}) \in \mathbb{R}^{\frac{N(N-1)}{2} = {N \choose 2}}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Cmathbf%7By%7D%20%3D%20(y_%7B1%2C2%7D%2C%20%5Cldots%2C%20y_%7B1%2CN%7D%2C%20y_%7B2%2C3%7D%2C%20%5Cldots%2C%20y_%7BN-1%2C%20N%7D)%20%5Cin%20%5Cmathbb%7BR%7D%5E%7B%5Cfrac%7BN(N-1)%7D%7B2%7D%20%3D%20%7BN%20%5Cchoose%202%7D%7D"> and <!-- $\mathbf{z} = (z_{1,2,3}, \ldots, z_{1,N-1,N}, z_{2,3,4}, \ldots, z_{N-2,N-1,N}) \in \mathbb{R}^{\frac{N(N-1)(N-2)}{6}= {N \choose 3}}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Cmathbf%7Bz%7D%20%3D%20(z_%7B1%2C2%2C3%7D%2C%20%5Cldots%2C%20z_%7B1%2CN-1%2CN%7D%2C%20z_%7B2%2C3%2C4%7D%2C%20%5Cldots%2C%20z_%7BN-2%2CN-1%2CN%7D)%20%5Cin%20%5Cmathbb%7BR%7D%5E%7B%5Cfrac%7BN(N-1)(N-2)%7D%7B6%7D%3D%20%7BN%20%5Cchoose%203%7D%7D">. One can notice that the subscripts of each decision variables are in an ascending order s.t. every combination will have an unique representation. 

<!-- $
\begin{aligned}
Max ~ & \sum\limits_{i = 1}^N r_i x_i + 
\sum\limits_{i = 1}^{N} \sum\limits_{j > i}^N  r_{i,j}y_{i,j} + 
\sum\limits_{i = 1}^{N} \sum\limits_{j > i}^{N} \sum\limits_{k > j}^N r_{i,j,k} z_{i,j,k} \\
\\
s.t. ~ & \sum\limits_{i = 1}^N x_i = m \\
       & \sum\limits_{i = 1}^N d_i x_i - \sum\limits_{i = 1}^{N} \sum\limits_{j > i}^N  d_{i,j}y_{i,j} + \sum\limits_{i = 1}^{N} \sum\limits_{j > i}^{N} \sum\limits_{k > j}^N d_{i,j,k} z_{i,j,k} \leq b \\
       & \underbrace{\sum\limits_{j>i}^N y_{i,j} + \sum\limits_{j<i}^N y_{j,i} + \sum\limits_{j>i}^N \sum\limits_{k>j}^N z_{i,j,k} + \sum\limits_{i>j}^N \sum\limits_{k>i}^N z_{j,i,k} +\sum\limits_{k>j}^N \sum\limits_{i>k}^N z_{j,k,i} = \frac{m(m-1)}{2} x_i,\; \text{for } i = 1,\ldots ,N}_{\textstyle \begin{array}{c} \Leftrightarrow x_ix_j = y_{i,j} \text{ and } x_i x_j x_k = z_{i,j,k} \end{array}} \\
       & x_i \in \{0, 1\} \text{ and } 0 \leq y_{i,j}, z_{i,j,k} \leq 1, \; \text{for } i,j,k = 1, \ldots ,N, \text{ and } i<j<k
\end{aligned}
$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Cbegin%7Baligned%7D%0AMax%20~%20%26%20%5Csum%5Climits_%7Bi%20%3D%201%7D%5EN%20r_i%20x_i%20%2B%20%0A%5Csum%5Climits_%7Bi%20%3D%201%7D%5E%7BN%7D%20%5Csum%5Climits_%7Bj%20%3E%20i%7D%5EN%20%20r_%7Bi%2Cj%7Dy_%7Bi%2Cj%7D%20%2B%20%0A%5Csum%5Climits_%7Bi%20%3D%201%7D%5E%7BN%7D%20%5Csum%5Climits_%7Bj%20%3E%20i%7D%5E%7BN%7D%20%5Csum%5Climits_%7Bk%20%3E%20j%7D%5EN%20r_%7Bi%2Cj%2Ck%7D%20z_%7Bi%2Cj%2Ck%7D%20%5C%5C%0A%5C%5C%0As.t.%20~%20%26%20%5Csum%5Climits_%7Bi%20%3D%201%7D%5EN%20x_i%20%3D%20m%20%5C%5C%0A%20%20%20%20%20%20%20%26%20%5Csum%5Climits_%7Bi%20%3D%201%7D%5EN%20d_i%20x_i%20-%20%5Csum%5Climits_%7Bi%20%3D%201%7D%5E%7BN%7D%20%5Csum%5Climits_%7Bj%20%3E%20i%7D%5EN%20%20d_%7Bi%2Cj%7Dy_%7Bi%2Cj%7D%20%2B%20%5Csum%5Climits_%7Bi%20%3D%201%7D%5E%7BN%7D%20%5Csum%5Climits_%7Bj%20%3E%20i%7D%5E%7BN%7D%20%5Csum%5Climits_%7Bk%20%3E%20j%7D%5EN%20d_%7Bi%2Cj%2Ck%7D%20z_%7Bi%2Cj%2Ck%7D%20%5Cleq%20b%20%5C%5C%0A%20%20%20%20%20%20%20%26%20%5Cunderbrace%7B%5Csum%5Climits_%7Bj%3Ei%7D%5EN%20y_%7Bi%2Cj%7D%20%2B%20%5Csum%5Climits_%7Bj%3Ci%7D%5EN%20y_%7Bj%2Ci%7D%20%2B%20%5Csum%5Climits_%7Bj%3Ei%7D%5EN%20%5Csum%5Climits_%7Bk%3Ej%7D%5EN%20z_%7Bi%2Cj%2Ck%7D%20%2B%20%5Csum%5Climits_%7Bi%3Ej%7D%5EN%20%5Csum%5Climits_%7Bk%3Ei%7D%5EN%20z_%7Bj%2Ci%2Ck%7D%20%2B%5Csum%5Climits_%7Bk%3Ej%7D%5EN%20%5Csum%5Climits_%7Bi%3Ek%7D%5EN%20z_%7Bj%2Ck%2Ci%7D%20%3D%20%5Cfrac%7Bm(m-1)%7D%7B2%7D%20x_i%2C%5C%3B%20%5Ctext%7Bfor%20%7D%20i%20%3D%201%2C%5Cldots%20%2CN%7D_%7B%5Ctextstyle%20%5Cbegin%7Barray%7D%7Bc%7D%20%5CLeftrightarrow%20x_ix_j%20%3D%20y_%7Bi%2Cj%7D%20%5Ctext%7B%20and%20%7D%20x_i%20x_j%20x_k%20%3D%20z_%7Bi%2Cj%2Ck%7D%20%5Cend%7Barray%7D%7D%20%5C%5C%0A%20%20%20%20%20%20%20%26%20x_i%20%5Cin%20%5C%7B0%2C%201%5C%7D%20%5Ctext%7B%20and%20%7D%200%20%5Cleq%20y_%7Bi%2Cj%7D%2C%20z_%7Bi%2Cj%2Ck%7D%20%5Cleq%201%2C%20%5C%3B%20%5Ctext%7Bfor%20%7D%20i%2Cj%2Ck%20%3D%201%2C%20%5Cldots%20%2CN%2C%20%5Ctext%7B%20and%20%7D%20i%3Cj%3Ck%0A%5Cend%7Baligned%7D">


### Proposed Model (Equality Cardinality Constraint)

In this model, <!-- $\mathbf{y}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Cmathbf%7By%7D"> decision variables are replaced with <!-- $\mathbf{z}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Cmathbf%7Bz%7D"> via some equations. Related proofs can be found in [[2]](#2).

<!-- $
\begin{aligned} 
Max ~ & \sum\limits_{i = 1}^N r_i x_i + 
\underbrace{\frac{1}{m-2}\sum\limits_{i = 1}^{N} \sum\limits_{j > i}^N \sum\limits_{k > j}^N (r_{i,j} + r_{i,k} + r_{j,k})z_{i,j,k}}_{\textstyle \begin{array}{c} =\sum\limits_{i = 1}^{N} \sum\limits_{j > i}^N  r_{i,j}y_{i,j} \end{array}} + 
\sum\limits_{i = 1}^{N} \sum\limits_{j > i}^{N} \sum\limits_{k > j}^N r_{i,j,k} z_{i,j,k}
\end{aligned} 
$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Cbegin%7Baligned%7D%20%0AMax%20~%20%26%20%5Csum%5Climits_%7Bi%20%3D%201%7D%5EN%20r_i%20x_i%20%2B%20%0A%5Cunderbrace%7B%5Cfrac%7B1%7D%7Bm-2%7D%5Csum%5Climits_%7Bi%20%3D%201%7D%5E%7BN%7D%20%5Csum%5Climits_%7Bj%20%3E%20i%7D%5EN%20%5Csum%5Climits_%7Bk%20%3E%20j%7D%5EN%20(r_%7Bi%2Cj%7D%20%2B%20r_%7Bi%2Ck%7D%20%2B%20r_%7Bj%2Ck%7D)z_%7Bi%2Cj%2Ck%7D%7D_%7B%5Ctextstyle%20%5Cbegin%7Barray%7D%7Bc%7D%20%3D%5Csum%5Climits_%7Bi%20%3D%201%7D%5E%7BN%7D%20%5Csum%5Climits_%7Bj%20%3E%20i%7D%5EN%20%20r_%7Bi%2Cj%7Dy_%7Bi%2Cj%7D%20%5Cend%7Barray%7D%7D%20%2B%20%0A%5Csum%5Climits_%7Bi%20%3D%201%7D%5E%7BN%7D%20%5Csum%5Climits_%7Bj%20%3E%20i%7D%5E%7BN%7D%20%5Csum%5Climits_%7Bk%20%3E%20j%7D%5EN%20r_%7Bi%2Cj%2Ck%7D%20z_%7Bi%2Cj%2Ck%7D%0A%5Cend%7Baligned%7D">

<!-- $
\begin{aligned} 
s.t. ~ & \sum\limits_{i = 1}^N x_i = m \\
       & \sum\limits_{i = 1}^N d_i x_i - \underbrace{\frac{1}{m-2} \sum\limits_{i = 1}^{N} \sum\limits_{j > i}^N \sum\limits_{k > j}^N (d_{i,j} + d_{i,k} + d_{j,k}) z_{i,j,k}}_{\textstyle \begin{array}{c} =\sum\limits_{i = 1}^{N} \sum\limits_{j > i}^N  d_{i,j}y_{i,j} \end{array}} + \sum\limits_{i = 1}^{N} \sum\limits_{j > i}^{N} \sum\limits_{k > j}^N d_{i,j,k} z_{i,j,k} \leq b \\
       & \underbrace{\sum\limits_{j>i}^N \sum\limits_{k>j}^N z_{i,j,k} + \sum\limits_{i>j}^N \sum\limits_{k>i}^N z_{j,i,k} +\sum\limits_{k>j}^N \sum\limits_{i>k}^N z_{j,k,i} = \frac{(m-1)(m-2)}{2} x_i, \; \text{for } i = 1,\ldots ,N}_{\textstyle \begin{array}{c} \Leftrightarrow  x_i x_j x_k = z_{i,j,k} \end{array}}\\
       & x_i \in \{0, 1\} \text{ and } 0 \leq z_{i,j,k} \leq 1, \; \text{for } i,j,k = 1, \ldots ,N, \text{ and } i<j<k
\end{aligned}
$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Cbegin%7Baligned%7D%20%0As.t.%20~%20%26%20%5Csum%5Climits_%7Bi%20%3D%201%7D%5EN%20x_i%20%3D%20m%20%5C%5C%0A%20%20%20%20%20%20%20%26%20%5Csum%5Climits_%7Bi%20%3D%201%7D%5EN%20d_i%20x_i%20-%20%5Cunderbrace%7B%5Cfrac%7B1%7D%7Bm-2%7D%20%5Csum%5Climits_%7Bi%20%3D%201%7D%5E%7BN%7D%20%5Csum%5Climits_%7Bj%20%3E%20i%7D%5EN%20%5Csum%5Climits_%7Bk%20%3E%20j%7D%5EN%20(d_%7Bi%2Cj%7D%20%2B%20d_%7Bi%2Ck%7D%20%2B%20d_%7Bj%2Ck%7D)%20z_%7Bi%2Cj%2Ck%7D%7D_%7B%5Ctextstyle%20%5Cbegin%7Barray%7D%7Bc%7D%20%3D%5Csum%5Climits_%7Bi%20%3D%201%7D%5E%7BN%7D%20%5Csum%5Climits_%7Bj%20%3E%20i%7D%5EN%20%20d_%7Bi%2Cj%7Dy_%7Bi%2Cj%7D%20%5Cend%7Barray%7D%7D%20%2B%20%5Csum%5Climits_%7Bi%20%3D%201%7D%5E%7BN%7D%20%5Csum%5Climits_%7Bj%20%3E%20i%7D%5E%7BN%7D%20%5Csum%5Climits_%7Bk%20%3E%20j%7D%5EN%20d_%7Bi%2Cj%2Ck%7D%20z_%7Bi%2Cj%2Ck%7D%20%5Cleq%20b%20%5C%5C%0A%20%20%20%20%20%20%20%26%20%5Cunderbrace%7B%5Csum%5Climits_%7Bj%3Ei%7D%5EN%20%5Csum%5Climits_%7Bk%3Ej%7D%5EN%20z_%7Bi%2Cj%2Ck%7D%20%2B%20%5Csum%5Climits_%7Bi%3Ej%7D%5EN%20%5Csum%5Climits_%7Bk%3Ei%7D%5EN%20z_%7Bj%2Ci%2Ck%7D%20%2B%5Csum%5Climits_%7Bk%3Ej%7D%5EN%20%5Csum%5Climits_%7Bi%3Ek%7D%5EN%20z_%7Bj%2Ck%2Ci%7D%20%3D%20%5Cfrac%7B(m-1)(m-2)%7D%7B2%7D%20x_i%2C%20%5C%3B%20%5Ctext%7Bfor%20%7D%20i%20%3D%201%2C%5Cldots%20%2CN%7D_%7B%5Ctextstyle%20%5Cbegin%7Barray%7D%7Bc%7D%20%5CLeftrightarrow%20%20x_i%20x_j%20x_k%20%3D%20z_%7Bi%2Cj%2Ck%7D%20%5Cend%7Barray%7D%7D%5C%5C%0A%20%20%20%20%20%20%20%26%20x_i%20%5Cin%20%5C%7B0%2C%201%5C%7D%20%5Ctext%7B%20and%20%7D%200%20%5Cleq%20z_%7Bi%2Cj%2Ck%7D%20%5Cleq%201%2C%20%5C%3B%20%5Ctext%7Bfor%20%7D%20i%2Cj%2Ck%20%3D%201%2C%20%5Cldots%20%2CN%2C%20%5Ctext%7B%20and%20%7D%20i%3Cj%3Ck%0A%5Cend%7Baligned%7D">

### Conventional and Proposed Model (Inequality Cardinality Constraint)

The basic idea is to introduce a set of binary variables in order to represent the cardinality, which is less than or equal to <!-- $m$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?m">.

The details of the formulation can be also found in the original paper [[2]](#2).

## Python + Gurobi Implementation

First, make sure you have installed the following packages and have Gurobi license:
```
numpy
gurobipy
```
I implemented four kinds of models including conventional model and proposed model with equality/ inequality cardinality constraint.

### Problem Solver
```
def PPSP_solver(N, m, r_i, r_ij, r_ijk, d_i, d_ij, d_ijk, b, mode, equality=True)
```

* Parameters
  - `N`: *int*
  - `m`: *int*
  - `r_i`: *dict of 1-D index*, e.g., `r_i[1]` means the benefit from implementing project 1.
  - `r_ij`: *dict of 2-D index*, e.g., `r_ij[1, 2]` means the benefit from implementing project 1 and 2.
  - `r_ijk`: *dict of 3-D index*, e.g.,  `r_ijk[1, 2, 3]` means the benefit from implementing project 1, 2 and 3.
  - `d_i`: *dict of 1-D index*, e.g., `d_i[1]` means the resource required from implementing project 1.
  - `d_ij`: *dict of 2-D index*, e.g., `d_ij[1, 2]` means the resource required from implementing project 1 and 2.
  - `d_ijk`: *dict of 3-D index*, e.g., `d_ijk[1, 2, 3]` means the resource required from implementing project 1, 2 and 3.
  - `b`: *float*
  - `mode`: *{'conventional', 'proposed'}, default='proposed'*
  - `equality`: *bool, default='True'*
  - `time_limit`: *int, default=3600*, the time limit to optimize the model
  - `is_quiet`: *bool, default=True*, enables or disables solver output

* Returns
  - *gurobipy.Model*

The parameter `mode` can be either 'conventional' or 'proposed' with `equality` being 'True' or 'False'. So, there are 4 kinds of model. The output of this function is an optimized Gurobi model. You can access it directly.

### Instance Generator
Additionally, you can automatically generate the instances by given N and m.

The parameters are basically uniformly distributed, which follows [[1]](#1):

- Resource
  + <!-- $d_{i} \sim \text{Uniform}(1,10)$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?d_%7Bi%7D%20%5Csim%20%5Ctext%7BUniform%7D(1%2C10)">
  + <!-- $d_{i,j} \sim \text{Uniform}(5,20)$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?d_%7Bi%2Cj%7D%20%5Csim%20%5Ctext%7BUniform%7D(5%2C20)">
  + <!-- $d_{i,j,k} \sim \text{Uniform}(10,50)$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?d_%7Bi%2Cj%2Ck%7D%20%5Csim%20%5Ctext%7BUniform%7D(10%2C50)">
  + <!-- $b \sim \text{Uniform}(0.05G, 0.1G),\, G = \sum_{i}d_i - \sum_{i}\sum_{i<j}d_{i,j}+\sum_{i}\sum_{i<j}\sum_{j<k}d_{i,j,k}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?b%20%5Csim%20%5Ctext%7BUniform%7D(0.05G%2C%200.1G)%2C%5C%2C%20G%20%3D%20%5Csum_%7Bi%7Dd_i%20-%20%5Csum_%7Bi%7D%5Csum_%7Bi%3Cj%7Dd_%7Bi%2Cj%7D%2B%5Csum_%7Bi%7D%5Csum_%7Bi%3Cj%7D%5Csum_%7Bj%3Ck%7Dd_%7Bi%2Cj%2Ck%7D">
- Benefit
  + <!-- $r_{i} \sim \text{Uniform}(10,100)$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?r_%7Bi%7D%20%5Csim%20%5Ctext%7BUniform%7D(10%2C100)">
  + <!-- $r_{i,j} \sim \text{Uniform}(50,200)$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?r_%7Bi%2Cj%7D%20%5Csim%20%5Ctext%7BUniform%7D(50%2C200)">
  + <!-- $r_{i,j,k} \sim \text{Uniform}(100,500)$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?r_%7Bi%2Cj%2Ck%7D%20%5Csim%20%5Ctext%7BUniform%7D(100%2C500)">

```
def instance_generator(N, m)
```
* Parameters
  - `N`: *int*
  - `m`: *int*
* Returns
  - *dict*

## Example
Please access 'example.ipynb' to run the code.

```
import numpy as np
import gurobipy as gp
from gurobipy import GRB

from model import PPSP_solver, instance_generator

# generate a problem instance with N = 16 and m = 3
instance = instance_generator(16, 3)

# solve the instance with four kinds of models and print the result with running time
for is_equal in [True, False]:
    if is_equal:
        print('-----------  Equality Cardinality Constraint  -----------')
    else:
        print('-----------  InEquality Cardinality Constraint  -----------')
        
    for mode_ in ['conventional', 'proposed']:
        model = PPSP_solver(**instance, mode=mode_, equality=is_equal)
        
        if  model.status == GRB.OPTIMAL:
            portfolio = []
            for v in model.getVars():
                if 'x' in v.varName and abs(v.x-1) <= 0.0001:  # avoid rounding error
                    name = v.varName
                    portfolio.append(name[name.find('[') + 1:-1])

            print(f'Mode: {mode_}')
            print(f'\t Objective Value: {model.ObjVal}')
            print(f'\t Optimal Portfolio:', ','.join(portfolio))
            print(f'\t Running Time: {model.RunTime}')
    print()
```

## Advanced Topics
So far, we have already handled order two and order three terms, but I want to provide the treatment for higher order terms. Basically, the extension of properties and theorems from [[2]](#2) can reach the goal. Thus, there are two corollaries below. The first one is the extension from proposition 1 and 2, and the second one is extended from theorem 1 in [[2]](#2). 

---

**<u>Corollary 1.</u>**
Let <!-- $m$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?m"> and <!-- $N$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?N"> be given positive integers such that <!-- $1 \leq m < N$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?1%20%5Cleq%20m%20%3C%20N"> and assume that <!-- $x_i \in \{0, 1\}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x_i%20%5Cin%20%5C%7B0%2C%201%5C%7D"> for <!-- $i = 1,
\ldots ,N$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?i%20%3D%201%2C%0A%5Cldots%20%2CN"> satisfying <!-- $\sum\limits_{i=1}^N{x_{i}}=m$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Csum%5Climits_%7Bi%3D1%7D%5EN%7Bx_%7Bi%7D%7D%3Dm">. For a set of non-negative variables <!-- $x^{[p]}_{i_1, i_2, \ldots i_p} \in [0, 1],~~ i_1, i_2, \ldots i_p \in \{1, \ldots ,N\}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x%5E%7B%5Bp%5D%7D_%7Bi_1%2C%20i_2%2C%20%5Cldots%20i_p%7D%20%5Cin%20%5B0%2C%201%5D%2C~~%20i_1%2C%20i_2%2C%20%5Cldots%20i_p%20%5Cin%20%5C%7B1%2C%20%5Cldots%20%2CN%5C%7D"> with all of the subscripts being distinct, if  

<!-- $$
\begin{aligned}
& \sum\limits_{i_1 < i_2}^N \sum\limits_{i_2<i_3}^N \cdots \sum\limits_{i_{p-1} < i_p}^N {x^{[p]}_{i_1, i_2, \ldots i_p}} + \\
& \sum\limits_{i_2 < i_1}^N \sum\limits_{i_1<i_3}^N \cdots \sum\limits_{i_{p-1} < i_p}^N {x^{[p]}_{i_2, i_1, \ldots i_p}} + \cdots +\\
& \sum\limits_{i_2 < i_3}^N \sum\limits_{i_3<i_4}^N \cdots \sum\limits_{i_p < i_1}^N {x^{[p]}_{i_2, i_3, \ldots i_1}} = {m-1 \choose p-1} x_{i_1},~ \text{for}~ i_1 = 1, \ldots ,N\text{,}
\end{aligned}
$$ --> 

<div align="center"><img style="background: white;" src="https://latex.codecogs.com/svg.latex?%5Cbegin%7Baligned%7D%0A%26%20%5Csum%5Climits_%7Bi_1%20%3C%20i_2%7D%5EN%20%5Csum%5Climits_%7Bi_2%3Ci_3%7D%5EN%20%5Ccdots%20%5Csum%5Climits_%7Bi_%7Bp-1%7D%20%3C%20i_p%7D%5EN%20%7Bx%5E%7B%5Bp%5D%7D_%7Bi_1%2C%20i_2%2C%20%5Cldots%20i_p%7D%7D%20%2B%20%5C%5C%0A%26%20%5Csum%5Climits_%7Bi_2%20%3C%20i_1%7D%5EN%20%5Csum%5Climits_%7Bi_1%3Ci_3%7D%5EN%20%5Ccdots%20%5Csum%5Climits_%7Bi_%7Bp-1%7D%20%3C%20i_p%7D%5EN%20%7Bx%5E%7B%5Bp%5D%7D_%7Bi_2%2C%20i_1%2C%20%5Cldots%20i_p%7D%7D%20%2B%20%5Ccdots%20%2B%5C%5C%0A%26%20%5Csum%5Climits_%7Bi_2%20%3C%20i_3%7D%5EN%20%5Csum%5Climits_%7Bi_3%3Ci_4%7D%5EN%20%5Ccdots%20%5Csum%5Climits_%7Bi_p%20%3C%20i_1%7D%5EN%20%7Bx%5E%7B%5Bp%5D%7D_%7Bi_2%2C%20i_3%2C%20%5Cldots%20i_1%7D%7D%20%3D%20%7Bm-1%20%5Cchoose%20p-1%7D%20x_%7Bi_1%7D%2C~%20%5Ctext%7Bfor%7D~%20i_1%20%3D%201%2C%20%5Cldots%20%2CN%5Ctext%7B%2C%7D%0A%5Cend%7Baligned%7D"></div>

then <!-- $x_{i_1}x_{i_2} \cdots x_{i_p} = x^{[p]}_{i_1, i_2, \ldots i_p}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x_%7Bi_1%7Dx_%7Bi_2%7D%20%5Ccdots%20x_%7Bi_p%7D%20%3D%20x%5E%7B%5Bp%5D%7D_%7Bi_1%2C%20i_2%2C%20%5Cldots%20i_p%7D">

**<u>Proof.</u>**
If <!-- $N > p$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?N%20%3E%20p"> and denote <!-- $\mathcal{A} = \{i | x_i=1 \} \subseteq \{1, 2, \ldots, N\}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Cmathcal%7BA%7D%20%3D%20%5C%7Bi%20%7C%20x_i%3D1%20%5C%7D%20%5Csubseteq%20%5C%7B1%2C%202%2C%20%5Cldots%2C%20N%5C%7D">, then there are <!-- $m$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?m"> elements in  <!-- $\mathcal{A}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Cmathcal%7BA%7D">. We have <!-- $x^{[p]}_{i_1, i_2, \ldots i_p} = x_1 x_2 \ldots x_p = 0$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x%5E%7B%5Bp%5D%7D_%7Bi_1%2C%20i_2%2C%20%5Cldots%20i_p%7D%20%3D%20x_1%20x_2%20%5Cldots%20x_p%20%3D%200"> if and only if <!-- $i_1, i_2, \cdots i_{p-1}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?i_1%2C%20i_2%2C%20%5Ccdots%20i_%7Bp-1%7D"> and <!-- $i_p$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?i_p"> is not in <!-- $\mathcal{A}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Cmathcal%7BA%7D">. For any <!-- $i_1' \in \mathcal{A}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?i_1'%20%5Cin%20%5Cmathcal%7BA%7D">, the value of the right-hand side is <!-- ${m-1 \choose p-1}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%7Bm-1%20%5Cchoose%20p-1%7D">. Since there are <!-- ${m-1 \choose p-1}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%7Bm-1%20%5Cchoose%20p-1%7D"> possible nonzero terms like <!-- $x^{[p]}_{i_1', i_2', \ldots i_p'}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x%5E%7B%5Bp%5D%7D_%7Bi_1'%2C%20i_2'%2C%20%5Cldots%20i_p'%7D">, <!-- $x^{[p]}_{i_2', i_1', \ldots i_p'}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x%5E%7B%5Bp%5D%7D_%7Bi_2'%2C%20i_1'%2C%20%5Cldots%20i_p'%7D"> and <!-- $x^{[p]}_{i_2', i_3', \ldots i_1'}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x%5E%7B%5Bp%5D%7D_%7Bi_2'%2C%20i_3'%2C%20%5Cldots%20i_1'%7D"> for <!-- $i_2', \ldots i_p' \in \mathcal{A}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?i_2'%2C%20%5Cldots%20i_p'%20%5Cin%20%5Cmathcal%7BA%7D"> on the left-hand side, and all <!-- $x^{[p]}_{i_1, i_2, \ldots i_p}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x%5E%7B%5Bp%5D%7D_%7Bi_1%2C%20i_2%2C%20%5Cldots%20i_p%7D">'s are no more than 1, it follows that <!-- $x^{[p]}_{i_1', i_2', \ldots i_p'} = x_{i_1'} x_{i_2'} \cdots x_{i_p'}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x%5E%7B%5Bp%5D%7D_%7Bi_1'%2C%20i_2'%2C%20%5Cldots%20i_p'%7D%20%3D%20x_%7Bi_1'%7D%20x_%7Bi_2'%7D%20%5Ccdots%20x_%7Bi_p'%7D"> for <!-- $i_1', i_2', \ldots i_p' \in \mathcal{A}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?i_1'%2C%20i_2'%2C%20%5Cldots%20i_p'%20%5Cin%20%5Cmathcal%7BA%7D"> and <!-- $i_1' < i_2' < \ldots < i_p'$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?i_1'%20%3C%20i_2'%20%3C%20%5Cldots%20%3C%20i_p'">.

---


**<u>Corollary 2.</u>**
For a vector <!-- $\mathbf{x} = (x_1, \ldots , x_N) \in \{0, 1\}^N$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Cmathbf%7Bx%7D%20%3D%20(x_1%2C%20%5Cldots%20%2C%20x_N)%20%5Cin%20%5C%7B0%2C%201%5C%7D%5EN">, one set of non-negative variables <!-- $x^{[p]}_{i_1, i_2, \ldots i_p} \in [0, 1],\; i_1, i_2, \ldots i_p \in \{1, \ldots ,N\}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x%5E%7B%5Bp%5D%7D_%7Bi_1%2C%20i_2%2C%20%5Cldots%20i_p%7D%20%5Cin%20%5B0%2C%201%5D%2C%5C%3B%20i_1%2C%20i_2%2C%20%5Cldots%20i_p%20%5Cin%20%5C%7B1%2C%20%5Cldots%20%2CN%5C%7D">, and one set of non-negative variables <!-- $x^{[p+1]}_{i_1, i_2, \ldots i_{p+1}} \in [0, 1],\; i_1, i_2, \ldots i_p, i_{p+1} \in \{1, \ldots ,N\}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x%5E%7B%5Bp%2B1%5D%7D_%7Bi_1%2C%20i_2%2C%20%5Cldots%20i_%7Bp%2B1%7D%7D%20%5Cin%20%5B0%2C%201%5D%2C%5C%3B%20i_1%2C%20i_2%2C%20%5Cldots%20i_p%2C%20i_%7Bp%2B1%7D%20%5Cin%20%5C%7B1%2C%20%5Cldots%20%2CN%5C%7D"> with all of the subscripts being distinct and <!-- $p+1 \leq m < N$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?p%2B1%20%5Cleq%20m%20%3C%20N">, where <!-- $m$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?m"> and <!-- $N$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?N"> are two integer variables. Let <!-- $r_{i_1, i_2, \ldots i_p}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?r_%7Bi_1%2C%20i_2%2C%20%5Cldots%20i_p%7D"> be the additional benefit from implementing project <!-- $i_1, i_2, \cdots ,i_{p-1}, i_p$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?i_1%2C%20i_2%2C%20%5Ccdots%20%2Ci_%7Bp-1%7D%2C%20i_p"> simultaneously. If the constraints from **<u>Corollary 1.</u>** with <!-- $p \rightarrow p$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?p%20%5Crightarrow%20p"> and <!-- $p \rightarrow p +1$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?p%20%5Crightarrow%20p%20%2B1">, and <!-- $\sum_{i=1}^N x_i = 1$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Csum_%7Bi%3D1%7D%5EN%20x_i%20%3D%201"> are satisfied, then  

<!-- $$
\sum\limits_{i_1 = 1}^N \sum\limits_{i_2 > i_1}^N \cdots \sum\limits_{i_{p} > i_{p-1}}^N (r_{i_1, i_2, \ldots i_p}) {x^{[p]}_{i_1, i_2, \ldots i_p}} = \frac{1}{m-p}\sum\limits_{i_1 = 1}^N \sum\limits_{i_2 > i_1}^N \cdots \sum\limits_{i_p > ~ i_{p-1}}^N \sum\limits_{i_{p+1} > i_p}^N (r_{i_1, i_2 \ldots i_p} + r_{i_1, i_3, \ldots i_{p+1}} + r_{i_1, i_4, \ldots i_{p+1}} + \cdots + r_{i_2, i_3, \ldots i_{p+1}})  x^{[p+1]}_{i_1, i_2, \ldots i_{p+1}}
$$ --> 

<div align="center"><img style="background: white;" src="https://latex.codecogs.com/svg.latex?%5Csum%5Climits_%7Bi_1%20%3D%201%7D%5EN%20%5Csum%5Climits_%7Bi_2%20%3E%20i_1%7D%5EN%20%5Ccdots%20%5Csum%5Climits_%7Bi_%7Bp%7D%20%3E%20i_%7Bp-1%7D%7D%5EN%20(r_%7Bi_1%2C%20i_2%2C%20%5Cldots%20i_p%7D)%20%7Bx%5E%7B%5Bp%5D%7D_%7Bi_1%2C%20i_2%2C%20%5Cldots%20i_p%7D%7D%20%3D%20%5Cfrac%7B1%7D%7Bm-p%7D%5Csum%5Climits_%7Bi_1%20%3D%201%7D%5EN%20%5Csum%5Climits_%7Bi_2%20%3E%20i_1%7D%5EN%20%5Ccdots%20%5Csum%5Climits_%7Bi_p%20%3E%20~%20i_%7Bp-1%7D%7D%5EN%20%5Csum%5Climits_%7Bi_%7Bp%2B1%7D%20%3E%20i_p%7D%5EN%20(r_%7Bi_1%2C%20i_2%20%5Cldots%20i_p%7D%20%2B%20r_%7Bi_1%2C%20i_3%2C%20%5Cldots%20i_%7Bp%2B1%7D%7D%20%2B%20r_%7Bi_1%2C%20i_4%2C%20%5Cldots%20i_%7Bp%2B1%7D%7D%20%2B%20%5Ccdots%20%2B%20r_%7Bi_2%2C%20i_3%2C%20%5Cldots%20i_%7Bp%2B1%7D%7D)%20%20x%5E%7B%5Bp%2B1%5D%7D_%7Bi_1%2C%20i_2%2C%20%5Cldots%20i_%7Bp%2B1%7D%7D"></div>

**<u>Proof.</u>**
If <!-- $p+1 \leq m < N$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?p%2B1%20%5Cleq%20m%20%3C%20N">, there exist unique <!-- $i_1', i_2', \ldots i_m'$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?i_1'%2C%20i_2'%2C%20%5Cldots%20i_m'"> such that <!-- $x_{i_1'}, x_{i_2'}, \ldots x_{i_m'} = 1$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x_%7Bi_1'%7D%2C%20x_%7Bi_2'%7D%2C%20%5Cldots%20x_%7Bi_m'%7D%20%3D%201">. Denote <!-- $\mathcal{A} = \{i_1', i_2', \ldots i_m'\}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Cmathcal%7BA%7D%20%3D%20%5C%7Bi_1'%2C%20i_2'%2C%20%5Cldots%20i_m'%5C%7D">.
1. It is clear that when any <!-- $p$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?p"> projects are selected (i.e., if <!-- $x_{i_1'}=x_{i_2'}= \cdots = x_{i_p'} = 1$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x_%7Bi_1'%7D%3Dx_%7Bi_2'%7D%3D%20%5Ccdots%20%3D%20x_%7Bi_p'%7D%20%3D%201"> then <!-- $x^{[p]}_{i_1', i_2', \ldots, i_p'} = 1$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x%5E%7B%5Bp%5D%7D_%7Bi_1'%2C%20i_2'%2C%20%5Cldots%2C%20i_p'%7D%20%3D%201">), the left-hand side becomes <!-- $\sum\limits_{i_1 = 1}^N \sum\limits_{i_2 > i_1}^N \cdots \sum\limits_{i_{p} > i_{p-1}}^N (r_{i_1, i_2, \ldots i_p}) {x^{[p]}_{i_1, i_2, \ldots i_p}} = r_{i_1', i_2' \ldots i_p'} + r_{i_1', i_3', \ldots i_{p+1}'} + r_{i_2', i_3', \ldots i_{p+1}'} + \cdots + r_{i_{m-(p-1)}', i_{m-(p-2)}', \ldots, i_{m-1}', i_{m}'}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Csum%5Climits_%7Bi_1%20%3D%201%7D%5EN%20%5Csum%5Climits_%7Bi_2%20%3E%20i_1%7D%5EN%20%5Ccdots%20%5Csum%5Climits_%7Bi_%7Bp%7D%20%3E%20i_%7Bp-1%7D%7D%5EN%20(r_%7Bi_1%2C%20i_2%2C%20%5Cldots%20i_p%7D)%20%7Bx%5E%7B%5Bp%5D%7D_%7Bi_1%2C%20i_2%2C%20%5Cldots%20i_p%7D%7D%20%3D%20r_%7Bi_1'%2C%20i_2'%20%5Cldots%20i_p'%7D%20%2B%20r_%7Bi_1'%2C%20i_3'%2C%20%5Cldots%20i_%7Bp%2B1%7D'%7D%20%2B%20r_%7Bi_2'%2C%20i_3'%2C%20%5Cldots%20i_%7Bp%2B1%7D'%7D%20%2B%20%5Ccdots%20%2B%20r_%7Bi_%7Bm-(p-1)%7D'%2C%20i_%7Bm-(p-2)%7D'%2C%20%5Cldots%2C%20i_%7Bm-1%7D'%2C%20i_%7Bm%7D'%7D">
2. Similarily, when any <!-- $p+1$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?p%2B1"> projects are selected (i.e., if <!-- $x_{i_1'}=x_{i_2'}= \cdots = x_{i_p'} = x_{i_{p+1}}' = 1$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x_%7Bi_1'%7D%3Dx_%7Bi_2'%7D%3D%20%5Ccdots%20%3D%20x_%7Bi_p'%7D%20%3D%20x_%7Bi_%7Bp%2B1%7D%7D'%20%3D%201"> then <!-- $x^{[p+1]}_{i_1', i_2', \ldots, i_p', i_{p+1}'} = 1$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x%5E%7B%5Bp%2B1%5D%7D_%7Bi_1'%2C%20i_2'%2C%20%5Cldots%2C%20i_p'%2C%20i_%7Bp%2B1%7D'%7D%20%3D%201">), the right-hand side becomes <!-- $\frac{1}{m-p}\sum\limits_{i_1 = 1}^N \sum\limits_{i_2 > i_1}^N \cdots \sum\limits_{i_p > ~ i_{p-1}}^N \sum\limits_{i_{p+1} > i_p}^N (r_{i_1, i_2 \ldots i_p} + r_{i_1, i_3, \ldots i_{p+1}} + r_{i_1, i_4, \ldots i_{p+1}} + \cdots + r_{i_2, i_3, \ldots i_{p+1}})  x^{[p+1]}_{i_1, i_2, \ldots i_{p+1}} =r_{i_1', i_2' \ldots i_p'} + r_{i_1', i_3', \ldots i_{p+1}'} + r_{i_2', i_3', \ldots i_{p+1}'} + \cdots + r_{i_{m-(p-1)}', i_{m-(p-2)}', \ldots, i_{m-1}', i_{m}'}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%5Cfrac%7B1%7D%7Bm-p%7D%5Csum%5Climits_%7Bi_1%20%3D%201%7D%5EN%20%5Csum%5Climits_%7Bi_2%20%3E%20i_1%7D%5EN%20%5Ccdots%20%5Csum%5Climits_%7Bi_p%20%3E%20~%20i_%7Bp-1%7D%7D%5EN%20%5Csum%5Climits_%7Bi_%7Bp%2B1%7D%20%3E%20i_p%7D%5EN%20(r_%7Bi_1%2C%20i_2%20%5Cldots%20i_p%7D%20%2B%20r_%7Bi_1%2C%20i_3%2C%20%5Cldots%20i_%7Bp%2B1%7D%7D%20%2B%20r_%7Bi_1%2C%20i_4%2C%20%5Cldots%20i_%7Bp%2B1%7D%7D%20%2B%20%5Ccdots%20%2B%20r_%7Bi_2%2C%20i_3%2C%20%5Cldots%20i_%7Bp%2B1%7D%7D)%20%20x%5E%7B%5Bp%2B1%5D%7D_%7Bi_1%2C%20i_2%2C%20%5Cldots%20i_%7Bp%2B1%7D%7D%20%3Dr_%7Bi_1'%2C%20i_2'%20%5Cldots%20i_p'%7D%20%2B%20r_%7Bi_1'%2C%20i_3'%2C%20%5Cldots%20i_%7Bp%2B1%7D'%7D%20%2B%20r_%7Bi_2'%2C%20i_3'%2C%20%5Cldots%20i_%7Bp%2B1%7D'%7D%20%2B%20%5Ccdots%20%2B%20r_%7Bi_%7Bm-(p-1)%7D'%2C%20i_%7Bm-(p-2)%7D'%2C%20%5Cldots%2C%20i_%7Bm-1%7D'%2C%20i_%7Bm%7D'%7D">. Without loss of generality, we can take <!-- $r_{i_1', i_2' \ldots i_p'}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?r_%7Bi_1'%2C%20i_2'%20%5Cldots%20i_p'%7D"> for example. In the RHS, <!-- $x^{[p+1]}_{i_1', i_2' \ldots i_p', j} = 1$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?x%5E%7B%5Bp%2B1%5D%7D_%7Bi_1'%2C%20i_2'%20%5Cldots%20i_p'%2C%20j%7D%20%3D%201">, where <!-- $j \in \mathcal{B} = \mathcal{A} \backslash \{i_1', i_2' \ldots i_p'\}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?j%20%5Cin%20%5Cmathcal%7BB%7D%20%3D%20%5Cmathcal%7BA%7D%20%5Cbackslash%20%5C%7Bi_1'%2C%20i_2'%20%5Cldots%20i_p'%5C%7D"> with <!-- $|\mathcal{B}| = m - p$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?%7C%5Cmathcal%7BB%7D%7C%20%3D%20m%20-%20p">. It shows that <!-- $r_{i_1', i_2' \ldots i_p'}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?r_%7Bi_1'%2C%20i_2'%20%5Cldots%20i_p'%7D"> will repeat <!-- $m - p$ --> <img style="transform: translateY(0.1em); background: white;" src="https://latex.codecogs.com/svg.latex?m%20-%20p"> times compared to LHS, so there is a coefficient <!-- $\frac{1}{m-p}$ --> <img style="background: white;" src="https://latex.codecogs.com/svg.latex?%5Cfrac%7B1%7D%7Bm-p%7D"> in front of the summation.

Proved.
    
> With **<u>Corollary 2.</u>**, one can extend propsion 3, 4 and 5 in [[2]](#2) easily.


## References
<a id="1">[1]</a> Xingmei Li, Yao-Huei Huang, Shu-Cherng Fang and Zhibin Deng (2016), Reformulations for project portfolio selection problem considering interdependence and cardinality, *Pacific Journal of Optimization*, 12(2), 355-366.  
<a id="1">[2]</a> Xingmei Li, Yao-Huei Huang , Shu-Cherng Fang , Youzhong Zhang (2020), An alternative efficient representation for the project portfolio selection problem, *European Journal of Operational Research*, 281(1), 100-113.



