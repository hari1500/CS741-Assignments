def XOR_sum(n):
    count = 0
    while (n):
        n &= (n-1) 
        count+= 1

    return count%2