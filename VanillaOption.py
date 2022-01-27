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
                 strike: float,
                 rate: float,
                 dividend: float,
                 maturity: int,
                 typ: str = 'C',
                 volatility: float = 0,
                 pricing_method: str = 'BS'):
        """

        :param spot: spot price
        :param strike: stirke price
        :param rate: risk free rate 0.05 corresponds to 5%
        :param dividend: dividend yield 0.01 corresponds to 1%
        :param maturity: maturity in days
        :param typ: 'C': Call / 'P': Put
        :param volatility: volatility 0.16 corresponds to 16%
        :param pricing_method: 'BS': Black&Scholes
        """
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
                return self.pricing_call_bs()

            if self.__typ == 'P':
                return self.pricing_put_bs()

    @property
    def Delta(self) -> float:
        if self.__pricing_method == "BS":
            if self.__typ == 'C':
                return self.delta_call_bs()
            if self.__typ == 'P':
                return self.delta_put_bs()

    @property
    def Theta(self) -> float:
        if self.__pricing_method == "BS":
            if self.__typ == 'C':
                return self.theta_call_bs()
            if self.__typ == 'P':
                return self.theta_put_bs()
    @property
    def Gamma(self) -> float:
        if self.__pricing_method == "BS":
            return self.gamma_bs()

    @property
    def Vega(self) -> float:
        if self.__pricing_method == "BS":
            return self.vega_bs()

    ############################################### BLACK & SCHOLES ####################################################
    @property
    def d1(self) -> float:
        """
        :return: the d1 of the BS model
        """
        s = self.__spot
        k = self.__strike
        r = self.__rate
        q = self.__dividend
        sig = self.__volatility
        t = self.__maturity
        b = self.__annual_basis
        return (np.log(s / k) + (r - q + 0.5 * (sig ** 2)) * t / b) / (sig * np.sqrt(t / b))

    @property
    def d2(self) -> float:
        """
        :return: the d2 of the BS model
        """
        s = self.__spot
        k = self.__strike
        r = self.__rate
        q = self.__dividend
        sig = self.__volatility
        t = self.__maturity
        b = self.__annual_basis
        return (np.log(s / k) + (r - q - 0.5 * (sig ** 2)) * t / b) / (sig * np.sqrt(t / b))

    @property
    def n_d1(self,) -> float:
        return norm.cdf(self.d1, 0, 1)

    @property
    def n_d2(self) -> float:
        return norm.cdf(self.d2, 0, 1)

    @property
    def d_n_d1(self) -> float:
        return norm.pdf(self.d1, 0, 1)

    @property
    def d_n_d2(self) -> float:
        return norm.pdf(self.d2, 0, 1)

    def pricing_call_bs(self) -> float:
        """
        :return: the price of a call with the BS model
        """
        s = self.__spot
        k = self.__strike
        r = self.__rate
        q = self.__dividend
        t = self.__maturity
        b = self.__annual_basis
        n_d1 = self.n_d1
        n_d2 = self.n_d2
        return s * n_d1 * np.exp(-q * t / b) - k * np.exp(-r * t / b) * n_d2

    def pricing_put_bs(self) -> float:
        """
        :return: the price of a put with the BS model
        """
        s = self.__spot
        k = self.__strike
        r = self.__rate
        q = self.__dividend
        t = self.__maturity
        b = self.__annual_basis
        n_md1 = 1 - self.n_d1
        n_md2 = 1 - self.n_d2
        return k * n_md2 * np.exp(-r * t / b)  - s * n_md1 * np.exp(-q * t / b)

    def delta_call_bs(self) -> float:
        """
        :return: the delta of a call with the BS model
        """
        q = self.__dividend
        t = self.__maturity
        b = self.__annual_basis
        n_d1 = self.n_d1
        return np.exp(-q * t / b) * n_d1

    def delta_put_bs(self) -> float:
        """
        :return: the delta of a put with the BS model
        """
        q = self.__dividend
        t = self.__maturity
        b = self.__annual_basis
        n_d1 = self.n_d1
        return np.exp(-q * t / b) * (n_d1 - 1)

    def theta_call_bs(self) -> float:
        """
        :return: the theta of a call with the BS model
        """
        s = self.__spot
        k = self.__strike
        r = self.__rate
        q = self.__dividend
        sig = self.__volatility
        t = self.__maturity
        b = self.__annual_basis
        n_d1 = self.n_d1
        n_d2 = self.n_d2
        d_n_d1 = self.d_n_d1
        return (-np.exp(-q * t / b) * s * d_n_d1 * sig / (2 * np.sqrt(t / b)) + q * np.exp(-q * t / b) * s * n_d1
                - r * np.exp(-r * t / b) * k * n_d2) / b

    def theta_put_bs(self) -> float:
        """
        :return: the theta of a put with the BS model
        """
        s = self.__spot
        k = self.__strike
        r = self.__rate
        q = self.__dividend
        sig = self.__volatility
        t = self.__maturity
        b = self.__annual_basis
        n_md1 = 1 - self.n_d1
        n_md2 = 1 - self.n_d1
        d_n_d1 = self.d_n_d1
        return (-np.exp(-q * t / b) * s * d_n_d1 * sig / (2 * np.sqrt(t / b)) - q * np.exp(-q * t / b) * s * n_md1
                + r * np.exp(-r * t * b) * k * n_md2) / b

    def gamma_bs(self) -> float:
        """
        :return: the gamma with the BS model
        """
        s = self.__spot
        q = self.__dividend
        sig = self.__volatility
        t = self.__maturity
        b = self.__annual_basis
        d_n_d1 = self.d_n_d1
        return (np.exp(-q * t / b) / (s * sig * np.sqrt(t / b))) * d_n_d1

    def vega_bs(self) -> float:
        """
        :return: the vega with the BS model
        """
        s = self.__spot
        q = self.__dividend
        t = self.__maturity
        b = self.__annual_basis
        d_n_d1 = self.d_n_d1
        return (np.exp(-q * t / b) * s * np.sqrt(t / b) * d_n_d1) / 100

