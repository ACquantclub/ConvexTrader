def optimize(holdings, trade):
    value = sum(holdings)
    weight = [holding / value for holding in holdings]
