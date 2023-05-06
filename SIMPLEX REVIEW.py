import numpy as np

def simplex(c, A, b):   

    # Add slack variables
    A = np.hstack((A, np.identity(len(A)))) # Adding coefficients of Slacks
    c = np.hstack((c, np.zeros(len(A[0])-len(c)))) # Adding 0s to last row, no. of cols of A - no. of actual coefficients of C
    # Create initial tableau
    tableau = np.vstack((np.hstack((A, np.atleast_2d(b).T)), np.hstack((c, 0))))
    basic_variables = list(range(len(A[0])-len(A), len(A[0]))) # indices from no. of (cols-rows) to no. of cols; initially slacks
    print("Initial tableau:\n", tableau)
    print("Initial basic_variables' indices:\n", basic_variables)

    # Iterate until optimal solution is found or problem is unbounded
    while True:

        # Check for optimality or unboundedness
        if np.all(tableau[-1, :-1] <= 0): # If all the elements of last row are less than or equal to 0, the solution is optimised
            break
        pivot_column = np.argmax(tableau[-1, :-1]) # The index of the col(element) with max value (index of pivot col)

        # Select pivot row
        ratios = tableau[:-1, -1] / tableau[:-1, pivot_column] # The elements of last column are divided with elements of pivot column
        ratios[~(ratios >= 0)] = np.inf # This is for setting negative values in ratios as inf
        pivot_row = np.argmin(ratios) 

        # Check for unboundedness
        if ratios[pivot_row] == np.inf: # If the element in ratios column corresonding to pivot row is inf, the optimization is not possible
            return None, None

        # Update basic variables, the element corresponding to index of pivot row in basic variables is replaced with index of pivot column
        basic_variables[pivot_row] = pivot_column 

        # Perform pivot operation
        pivot_value = tableau[pivot_row, pivot_column]
        tableau[pivot_row, :] /= pivot_value # to create unity at pivot element
        for i in range(len(tableau)): # for number of rows in tableau
            if i != pivot_row:
                tableau[i, :] -= tableau[i, pivot_column] * tableau[pivot_row, :]
        print("Pivot element: ", pivot_value)
        print("New tableau:\n", tableau)
        print("Basic variables' indices in tableau for this iteration:\n",basic_variables)

    # Extract optimal solution and objective value
    optimal_solution = np.zeros(len(c))
    for i, j in enumerate(basic_variables):
        if j < len(c): # the indices of variables in o.f are only taken into account, slacks are left out
            optimal_solution[j] = tableau[i, -1]
    optimal_value = tableau[-1, -1]
    optimal_value = -optimal_value
    return optimal_solution, optimal_value

c = np.array([40, 30])
A = np.array([[1, 1], [2, 1]])
b = np.array([12, 16])
x, obj = simplex(c, A, b)
print("Optimal solution: ", x)
print("Optimal value: ", obj)


'''
print('==================================')
print('==================================')
-

c = np.array([1, 1])
A = np.array([[3, 2], [0, 1]])
b = np.array([5, 2])
x, obj = simplex(c, A, b)
print("Optimal solution: ", x)
print("Optimal value: ", obj)
'''
