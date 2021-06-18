# Project Portfolio Selection Problem (PPSP)
 Efficient formulations for PPSP problem considering cardinality and interdependence

# Higher Order

# Higher Order

## From Prop 1, Prop 2
**<u>Corollary 1.</u>**
Let $m$ and $N$ be given positive integers such that $1 \leq m < N$ and assume that $x_i \in \{0, 1\}$ for $i = 1,
\ldots ,N$ satisfying $\sum\limits_{i=1}^N{x_{i}}=m$. For a set of non-negative variables $x^{[p]}_{i_1, i_2, \ldots i_p} \in [0, 1],~~ i_1, i_2, \ldots i_p \in \{1, \ldots ,N\}$ with all of the subscripts being distict, if  

<!-- $$
\begin{aligned}
& \sum\limits_{i_1 < i_2}^N \sum\limits_{i_2<i_3}^N \cdots \sum\limits_{i_{p-1} ~ < i_p}^N {x^{[p]}_{i_1, i_2, \ldots i_p}} + \\
& \sum\limits_{i_2 < i_1}^N \sum\limits_{i_1<i_3}^N \cdots \sum\limits_{i_{p-1} ~ < i_p}^N {x^{[p]}_{i_2, i_1, \ldots i_p}} + \\
& \sum\limits_{i_2 < i_3}^N \sum\limits_{i_3<i_4}^N \cdots \sum\limits_{i_p < i_1}^N {x^{[p]}_{i_2, i_3, \ldots i_1}} = C^{m-1}_{p-1} x_{i_1},~ \text{for}~ i_1 = 1, \ldots ,N,
\end{aligned}
$$ --> 

<div align="center"><img style="background: white;" src="https://latex.codecogs.com/svg.latex?%5Cbegin%7Baligned%7D%0A%26%20%5Csum%5Climits_%7Bi_1%20%3C%20i_2%7D%5EN%20%5Csum%5Climits_%7Bi_2%3Ci_3%7D%5EN%20%5Ccdots%20%5Csum%5Climits_%7Bi_%7Bp-1%7D%20~%20%3C%20i_p%7D%5EN%20%7Bx%5E%7B%5Bp%5D%7D_%7Bi_1%2C%20i_2%2C%20%5Cldots%20i_p%7D%7D%20%2B%20%5C%5C%0A%26%20%5Csum%5Climits_%7Bi_2%20%3C%20i_1%7D%5EN%20%5Csum%5Climits_%7Bi_1%3Ci_3%7D%5EN%20%5Ccdots%20%5Csum%5Climits_%7Bi_%7Bp-1%7D%20~%20%3C%20i_p%7D%5EN%20%7Bx%5E%7B%5Bp%5D%7D_%7Bi_2%2C%20i_1%2C%20%5Cldots%20i_p%7D%7D%20%2B%20%5C%5C%0A%26%20%5Csum%5Climits_%7Bi_2%20%3C%20i_3%7D%5EN%20%5Csum%5Climits_%7Bi_3%3Ci_4%7D%5EN%20%5Ccdots%20%5Csum%5Climits_%7Bi_p%20%3C%20i_1%7D%5EN%20%7Bx%5E%7B%5Bp%5D%7D_%7Bi_2%2C%20i_3%2C%20%5Cldots%20i_1%7D%7D%20%3D%20C%5E%7Bm-1%7D_%7Bp-1%7D%20x_%7Bi_1%7D%2C~%20%5Ctext%7Bfor%7D~%20i_1%20%3D%201%2C%20%5Cldots%20%2CN%2C%0A%5Cend%7Baligned%7D"></div>


<!-- $$
\begin{aligned} 
f &= 2 + x + 3 \\
  &= 5 + x
\end{aligned}
$$ --> 

<div align="center"><img style="background: white;" src="https://render.githubusercontent.com/render/math?math=%5Cbegin%7Baligned%7D%20%0Af%20%26%3D%202%20%2B%20x%20%2B%203%20%5C%5C%0A%20%20%26%3D%205%20%2B%20x%0A%5Cend%7Baligned%7D"></div> 






then <!-- $x_{i_1}x_{i_2} \ldots x_{i_p} = x^{[p]}_{i_1, i_2, \ldots i_p}$ --> <img style="transform: translateY(0.1em); background: white;" src="https://render.githubusercontent.com/render/math?math=x_%7Bi_1%7Dx_%7Bi_2%7D%20%5Cldots%20x_%7Bi_p%7D%20%3D%20x%5E%7B%5Bp%5D%7D_%7Bi_1%2C%20i_2%2C%20%5Cldots%20i_p%7D"> with all of the subscripts of $x^{[p]}$ being distinct