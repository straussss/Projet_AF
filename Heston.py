import numpy as np
from scipy.stats import norm
from scipy.stats import multivariate_normal
import numpy as np

class Heston:
    def __init__(self,
                 spot: float,
                 strike: float,
                 rate: float,
                 dividend: float,
                 maturity: int,
                 volatility: float,
                 volatility_vol : float = 0.3,
                 mu: float = 0.1,
                 kappa: float = 2,
                 theta: float = 0.04,
                 rho: float = -0.2,
                 annual_basis: int = 365,
                 steps: int = 2,
                 paths: int = 5):
        """
        :param spot: spot price
        :param strike: strike price
        :param rate: risk free rate 0.05 corresponds to 5%
        :param dividend: dividend yield 0.01 corresponds to 1%
        :param maturity: maturity in days
        :param volatility: volatility 0.16 corresponds to 16%
        :param volatility_vol: volatility of volatility
        :param mu: drift of the stock process
        :param kappa: mean reversion coefficient of the variance process, ATTENTION CONDITION FELLER 2*kappa*theta > sigma^2
        :param theta: long term mean of the variance process
        :param rho:  correlation between W1 and W2, <W1,W2>
        :param steps:  number of steps
        :param paths:  number of paths
        """
        self.__spot = spot
        self.__strike = strike
        self.__rate = rate
        self.__dividend = dividend
        self.__maturity = maturity
        self._volatility = volatility
        self._volatility_vol = volatility_vol
        self.__mu = mu
        self.__kappa = kappa
        self.__theta = theta
        self.__rho = rho
        self.__annual_basis = annual_basis
        self.__steps = steps
        self.__paths = paths

        assert 2*kappa*theta > volatility**2, 'Feller condition not verified : 2*kappa*theta > volatility^2'

    @property
    def spot(self) -> float:
        return self.__spot

    @property
    def strike(self) -> float:
        return self.__strike

    @property
    def rate(self) -> float:
        return self.__rate

    @property
    def dividend(self) -> float:
        return self.__dividend

    @property
    def maturity(self) -> int:
        return self.__maturity

    @property
    def volatility(self) -> float:
        return self._volatility

    @property
    def volatility_vol(self) -> float:
        return self._volatility_vol

    @property
    def mu(self) -> float:
        return self.__mu

    @property
    def kappa(self) -> float:
        return self.__kappa

    @property
    def theta(self) -> float:
        return self.__theta

    @property
    def rho(self) -> float:
        return self.__rho

    @property
    def annual_basis(self) -> float:
        return self.__annual_basis

    @property
    def steps(self) -> int:
        return self.__steps

    @property
    def paths(self) -> int:
        return self.__paths

    ################################################### MONTE CARLO ####################################################

    @property
    def W(self) -> tuple:
        MU = np.array([0, 0])
        COV = np.matrix([[1, self.rho], [self.rho, 1]])
        W = multivariate_normal.rvs(mean=MU, cov=COV, size=(self.paths, self.steps-1))
        return W, W[:, 0], W[:, 1]
    
    @property
    def mc_paths(self) -> np.matrix:
        S = np.zeros((self.paths, self.steps))
        S[:, 0] = self.spot
        V = np.zeros((self.paths, self.steps))
        V[:, 0] = self.volatility


