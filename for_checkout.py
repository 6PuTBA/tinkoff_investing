from go import operations, positions


def get_full_portfolio_csv():
    csv_rows = [",".join(["name", "average_position_price", "currency", "balance", "expected_yield", "ticker"])]
    for position in positions:
        csv_rows.append(",".join([position.name,
                                  str(position.average_position_price.value),
                                  position.average_position_price.currency,
                                  str(position.balance),
                                  str(position.expected_yield.value),
                                  position.ticker]))
    with open("positions.csv", "w") as f:
        f.write("\n".join(csv_rows))


def get_full_operations_csv():
    csv_rows = [",".join(["Date", "Currency", "Figi", "Operation_Type", "Payment", "Price", "Quantity"])]
    for operation in operations:
        csv_rows.append(
            ",".join(map(str, [operation.date, operation.currency.value, operation.figi, operation.operation_type.value,
                               operation.payment, operation.price or "", operation.quantity or ""])))
    with open("operations.csv", "w") as f:
        f.write("\n".join(csv_rows))
