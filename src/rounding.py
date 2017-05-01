from decimal import Decimal, ROUND_HALF_UP

class Rounding(object):
    """take care of rounding methods """

    def dollar_rounding(self,amount,decimal=1,rounding_mode=ROUND_HALF_UP):
        return Decimal(amount).quantize(Decimal(decimal), rounding=rounding_mode)
