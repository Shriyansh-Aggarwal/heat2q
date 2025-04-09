import numpy as np
import matplotlib.pyplot as plt

class Heatmap:
    seed = None
    heatmap = None
    dim_x = 1
    dim_y = 1
    qbits = 1

    def __init__(self, seed=None, dim_x=1, dim_y=dim_x):
        self.seed = seed
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.qbits = int(np.ceil(np.log2(dim_x*dim_y)))

    def _normalize_heatmap(self, heatmap):
        self.heatmap = heatmap / np.sum(heatmap)
        return

    def create_random_heatmap(self):
        if self.seed is not None:
            np.random.seed(self.seed)
        self.heatmap = np.random.rand(self.dim_x, self.dim_y)
        self._normalize_heatmap(self.heatmap)
        return

    def create_gaussian_heatmap(self, sigma=4.0):
        x = np.linspace(0, self.dim_x - 1, self.dim_x)
        y = np.linspace(0, self.dim_y - 1, self.dim_y)
        x, y = np.meshgrid(x, y)

        mu_x = (self.dim_x - 1) / 2
        mu_y = (self.dim_y - 1) / 2
        self.heatmap = np.exp(-((x - mu_x)**2 + (y - mu_y)**2) / (2 * sigma**2))
        self._normalize_heatmap(self.heatmap)
        return 

    def use_heatmap(self, heatmap):
        self.dim_x, self.dim_y = np.shape(heatmap)
        self._normalize_heatmap(heatmap)
        return
    
    def get_amps(self):
        amps = np.pad(np.sqrt(self.heatmap.flatten()), (0, (2**self.qbits) - (self.dim_x * self.dim_y)), mode='constant')
        return amps
    
    def visual(self):
        half_x = self.dim_x // 2
        half_y = self.dim_y // 2
        extent = [-half_x, half_x, -half_y, half_y]
        plt.imshow(self.heatmap, cmap='hot', extent=extent, origin='lower', interpolation='nearest')
        plt.colorbar(label='Probability')
        plt.title(f'{self.dim_x}x{self.dim_y} Heatmap | Seed: {self.seed}')
        plt.show()