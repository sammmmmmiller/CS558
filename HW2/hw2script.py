# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 16:21:23 2024

@author: Sam
"""
F = 20000 # Mb
d = 2 # Mbps
us = 30 # Mbps

def idk(N, ui, isClientServer):
    if isClientServer:
        return max(N * F/ us, F / d)
    else:
        return max(F / us, F / d, N * F / (us + (N * ui)))
    
N_lst = [10, 100, 1000] # peers
u_lst = [0.3, 0.7, 2] # Mbps

servers = {}
for N in N_lst:
    lst = []
    for u in u_lst:
        result = idk(N, u, True)
        print(N, u, result)
        lst.append(result)
    servers[N] = lst

p2ps = {}
for N in N_lst:
    lst = []
    for u in u_lst:
        result = idk(N, u, False)
        print(N, u, result)
        lst.append(result)
    p2ps[N] = lst
        
        
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

# Plot for each N value
for u_index, u in enumerate(u_lst):
    client_server_times = [servers[N][u_index] for N in N_lst]
    p2p_times = [p2ps[N][u_index] for N in N_lst]

    plt.plot(N_lst, client_server_times, label=f'Client-Server, u = {u} Mbps', marker='o')
    plt.plot(N_lst, p2p_times, label=f'P2P, u = {u} Mbps', marker='x')

plt.xlabel('Number of Peers (N)')
plt.ylabel('Minimum Distribution Time (s)')
plt.xscale('log')  # If the N values vary widely, a log scale might make the plot more readable
plt.yscale('log')  # Optional: Use if distribution times vary greatly
plt.title('Minimum Distribution Time Comparison of Client-Server and P2P Models')
plt.legend()
plt.show()