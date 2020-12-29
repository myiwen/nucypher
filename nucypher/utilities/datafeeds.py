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
from difflib import get_close_matches
from typing import Optional

import requests
from datetime import datetime, timezone, timedelta
from constant_sorrow.constants import SLOW, MEDIUM, FAST, FASTEST
from web3 import Web3
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

    _speed_equivalence_classes = {
        SLOW: ('slow', 'safeLow', 'low'),
        MEDIUM: ('medium', 'standard', 'average'),
        FAST: ('fast', 'high'),
        FASTEST: ('fastest', 'rapid', ),
        'cheapfast': ('cheapfast', ),
    }

    @abstractmethod
    def _parse_gas_prices(self):
        return NotImplementedError

    def get_gas_price(self, speed: Optional[str] = None) -> Wei:
        speed = speed or self._default_speed
        self._parse_gas_prices()
        gas_price_wei = Wei(self.gas_prices[self.get_canonical_speed(speed)])
        return gas_price_wei

    @classmethod
    def construct_gas_strategy(cls, speed: Optional[str] = None):
        def gas_price_strategy(web3: Web3, transaction_params: TxParams = None) -> Wei:
            feed = cls()
            gas_price = feed.get_gas_price(speed=speed)
            return gas_price
        return gas_price_strategy

    @classmethod
    def get_canonical_speed(cls, speed: str):
        for canonical_speed, speed_names in cls._speed_equivalence_classes.items():
            if speed.lower() in map(str.lower, speed_names):
                return canonical_speed
        else:
            all_speed_names = [name for names in cls._speed_equivalence_classes.values() for name in names]
            suggestion = get_close_matches(speed, all_speed_names, n=1)
            if not suggestion:
                message = f"'{speed}' is not a valid speed name."
            else:
                suggestion = suggestion.pop()
                message = f"'{speed}' is not a valid speed name. Did you mean '{suggestion}'?"
            raise LookupError(message)


def get_cheap_fast_price(fast, standard):
    print('fast,', fast/10**9, 'standard,', standard/10**9, datetime.now(tz=timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S'))
    fast += 10**8  # wei
    standard += 10**8  # wei
    if fast <= 30 * 10**9:  # Gwei
        return fast
    delta = fast - standard
    if delta < 8 * 10**9:
        return fast
    else:
        return fast - (int(delta/3/10**8)*10**8)


class CheapfastGasPriceDatafeed(EthereumGasPriceDatafeed):
    """Try to get a cheap and fast gas price"""

    name = "Cheap datafeed"
    api_url = "https://gasnow.sparkpool.com/api/v3/gas/price"
    _speed_names = {
        SLOW: 'slow',
        MEDIUM: 'standard',
        FAST: 'fast',
        FASTEST: 'rapid',
    }
    _default_speed = 'cheapfast'
    fair_price = None

    def get_gas_prices(self):
        self._probe_feed()
        print('get gasnow price')
        self.gas_prices = {self.get_canonical_speed(k): int(Web3.toWei(int(v / 10 ** 9), 'gwei')) for k, v in self._raw_data['data'].items() if k in self._speed_names}
        self.gas_prices['cheapfast'] = get_cheap_fast_price(self.gas_prices[FAST], self.gas_prices[MEDIUM])
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
    _speed_names = {
        SLOW: 'safeLow',
        MEDIUM: 'standard',
        FAST: 'fast',
        FASTEST: 'fastest',
    }
    _default_speed = 'cheapfast'
    fair_price = None

    def get_gas_prices(self):
        self._probe_feed()
        print('get etherchain price')
        self.gas_prices = {self.get_canonical_speed(k): int(Web3.toWei(v, 'gwei')) for k, v in self._raw_data.items()}
        self.gas_prices['cheapfast'] = get_cheap_fast_price(self.gas_prices[FAST], self.gas_prices[MEDIUM])
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
    _speed_names = {
        SLOW: 'safeLow',
        MEDIUM: 'standard',
        FAST: 'fast',
        FASTEST: 'fastest'
    }
    _default_speed = 'fast'

    def _parse_gas_prices(self):
        self._probe_feed()
        self.gas_prices = {self.get_canonical_speed(k): int(Web3.toWei(v, 'gwei')) for k, v in self._raw_data.items()}


class UpvestGasPriceDatafeed(EthereumGasPriceDatafeed):
    """Gas price datafeed from Upvest"""

    name = "Upvest datafeed"
    api_url = "https://fees.upvest.co/estimate_eth_fees"
    _speed_names = {
        SLOW: 'slow',
        MEDIUM: 'medium',
        FAST: 'fast',
        FASTEST: 'fastest'
    }
    _default_speed = 'fastest'

    def _parse_gas_prices(self):
        self._probe_feed()
        self.gas_prices = {self.get_canonical_speed(k): int(Web3.toWei(v, 'gwei'))
                           for k, v in self._raw_data['estimates'].items()}


class ZoltuGasPriceDatafeed(EthereumGasPriceDatafeed):
    """Gas price datafeed from gas-oracle.zoltu.io"""

    name = "gas-oracle.zoltu.io datafeed"
    api_url = "https://gas-oracle.zoltu.io"
    _speed_names = {
        SLOW: 'percentile_40',
        MEDIUM: 'percentile_75',
        FAST: 'percentile_95',
        FASTEST: 'percentile_98'
    }
    _default_speed = 'fast'

    def _parse_gas_prices(self):
        self._probe_feed()
        self.gas_prices = dict()
        for canonical_speed_name, zoltu_speed in self._speed_names.items():
            gwei_price = self._raw_data[zoltu_speed].split(" ")[0]
            wei_price = int(Web3.toWei(gwei_price, 'gwei'))
            self.gas_prices[canonical_speed_name] = wei_price
