import numpy as np
from scipy.stats import norm


class VanillaOption:
    """
    Annual Basis default 365
    Annual Volatility: 0.16 for 16% annually
    Annual Rate: 0.03 for 3% annually
    Annual Dividend: 0.05 for 5% annually
    Maturity in days

    Pricing methods:
    BS --> Black & Scholes + Greeks

    """

    def __init__(self,
                 spot: float,
                 strike: int,
                 rate: float,
                 dividend: float,
                 maturity: int,
                 typ: str = 'C',
                 volatility: float = 0,
                 pricing_method: str = 'BS'):
        self.__typ = typ
        self.__spot = spot
        self.__strike = strike
        self.__rate = rate
        self.__dividend = dividend
        self.__maturity = maturity
        self.__volatility = volatility
        self.__pricing_method = pricing_method
        self.__annual_basis = 365

    @property
    def Volatility(self) -> float:
        return self.__volatility

    @Volatility.setter
    def Volatility(self, volatility):
        self.__volatility = volatility

    @property
    def Price(self) -> float:
        if self.__pricing_method == "BS":
            if self.__typ == 'C':
                return VanillaOption.pricing_call_bs(self.__spot, self.__strike, self.__rate, self.__dividend,
                                                     self.__volatility, self.__maturity, self.__annual_basis)
            if self.__typ == 'P':
                return VanillaOption.pricing_put_bs(self.__spot, self.__strike, self.__rate, self.__dividend,
                                                    self.__volatility, self.__maturity, self.__annual_basis)

    @property
    def Delta(self) -> float:
        if self.__pricing_method == "BS":
            if self.__typ == 'C':
                return VanillaOption.delta_call_bs(self.__spot, self.__strike, self.__rate, self.__dividend,
                                                   self.__volatility, self.__maturity, self.__annual_basis)
            if self.__typ == 'P':
                return VanillaOption.delta_put_bs(self.__spot, self.__strike, self.__rate, self.__dividend,
                                                  self.__volatility, self.__maturity, self.__annual_basis)

    @property
    def Theta(self) -> float:
        if self.__pricing_method == "BS":
            if self.__typ == 'C':
                return VanillaOption.theta_call_bs(self.__spot, self.__strike, self.__rate, self.__dividend,
                                                   self.__volatility, self.__maturity, self.__annual_basis)
            if self.__typ == 'P':
                return VanillaOption.theta_put_bs(self.__spot, self.__strike, self.__rate, self.__dividend,
                                                  self.__volatility, self.__maturity, self.__annual_basis)

    @property
    def Gamma(self) -> float:
        if self.__pricing_method == "BS":
            return VanillaOption.gamma_bs(self.__spot, self.__strike, self.__rate, self.__dividend,
                                          self.__volatility, self.__maturity, self.__annual_basis)

    @property
    def Vega(self) -> float:
        if self.__pricing_method == "BS":
            return VanillaOption.vega_bs(self.__spot, self.__strike, self.__rate, self.__dividend,
                                         self.__volatility, self.__maturity, self.__annual_basis)

    ############################################### BLACK & SCHOLES ####################################################
    @property
    def d1(self) -> float:
        return VanillaOption.c_d1(self.__spot, self.__strike, self.__rate, self.__dividend, self.__volatility,
                                  self.__maturity)

    @property
    def d2(self) -> float:
        return VanillaOption.c_d2(self.__spot, self.__strike, self.__rate, self.__dividend, self.__volatility,
                                  self.__maturity)

    @staticmethod
    def pricing_call_bs(s: float, k: float, r: float, q: float, sig: float, t: int, b=365) -> float:
        """
        :param s: spot price
        :param k: stirke price
        :param r: risk free rate 0.05 corresponds to 5%
        :param q: dividend yield 0.01 corresponds to 1%
        :param sig: volatility 0.16 corresponds to 16%
        :param t: maturity in days
        :param b: annual basis 365 days per year
        :return: the price of a call with the BS model
        """
        d1 = VanillaOption.c_d1(s, k, r, q, sig, t, b)
        d2 = VanillaOption.c_d2(s, k, r, q, sig, t, b)
        n_d1 = VanillaOption.n(d1)
        n_d2 = VanillaOption.n(d2)
        return s * n_d1 * np.exp(-q * t / b) - k * np.exp(-r * t / b) * n_d2

    @staticmethod
    def c_d1(s: float, k: float, r: float, q: float, sig: float, t: int, b=365) -> float:
        """
        :param s: spot price
        :param k: stirke price
        :param r: risk free rate 0.05 corresponds to 5%
        :param q: dividend yield 0.01 corresponds to 1%
        :param sig: volatility 0.16 corresponds to 16%
        :param t: maturity in days
        :param b: annual basis 365 days per year
        :return: the d1 of the BS model
        """
        return (np.log(s / k) + (r - q + 0.5 * (sig ** 2)) * t / b) / (sig * np.sqrt(t / b))

    @staticmethod
    def c_d2(s: float, k: float, r: float, q: float, sig: float, t: int, b=365) -> float:
        """
        :param s: spot price
        :param k: stirke price
        :param r: risk free rate 0.05 corresponds to 5%
        :param q: dividend yield 0.01 corresponds to 1%
        :param sig: volatility 0.16 corresponds to 16%
        :param t: maturity in days
        :param b: annual basis 365 days per year
        :return: the d2 of the BS model
        """
        return (np.log(s / k) + (r - q - 0.5 * (sig ** 2)) * t / b) / (sig * np.sqrt(t / b))

    @staticmethod
    def n(d: float) -> float:
        """
        :param d: d1 or d2
        :return: CDF of the normal law.
        """
        return norm.cdf(d, 0, 1)

    @staticmethod
    def d_n(d: float) -> float:
        """
        :param d: d1 or d2
        :return: derivative of the CDF of the normal law
        """
        return norm.pdf(d, 0, 1)

    @staticmethod
    def pricing_put_bs(s: float, k: float, r: float, q: float, sig: float, t: int, b=365) -> float:
        """
        :param s: spot price
        :param k: stirke price
        :param r: risk free rate 0.05 corresponds to 5%
        :param q: dividend yield 0.01 corresponds to 1%
        :param sig: volatility 0.16 corresponds to 16%
        :param t: maturity in days
        :param b: annual basis 365 days per year
        :return: the price of a put with the BS model
        """
        d1 = VanillaOption.c_d1(s, k, r, q, sig, t, b)
        d2 = VanillaOption.c_d2(s, k, r, q, sig, t, b)
        n_md1 = VanillaOption.n(-d1)
        n_md2 = VanillaOption.n(-d2)
        return k * np.exp(-r * t / b) * n_md2 - s * n_md1 * np.exp(-q * t / b)

    @staticmethod
    def delta_call_bs(s: float, k: float, r: float, q: float, sig: float, t: int, b=365) -> float:
        """
        :param s: spot price
        :param k: stirke price
        :param r: risk free rate 0.05 corresponds to 5%
        :param q: dividend yield 0.01 corresponds to 1%
        :param sig: volatility 0.16 corresponds to 16%
        :param t: maturity in days
        :param b: annual basis 365 days per year
        :return: the delta of a call with the BS model
        """
        d1 = VanillaOption.c_d1(s, k, r, q, sig, t, b)
        n_d1 = VanillaOption.n(d1)
        return np.exp(-q * t / b) * n_d1

    @staticmethod
    def delta_put_bs(s: float, k: float, r: float, q: float, sig: float, t: int, b=365) -> float:
        """
        :param s: spot price
        :param k: stirke price
        :param r: risk free rate 0.05 corresponds to 5%
        :param q: dividend yield 0.01 corresponds to 1%
        :param sig: volatility 0.16 corresponds to 16%
        :param t: maturity in days
        :param b: annual basis 365 days per year
        :return: the delta of a put with the BS model
        """
        d1 = VanillaOption.c_d1(s, k, r, q, sig, t, b)
        n_d1 = VanillaOption.n(d1)
        return np.exp(-q * t / b) * (n_d1 - 1)

    @staticmethod
    def theta_call_bs(s: float, k: float, r: float, q: float, sig: float, t: int, b=365) -> float:
        """
        :param s: spot price
        :param k: stirke price
        :param r: risk free rate 0.05 corresponds to 5%
        :param q: dividend yield 0.01 corresponds to 1%
        :param sig: volatility 0.16 corresponds to 16%
        :param t: maturity in days
        :param b: annual basis 365 days per year
        :return: the theta of a call with the BS model
        """
        d1 = VanillaOption.c_d1(s, k, r, q, sig, t, b)
        d2 = VanillaOption.c_d2(s, k, r, q, sig, t, b)
        n_d1 = VanillaOption.n(d1)
        n_d2 = VanillaOption.n(d2)
        d_n_d1 = VanillaOption.d_n(d1)
        return (-np.exp(-q * t / b) * s * d_n_d1 * sig / (2 * np.sqrt(t / b)) + q * np.exp(-q * t / b) * s * n_d1
                - r * np.exp(-r * t / b) * k * n_d2) / b

    @staticmethod
    def theta_put_bs(s: float, k: float, r: float, q: float, sig: float, t: int, b=365) -> float:
        """
        :param s: spot price
        :param k: stirke price
        :param r: risk free rate 0.05 corresponds to 5%
        :param q: dividend yield 0.01 corresponds to 1%
        :param sig: volatility 0.16 corresponds to 16%
        :param t: maturity in days
        :param b: annual basis 365 days per year
        :return: the theta of a put with the BS model
        """
        d1 = VanillaOption.c_d1(s, k, r, q, sig, t, b)
        d2 = VanillaOption.c_d2(s, k, r, q, sig, t, b)
        n_md1 = VanillaOption.n(-d1)
        n_md2 = VanillaOption.n(-d2)
        d_n_d1 = VanillaOption.d_n(d1)
        return (-np.exp(-q * t / b) * s * d_n_d1 * sig / (2 * np.sqrt(t / b)) - q * np.exp(-q * t / b) * s * n_md1
                + r * np.exp(-r * t * b) * k * n_md2) / b

    @staticmethod
    def gamma_bs(s: float, k: float, r: float, q: float, sig: float, t: int, b=365) -> float:
        """
        :param s: spot price
        :param k: stirke price
        :param r: risk free rate 0.05 corresponds to 5%
        :param q: dividend yield 0.01 corresponds to 1%
        :param sig: volatility 0.16 corresponds to 16%
        :param t: maturity in days
        :param b: annual basis 365 days per year
        :return: the gamma with the BS model
        """
        d1 = VanillaOption.c_d1(s, k, r, q, sig, t, b)
        d_n_d1 = VanillaOption.d_n(d1)
        return (np.exp(-q * t / b) / (s * sig * np.sqrt(t / b))) * d_n_d1

    @staticmethod
    def vega_bs(s: float, k: float, r: float, q: float, sig: float, t: int, b=365) -> float:
        """
        :param s: spot price
        :param k: stirke price
        :param r: risk free rate 0.05 corresponds to 5%
        :param q: dividend yield 0.01 corresponds to 1%
        :param sig: volatility 0.16 corresponds to 16%
        :param t: maturity in days
        :param b: annual basis 365 days per year
        :return: the vega with the BS model
        """
        d1 = VanillaOption.c_d1(s, k, r, q, sig, t, b)
        d_n_d1 = VanillaOption.d_n(d1)
        return (np.exp(-q * t / b) * s * np.sqrt(t / b) * d_n_d1) / 100
