# Project Portfolio Selection Problem (PPSP)
 Efficient formulations for PPSP problem considering cardinality and interdependence

# Higher Order

## From Prop 1, Prop 2
**<u>Corollary 1.</u>**
Let $m$ and $N$ be given positive integers such that $1 \leq m < N$ and assume that $x_i \in \{0, 1\}$ for $i = 1,
\ldots ,N$ satisfying $\sum\limits_{i=1}^N{x_{i}}=m$. For a set of non-negative variables $x^{[p]}_{i_1, i_2, \ldots i_p} \in [0, 1],~~ i_1, i_2, \ldots i_p \in \{1, \ldots ,N\}$ with all of the subscripts being distict, if  

$$\begin{align}
& \sum\limits_{i_1 < i_2}^N \sum\limits_{i_2<i_3}^N \cdots \sum\limits_{i_{p-1} ~ < i_p}^N {x^{[p]}_{i_1, i_2, \ldots i_p}} + \\
& \sum\limits_{i_2 < i_1}^N \sum\limits_{i_1<i_3}^N \cdots \sum\limits_{i_{p-1} ~ < i_p}^N {x^{[p]}_{i_2, i_1, \ldots i_p}} + \\
& \sum\limits_{i_2 < i_3}^N \sum\limits_{i_3<i_4}^N \cdots \sum\limits_{i_p < i_1}^N {x^{[p]}_{i_2, i_3, \ldots i_1}} = C^{m-1}_{p-1} x_{i_1},~ \text{for}~ i_1 = 1, \ldots ,N,
\end{align}$$

then $x_{i_1}x_{i_2} \ldots x_{i_p} = x^{[p]}_{i_1, i_2, \ldots i_p}$ with all of the subscripts of $x^{[p]}$ being distinct