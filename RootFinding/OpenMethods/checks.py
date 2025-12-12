class ConvStatus:
    
    CONVERGENT = 1
    DIVERGENT = -1


def convergence_status(
    error_history,
    iterations,
    max_iterations,
):
  
    
    # 1- converged
    if iterations < max_iterations:
        return ConvStatus.CONVERGENT
    
    # 2- Reached max iterations: check if diverging
    if iterations >= max_iterations:
        
        # Need at least 3 errors to determine trend
        if len(error_history) >= 3:
            
            last = error_history[-1]
            prev = error_history[-2]
            prev2 = error_history[-3]
        
        #  convergence rates
            r1 = (last / prev) if prev != 0 else float('inf')
            r2 = (prev / prev2) if prev2 != 0 else float('inf')
            avg_r = (r1 + r2) / 2.0
        
        # growing error
            if avg_r > 1.05:
                return ConvStatus.DIVERGENT
        
    
    return ConvStatus.DIVERGENT