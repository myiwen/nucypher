"""
 This file is part of nucypher.

 nucypher is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 nucypher is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with nucypher.  If not, see <https://www.gnu.org/licenses/>.
"""
from abc import ABC, abstractmethod
from typing import Optional

import requests
from web3 import Web3
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from web3.types import Wei, TxParams


class Datafeed(ABC):

    class DatafeedError(RuntimeError):
        """Base class for exceptions concerning Datafeeds"""

    name = NotImplemented
    api_url = NotImplemented  # TODO: Deal with API keys

    def _probe_feed(self):
        try:
            response = requests.get(self.api_url)
        except requests.exceptions.ConnectionError as e:
            error = f"Failed to probe feed at {self.api_url}: {str(e)}"
            raise self.DatafeedError(error)

        if response.status_code != 200:
            error = f"Failed to probe feed at {self.api_url} with status code {response.status_code}"
            raise self.DatafeedError(error)

        self._raw_data = response.json()

    def __repr__(self):
        return f"{self.name} ({self.api_url})"


class EthereumGasPriceDatafeed(Datafeed):
    """Base class for Ethereum gas price data feeds"""

    _speed_names = NotImplemented
    _default_speed = NotImplemented

    @abstractmethod
    def _parse_gas_prices(self):
        return NotImplementedError

    def get_gas_price(self, speed: Optional[str] = None) -> Wei:
        speed = speed or self._default_speed
        self._parse_gas_prices()
        gas_price_wei = Wei(self.gas_prices[speed])
        return gas_price_wei

    @classmethod
    def construct_gas_strategy(cls):
        def gas_price_strategy(web3: Web3, transaction_params: TxParams = None) -> Wei:
            feed = cls()
            gas_price = feed.get_gas_price()
            return gas_price
        return gas_price_strategy


def get_cheap_fast_price(fast, standard):
    print('fast,', fast/10**9, 'standard,', standard/10**9)
    fast += 10**8  # wei
    standard += 10**8  # wei
    if fast <= 23 * 10**9:  # 23 Gwei
        return fast
    delta = fast - standard
    if delta < 8 * 10**9:
        return fast
    else:
        return fast - delta / 3


class CheapfastGasPriceDatafeed(EthereumGasPriceDatafeed):
    """Try to get a cheap and fast gas price"""

    name = "Cheap datafeed"
    api_url = "https://gasnow.sparkpool.com/api/v3/gas/price"
    _speed_names = ('slow', 'standard', 'fast', 'rapid')
    _default_speed = 'cheapfast'
    fair_price = None

    def get_gas_prices(self):
        self._probe_feed()
        print('get gasnow price')
        self.gas_prices = {k: int(Web3.toWei(int(v / 10 ** 9), 'gwei')) for k, v in self._raw_data['data'].items() if k in self._speed_names}
        self.gas_prices['cheapfast'] = get_cheap_fast_price(self.gas_prices['fast'], self.gas_prices['standard'])
        self.fair_price = self.gas_prices['cheapfast'] if self.fair_price is None else min(self.fair_price, self.gas_prices['cheapfast'])

    def _parse_gas_prices(self):
        import time
        c = 3
        while 1:
            self.get_gas_prices()
            c -= 1
            if c <= 0:
                self.gas_prices['cheapfast'] = self.fair_price
                break
            time.sleep(16)


class CheapfastGasPriceDatafeed2(EthereumGasPriceDatafeed):
    """Try to get a cheap and fast gas price"""

    name = "Cheap datafeed2"
    api_url = "https://www.etherchain.org/api/gasPriceOracle"
    _speed_names = ('safeLow', 'standard', 'fast', 'fastest')
    _default_speed = 'cheapfast'
    fair_price = None

    def get_gas_prices(self):
        self._probe_feed()
        print('get etherchain price')
        self.gas_prices = {k: int(Web3.toWei(v, 'gwei')) for k, v in self._raw_data.items()}
        self.gas_prices['cheapfast'] = get_cheap_fast_price(self.gas_prices['fast'], self.gas_prices['standard'])
        self.fair_price = self.gas_prices['cheapfast'] if self.fair_price is None else min(self.fair_price, self.gas_prices['cheapfast'])

    def _parse_gas_prices(self):
        import time
        c = 3
        while 1:
            self.get_gas_prices()
            c -= 1
            if c <= 0:
                self.gas_prices['cheapfast'] = self.fair_price
                break
            time.sleep(16)


class EtherchainGasPriceDatafeed(EthereumGasPriceDatafeed):
    """Gas price datafeed from Etherchain"""

    name = "Etherchain datafeed"
    api_url = "https://www.etherchain.org/api/gasPriceOracle"
    _speed_names = ('safeLow', 'standard', 'fast', 'fastest')
    _default_speed = 'fast'

    def _parse_gas_prices(self):
        self._probe_feed()
        self.gas_prices = {k: int(Web3.toWei(v, 'gwei')) for k, v in self._raw_data.items()}


class UpvestGasPriceDatafeed(EthereumGasPriceDatafeed):
    """Gas price datafeed from Upvest"""

    name = "Upvest datafeed"
    api_url = "https://fees.upvest.co/estimate_eth_fees"
    _speed_names = ('slow', 'medium', 'fast', 'fastest')
    _default_speed = 'fastest'

    def _parse_gas_prices(self):
        self._probe_feed()
        self.gas_prices = {k: int(Web3.toWei(v, 'gwei')) for k, v in self._raw_data['estimates'].items()}


# TODO: We can implement here other datafeeds, like the ETH/USD (e.g., https://api.coinmarketcap.com/v1/ticker/ethereum/)
# suggested in a comment in nucypher.blockchain.eth.interfaces.BlockchainInterface#sign_and_broadcast_transaction
