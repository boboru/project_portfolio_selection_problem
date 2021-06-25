import numpy as np
import gurobipy as gp
from gurobipy import GRB

def PPSP_solver(N, m, r_i, r_ij, r_ijk, d_i, d_ij, d_ijk, b, mode='proposed', equality=True, time_limit=3600, is_quiet=True):
    model = gp.Model('PPSP')
    model.setParam('OutputFlag', not is_quiet)  # mute
    model.setParam('TimeLimit', time_limit)  # the time limit is 3600 seconds 
    
    if mode == 'conventional':  # conventional models
        if equality == True:  # model 2-1, ECC
            x_list = []
            y_list = []
            z_list = []
            
            for i in range(N):
                x_list.append(i)
                for j in range(N):
                    if j > i:
                        y_list.append((i, j))
                    for k in range(N):
                        if j > i and k > j:
                            z_list.append((i, j, k))
                        
            
            x = model.addVars(x_list, vtype=GRB.BINARY, name='x')
            y = model.addVars(y_list, lb=0.0, ub=1, vtype=GRB.CONTINUOUS, name='y')
            z = model.addVars(z_list, lb=0.0, ub=1, vtype=GRB.CONTINUOUS, name='z')
            
            model.update()
                
            expr = gp.LinExpr()
            
            for i in range(N):
                expr.addTerms(r_i[i], x[i])
                
                for j in range(N):
                    if j > i:
                        expr.addTerms(r_ij[i, j], y[i, j])
                    
                    for k in range(N):
                        if j > i and k > j:
                            expr.addTerms(r_ijk[i, j, k], z[i, j, k])
                            
            model.setObjective(expr, GRB.MAXIMIZE)
            
            # Constraints
            
            ## C7
            expr = gp.LinExpr()
            for i in range(N):
                expr.addTerms(d_i[i], x[i])
                
                for j in range(N):
                    if j > i:
                        expr.addTerms(-d_ij[i, j], y[i, j])
                        
                    for k in range(N):
                        if j > i and k > j:
                            expr.addTerms(d_ijk[i, j, k], z[i, j, k])
            model.addLConstr(expr, GRB.LESS_EQUAL, b, 'C7')
            
            ## C8
            model.addLConstr(gp.quicksum(x[i] for i in range(N)) == m, 'C8')
            
                            
            ## C9
            for i in range(N):
                expr = gp.LinExpr()
                
                for j in range(N):
                    if j > i:
                        expr.addTerms(1, y[i, j])
                    elif j < i:
                        expr.addTerms(1, y[j, i])
                        
                    for k in range(N):
                        if j > i and k > j:
                            expr.addTerms(1, z[i, j, k])
                        elif i > j and k > i:
                            expr.addTerms(1, z[j, i, k])
                        elif k > j and i > k:
                            expr.addTerms(1, z[j, k, i])
                
                expr.addTerms(-m*(m-1)/2, x[i])
                model.addLConstr(expr, GRB.EQUAL, 0, f'C9_{i}')

        else:  # model 2-2, IECC
            x_list = []
            y_list = []
            z_list = []
            
            for i in range(N):
                x_list.append(i)
                for j in range(N):
                    if j > i:
                        y_list.append((i, j))
                    for k in range(N):
                        if j > i and k > j:
                            z_list.append((i, j, k))
                        
            
            x = model.addVars(x_list, vtype=GRB.BINARY, name='x')
            y = model.addVars(y_list, lb=0.0, ub=1, vtype=GRB.CONTINUOUS, name='y')
            z = model.addVars(z_list, lb=0.0, ub=1, vtype=GRB.CONTINUOUS, name='z')
            u = model.addVars(m, vtype=GRB.BINARY, name='u')
            phi = model.addVars(N, lb=0.0, vtype=GRB.CONTINUOUS, name='phi')
            bigM = m*(m-1)/2
            
            
            model.update()
                
            expr = gp.LinExpr()
            
            for i in range(N):
                expr.addTerms(r_i[i], x[i])
                
                for j in range(N):
                    if j > i:
                        expr.addTerms(r_ij[i, j], y[i, j])
                    
                    for k in range(N):
                        if j > i and k > j:
                            expr.addTerms(r_ijk[i, j, k], z[i, j, k])
                            
            model.setObjective(expr, GRB.MAXIMIZE)
            
            # Constraints
            ## C7
            expr = gp.LinExpr()
            for i in range(N):
                expr.addTerms(d_i[i], x[i])
                
                for j in range(N):
                    if j > i:
                        expr.addTerms(-d_ij[i, j], y[i, j])
                        
                    for k in range(N):
                        if j > i and k > j:
                            expr.addTerms(d_ijk[i, j, k], z[i, j, k])
            model.addLConstr(expr, GRB.LESS_EQUAL, b, 'C7')
            
            ## C10
            model.addLConstr(gp.quicksum(x[i] for i in range(N)) == gp.quicksum((t+1) * u[t] for t in range(m)), 'C10')
            
            ## C11
            model.addLConstr(gp.quicksum(u[t] for t in range(m)) == 1, 'C11')
            
            ## C12, C13
            for i in range(N):
                model.addLConstr(gp.quicksum(t*(t+1)/2*u[t] + bigM * (x[i]-1) for t in range(m)) <=  phi[i], f'C12_L_{i}')
                model.addLConstr(phi[i] <= gp.quicksum(t*(t+1)/2*u[t] + bigM * (1-x[i]) for t in range(m)), f'C12_R_{i}')
                model.addLConstr(phi[i] <= bigM * x[i], f'C13_{i}')
                
            ## C15
            for i in range(N):
                expr = gp.LinExpr()
                
                for j in range(N):
                    if j > i:
                        expr.addTerms(1, y[i, j])
                    elif j < i:
                        expr.addTerms(1, y[j, i])
                        
                    for k in range(N):
                        if j > i and k > j:
                            expr.addTerms(1, z[i, j, k])
                        elif j < i and k > i:
                            expr.addTerms(1, z[j, i, k])
                        elif j < k and k < i:
                            expr.addTerms(1, z[j, k, i])
                
                expr.addTerms(-1, phi[i])
                model.addLConstr(expr, GRB.EQUAL, 0, 'C15')
    else:  # proposed models
        if equality == True:  # model 3-1, ECC
            x_list = []
            z_list = []
            
            for i in range(N):
                x_list.append(i)
                for j in range(N):
                    for k in range(N):
                        if j > i and k > j:
                            z_list.append((i, j, k))
                        
            
            x = model.addVars(x_list, vtype=GRB.BINARY, name='x')
            z = model.addVars(z_list, lb=0.0, ub=1, vtype=GRB.CONTINUOUS, name='z')
            
            model.update()
                
            expr = gp.LinExpr()
            
            for i in range(N):
                expr.addTerms(r_i[i], x[i])
                
                for j in range(N):
                    for k in range(N):
                        if j > i and k > j:
                            expr.addTerms(1/(m-2)*(r_ij[i, j]+r_ij[i, k]+r_ij[j, k]), z[i, j, k])
                            expr.addTerms(r_ijk[i, j, k], z[i, j, k])
                            
            model.setObjective(expr, GRB.MAXIMIZE)
            
            # Constraints
            
            ## C8
            model.addLConstr(gp.quicksum(x[i] for i in range(N)) == m, 'C8')
            
                            
            ## C17
            for i in range(N):
                expr = gp.LinExpr()
                
                for j in range(N):
                    for k in range(N):
                        if j > i and k > j:
                            expr.addTerms(1, z[i, j, k])
                        elif i > j and k > i:
                            expr.addTerms(1, z[j, i, k])
                        elif k > j and i > k:
                            expr.addTerms(1, z[j, k, i])
                
                expr.addTerms(-(m-1)*(m-2)/2, x[i])
                model.addLConstr(expr, GRB.EQUAL, 0, f'C17_{i}')
                
            ## C20
            expr = gp.LinExpr()
            for i in range(N):
                expr.addTerms(d_i[i], x[i])
                
                for j in range(N): 
                    for k in range(N):
                        if j > i and k > j:
                            expr.addTerms(-1 / (m-2) * (d_ij[i, j]+d_ij[i, k]+d_ij[j, k]), z[i, j, k])
                            expr.addTerms(d_ijk[i, j, k], z[i, j, k])
            
            model.addLConstr(expr, GRB.LESS_EQUAL, b, 'C20')
        else:  # 3-2, IECC
            x_list = []
            z_list = []
            
            for i in range(N):
                x_list.append(i)
                for j in range(N):
                    for k in range(N):
                        if j > i and k > j:
                            z_list.append((i, j, k))
                        
            
            x = model.addVars(x_list, vtype=GRB.BINARY, name='x')
            z = model.addVars(z_list, lb=0.0, ub=1, vtype=GRB.CONTINUOUS, name='z')
            u = model.addVars(m-2 , vtype=GRB.BINARY, name='u')
            phi = model.addVars(N, lb=0.0, vtype=GRB.CONTINUOUS, name='phi')
            Q = model.addVars(N, lb=0.0, vtype=GRB.CONTINUOUS, name='Q')
            xi = model.addVar(lb=0.0, vtype=GRB.CONTINUOUS, name='xi')
            zeta = model.addVar(lb=0.0, vtype=GRB.CONTINUOUS, name='zeta')            
            bigM = 10 ** 9
            
            model.update()
                
            expr = gp.LinExpr()
            for i in range(N):
                expr.addTerms(r_i[i], x[i])
                
                for j in range(N):
                    for k in range(N):
                        if j > i and k > j:
                            expr.addTerms(r_ijk[i, j, k], z[i, j, k])
            
            expr.addTerms(1, xi)
            model.setObjective(expr, GRB.MAXIMIZE)
            
            # Constraints
            ## C21
            for t in range(m-2):
                expr = gp.LinExpr()
                expr.addTerms(bigM, u[t])
                expr.addConstant(-bigM)
                
                for i in range(N):
                    for j in range(N):                        
                        for k in range(N):
                            if j > i and k > j:
                                expr.addTerms(1/(t+1)*(r_ij[i, j] + r_ij[i, k] + r_ij[j, k]), z[i, j, k])
                expr.addTerms(-1, xi)
                model.addLConstr(expr, GRB.LESS_EQUAL, 0, f'C21_{t}')
                
            ## C22
            for t in range(m-2):
                expr = gp.LinExpr()
                expr.addConstant(bigM)
                expr.addTerms(-bigM, u[t])
                
                for i in range(N):
                    for j in range(N):                        
                        for k in range(N):
                            if j > i and k > j:
                                expr.addTerms(1/(t+1)*(r_ij[i, j] + r_ij[i, k] + r_ij[j, k]), z[i, j, k])
                expr.addTerms(-1, xi)
                model.addLConstr(expr, GRB.GREATER_EQUAL, 0, f'C22_{t}')
            
            ## C23
            for t in range(m-2):
                expr = gp.LinExpr()
                expr.addTerms(bigM, u[t])
                expr.addConstant(-bigM)
                
                for i in range(N):
                    for j in range(N):                        
                        for k in range(N):
                            if j > i and k > j:
                                expr.addTerms(1/(t+1)*(d_ij[i, j] + d_ij[i, k] + d_ij[j, k]), z[i, j, k])
                expr.addTerms(-1, zeta)
                model.addLConstr(expr, GRB.LESS_EQUAL, 0, f'C23_{t}')
                
            ## C24
            for t in range(m-2):
                expr = gp.LinExpr()
                expr.addConstant(bigM)
                expr.addTerms(-bigM, u[t])
                
                for i in range(N):
                    for j in range(N):                        
                        for k in range(N):
                            if j > i and k > j:
                                expr.addTerms(1/(t+1)*(d_ij[i, j] + d_ij[i, k] + d_ij[j, k]), z[i, j, k])
                expr.addTerms(-1, zeta)
                model.addLConstr(expr, GRB.GREATER_EQUAL, 0, f'C24_{t}')
            
            ## C26
            model.addLConstr(gp.quicksum(u[t] for t in range(m-2)) == 1, 'C26')
            
            ## C27
            model.addLConstr(gp.quicksum(x[i] for i in range(N)) == gp.quicksum((t+3) * u[t] for t in range(m-2)), 'C27')
            
            ## C28, C29, C30
            for i in range(N):
                model.addLConstr(phi[i] + Q[i] == (m-1) * (m-2) / 2 * (1-x[i]) + gp.quicksum((t+1) * (t+2) / 2 * u[t] for t in range(m-2)), f'C28_{i}')
                model.addLConstr(Q[i] <= (m-1) * (m-2) * (1-x[i]), f'C29_{i}')
                model.addLConstr(phi[i] <= (m-1) * (m-2) / 2 * x[i], f'C30_{i}')
            
            ## C32
            expr = gp.LinExpr()
            for i in range(N):
                expr.addTerms(d_i[i], x[i])
                for j in range(N):
                    for k in range(N):
                        if j > i and k > j:
                            expr.addTerms(d_ijk[i, j, k], z[i, j, k])
            
            expr.addTerms(-1, zeta)
            model.addLConstr(expr, GRB.LESS_EQUAL, b, f'C32')
                        
            
            ## C33
            for i in range(N):
                expr = gp.LinExpr()
                for j in range(N):                        
                    for k in range(N):
                        if j > i and k > j:
                            expr.addTerms(1, z[i, j, k])
                        elif j < i and k > i:
                            expr.addTerms(1, z[j, i, k])
                        elif j < k and k < i:
                            expr.addTerms(1, z[j, k, i])
                
                expr.addTerms(-1, phi[i])
                model.addLConstr(expr, GRB.EQUAL, 0, f'C33_{i}')
    
    model.optimize()
    
