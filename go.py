import os
import tinvest
from utils import get_usd_course
from datetime import datetime


TOKEN = os.getenv("T_TOKEN")
client = tinvest.SyncClient(TOKEN)
positions = client.get_portfolio().payload.positions

response_cur = client.get_portfolio_currencies().payload.currencies
rub_balance = response_cur[1].balance

operations = client.get_operations(from_="2020-01-01", to=datetime.now()).payload.operations


def get_currency_portfolio_sum():
    portfolio_sum = 0
    for position in positions:
        tmp_sum = position.balance * \
                  position.average_position_price.value + \
                  position.expected_yield.value
        if position.average_position_price.currency.name == "usd":
            tmp_sum *= get_usd_course()
        portfolio_sum += tmp_sum
    return int(portfolio_sum + rub_balance)


def get_margin_commision():
    sum = 0
    for operation in operations:
        if operation.operation_type.value == "MarginCommission":
            sum += operation.payment
    return str(sum)


def get_broker_commission():
    sum = 0
    for operation in operations:
        if operation.operation_type.value == "BrokerCommission":
            sum += operation.payment
    return str(sum)


def get_service_commission():
    sum = 0
    for operation in operations:
        if operation.operation_type.value == "ServiceCommission":
            sum += operation.payment
    return str(sum)


def get_sberbank_sum():
    sum = 0
    for operation in operations:
        if operation.figi == "BBG004730N88":
            sum += operation.payment
    for elem in positions:
        if elem.ticker == 'SBER':
            return f'{sum + ((elem.average_position_price.value * elem.balance + elem.expected_yield.value))} rub'


def total_sum():
    all_input = 0
    for operation in operations:
        if operation.operation_type.value == "PayIn":
            if operation.currency.value == "USD":
                all_input += operation.payment * int(get_usd_course())
            all_input += operation.payment
    return f'{get_currency_portfolio_sum() - all_input} rub'


def final_information():
    info = {"balance": total_sum(),
            "sber_balance": get_sberbank_sum(),
            "margin_balance": get_margin_commision(),
            "commission": get_broker_commission(),
            "service": get_service_commission()}
    for elem in info:
        print(f'{elem} {info.get(elem)}')


if __name__ == "__main__":
    final_information()
