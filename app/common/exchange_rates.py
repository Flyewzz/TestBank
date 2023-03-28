from decimal import Decimal

# LOVE, my princess <3333333

currencies = {
  "RUB": "₽",  # Russian ruble
  "USD": "$",  # American dollar
  "EUR": "€",  # European euro
  "PLN": "zł"  # Polish zloty
}

exchange_rates = {
  'RUB': {
    'USD': Decimal('0.014'),
    'EUR': Decimal('0.012'),
    'PLN': Decimal('0.058'),
    'RUB': Decimal('1.0')
  },
  'USD': {
    'RUB': Decimal('70.50'),
    'EUR': Decimal('0.85'),
    'PLN': Decimal('3.93'),
    'USD': Decimal('1.0')
  },
  'EUR': {
    'RUB': Decimal('82.17'),
    'USD': Decimal('1.18'),
    'PLN': Decimal('4.63'),
    'EUR': Decimal('1.0')
  },
  'PLN': {
    'RUB': Decimal('17.18'),
    'USD': Decimal('0.25'),
    'EUR': Decimal('0.22'),
    'PLN': Decimal('1.0')
  }
}


def get_exchange_rate(base_currency, target_currency):
  return exchange_rates[base_currency][target_currency]
