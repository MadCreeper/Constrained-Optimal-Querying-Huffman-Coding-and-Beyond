from matplotlib import pyplot as plt
import numpy as np
import scipy.stats as stats

def plot_hist(data):
    plt.xlabel("Number of queries (t)")
    plt.ylabel("Frequency")
    plt.hist(data, bins=40, density=True,label="queries")
    
    
    

if __name__ == "__main__":
    data = []
    with open("tries_num_log.txt", 'r') as f:
        for line in f:
            data.append(int(line))
    mu = np.mean(data)
    var = np.var(data)
    sigma = np.sqrt(var)
    print(mu, sigma)
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    plot_hist(data)
    plt.plot(x, stats.norm.pdf(x, mu, sigma),'r',label=f"Normal curve")
    plt.show()
    