#     model.write('test.lp')

    if model.status == GRB.OPTIMAL:
        solution = model.getAttr('X', x)
#         print('optimal obj value:', model.objVal)
#         print('x:', solution)
    elif model.status == GRB.INF_OR_UNBD:
        print('Model is infeasible or unbounded')
    elif model.status == GRB.INFEASIBLE:
        print('Model is infeasible')
    elif model.status == GRB.UNBOUNDED:
        print('Model is unbounded')
    else:
        print('Optimization ended with status %d' % model.status)
    
    return model


def instance_generator(N, m):
    instance = {'N': N, 'm': m}
    r_i = {}
    r_ij = {}
    r_ijk = {}

    d_i = {}
    d_ij = {}
    d_ijk = {}
    
    G = 0
    for i in range(N):
        r_i[i] = np.random.randint(10, 101)
        d_i[i] = np.random.randint(1, 11)
        G += d_i[i]
        for j in range(N):
            if j > i:
                r_ij[i, j] = np.random.randint(50, 201)
                d_ij[i, j] = np.random.randint(5, 21)
                G -= d_ij[i, j]
            for k in range(N):
                if j > i and k > j:
                    r_ijk[i, j, k] = np.random.randint(101, 501)
                    d_ijk[i, j, k] = np.random.randint(10, 51)
                    G += d_ijk[i, j, k]
                    
    b = np.random.randint(0.05*G, 0.1*G + 1)
    
    instance['r_i'] = r_i
    instance['r_ij'] = r_ij
    instance['r_ijk'] = r_ijk
    instance['d_i'] = d_i
    instance['d_ij'] = d_ij
    instance['d_ijk'] = d_ijk
    instance['b'] = b
    
    return instance