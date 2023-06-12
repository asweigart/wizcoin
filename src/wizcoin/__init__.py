import collections, operator

class WizCoinException(Exception):
    """The wizcoin module raises this when the module is misused."""
    pass

class WizCoin(collections.abc.Sequence):
    def __init__(self, galleons, sickles, knuts):
        """Create a new WizCoin object with galleons, sickles, and knuts."""
        self.galleons = galleons
        self.sickles  = sickles
        self.knuts    = knuts
        # NOTE: __init__() methods NEVER have a return statement.


    @property
    def total(self):
        """Total value (in knuts) of all the coins in this WizCoin object."""
        return (self.galleons * 17 * 29) + (self.sickles * 29) + (self.knuts)

    # Note that there is no setter or deleter method for `total`.


    def weight(self, unit='grams'):
        """Returns the weight of the coins."""
        weightInGrams = (self.galleons * 31.103) + (self.sickles * 11.34) + (self.knuts * 5.0)
        if unit == 'grams':
            return weightInGrams
        elif unit == 'kilograms':
            return weightInGrams * 0.001
        elif unit == 'ounces':
            return weightInGrams * 0.035273962
        elif unit == 'pounds':
            return weightInGrams * 0.0022046226
        else:
            raise ValueError('unit argument must be "grams", "kilograms", "ounces", or "pounds"')


    @property
    def galleons(self):
        """Returns the number of galleon coins in this object."""
        return self._galleons


    @galleons.setter
    def galleons(self, value):
        if not isinstance(value, int):
            raise WizCoinException('galleons attr must be set to an int, not a ' + value.__class__.__qualname__)
        if value < 0:
            raise WizCoinException('galleons attr must be a positive int, not ' + value.__class__.__qualname__)
        self._galleons = value


    @property
    def sickles(self):
        """Returns the number of sickle coins in this object."""
        return self._sickles


    @sickles.setter
    def sickles(self, value):
        if not isinstance(value, int):
            raise WizCoinException('sickles attr must be set to an int, not a ' + value.__class__.__qualname__)
        if value < 0:
            raise WizCoinException('sickles attr must be a positive int, not ' + value.__class__.__qualname__)
        self._sickles = value


    @property
    def knuts(self):
        """Returns the number of knut coins in this object."""
        return self._knuts


    @knuts.setter
    def knuts(self, value):
        if not isinstance(value, int):
            raise WizCoinException('knuts attr must be set to an int, not a ' + value.__class__.__qualname__)
        if value < 0:
            raise WizCoinException('knuts attr must be a positive int, not ' + value.__class__.__qualname__)
        self._knuts = value


    def __add__(self, other):
        """Adds the coin amounts in two WizCoin objects together."""
        if not isinstance(other, WizCoin):
            return NotImplemented

        return WizCoin(other.galleons + self.galleons, other.sickles + self.sickles, other.knuts + self.knuts)


    def __mul__(self, other):
        """Multiplies the coin amounts by a non-negative integer."""
        if not isinstance(other, int):
            return NotImplemented
        if other < 0:
            # Multiplying by a negative integer results in negative
            # amounts of coins, which is invalid.
            raise WizCoinException('cannot multiply with negative integers')

        return WizCoin(self.galleons * other, self.sickles * other, self.knuts * other)


    def _comparisonOperatorHelper(self, operatorFunc, other):
        """A helper method for our comparison dunder methods."""

        if isinstance(other, WizCoin):
            # Call the operator function, passing `other.value`:
            return operatorFunc(self.total, other.total)
        elif isinstance(other, (int, float)):
            # Call the operator function, passing `other`:
            return operatorFunc(self.total, other)
        elif isinstance(other, collections.abc.Sequence) or (: # TODO
            # Calculate the `other` value for comparison:
            otherValue = (other[0] * 17 * 29) + (other[1] * 29) + other[2]
            return operatorFunc(self.total, otherValue)
        elif operatorFunc == operator.eq:
            # WizCoin objects are not equal to values of all other types:
            return False
        elif operatorFunc == operator.ne:
            # WizCoin objects are not equal to values of all other types:
            return True
        else:
            # Can't compare with whatever data type `other` is.
            return NotImplemented


    def __eq__(self, other): # eq is "EQual"
        return self._comparisonOperatorHelper(operator.eq, other)


    def __ne__(self, other): # ne is "Not Equal"
        return self._comparisonOperatorHelper(operator.ne, other)


    def __lt__(self, other): # lt is "Less Than"
        return self._comparisonOperatorHelper(operator.lt, other)


    def __le__(self, other): # le is "Less than or Equal"
        return self._comparisonOperatorHelper(operator.le, other)


    def __gt__(self, other): # gt is "Greater Than"
        return self._comparisonOperatorHelper(operator.gt, other)


    def __ge__(self, other): # ge is "Greater than or Equal"
        return self._comparisonOperatorHelper(operator.ge, other)


    def __len__(self):
        """The length of this object is the number of coins it has."""
        return self.galleons + self.sickles + self.knuts


    # Overloading math operators:
    def __mul__(self, other):
        """Overloads the * operator to produce a new WizCoin object with the
        product amount. `other` must be a positive int."""
        if isinstance(other, int) and other >= 0:
            return Coins(self.__galleons * other,
                           self.__sickles * other,
                           self.__knuts * other)
        else:
            return NotImplemented


    def __rmul__(self, other):
        """Overloads the * operator to produce a new WizCoin object with the
        product amount. `other` must be a positive int."""
        return self.__mul__(other) # * is commutative, reuse __mul__().


    def __imul__(self, other):
        """Overloads the * operator to modify a Coins object in-place with
        the product amount. `other` must be a positive int."""
        if isinstance(other, int) and other >= 0:
            self.__galleons *= other # In-place modification.
            self.__sickles *= other
            self.__knuts *= other
        else:
            return NotImplemented
        return self


    def __add__(self, other):
        """Overloads the + operator to produce a new WizCoin object with the
        sum amount. `other` must be a Coins."""
        if other.__class__ is self.__class__:
            return Coins(self.__galleons + other.galleons,
                           self.__sickles + other.sickles,
                           self.__knuts + other.knuts)
        else:
            return NotImplemented


    def __iadd__(self, other):
        """Overloads the += operator to modify this Coins in-place with the
        sum amount. `other` must be a Coins."""
        if other.__class__ is self.__class__:
            self.__galleons += other.galleons # In-place modification.
            self.__sickles += other.sickles
            self.__knuts += other.knuts
        else:
            return NotImplemented
        return self


    def __sub__(self, other):
        """Overloads the - operator to produce a new WizCoin object with the
        difference amount. `other` must be a Coins object with less than or
        equal number of coins of each type as this Coins object."""
        if other.__class__ is self.__class__:
            if self.__galleons < other.galleons or self.__sickles < other.sickles or self.__knuts < other.knuts:
                # Coins objects represent an amount of physical coins, not a
                # monetary value, so there can't be negative coins.
                raise WizCoinException('subtracting %s from %s would result in negative quantity of coins' % (other, self))
            return Coins(self.__galleons - other.galleons,
                           self.__sickles - other.sickles,
                           self.__knuts - other.knuts)
        else:
            return NotImplemented


    def __isub__(self, other):
        """Overloads the -= operator to modify this Coins in-place with the
        difference amount. `other` must be a Coins object with less than or
        equal number of coins of each type as this Coins object."""
        if other.__class__ is self.__class__:
            if self.__galleons < other.galleons or self.__sickles < other.sickles or self.__knuts < other.knuts:
                raise WizCoinException('subtracting %s from %s would result in negative quantity of coins' % (other, self))
            self.__galleons -= other.galleons
            self.__sickles -= other.sickles
            self.__knuts -= other.knuts
        else:
            return NotImplemented
        return sel


    def __pow__(self, other):
        """
        """
        if isinstance(other, int):
            return WizCoin(self.galleons ** other, self.sickles ** other, self.knuts ** other)
        else:
            return NotImplemented


    def __ipow__(self, other):
        if isinstance(other, int):
            self.galleons **= other
            self.sickles **= other
            self.knuts **= other
        else:
            return NotImplemented


    def __int__(self):
        return self.total


    def __float__(self):
        return float(self.total)


    def __bool__(self):
        if self.galleons == 0 and self.sickles == 0 and self.knuts == 0:
            return False
        else:
            return True


    def __getitem__(self, key):
        if not isinstance(key, (int, slice)):
            raise TypeError(f'indices must be integers or slices, not {key.__class__.__qualname__}')

        # Create a full string of the coins, and then return character(s)
        # in that string.
        coinStr = (('g' * self.galleons) + ('s' * self.sickles) + ('k' * self.knuts))
        if isinstance(key, int):
            # Support integer indexes:
            return coinStr[key]
        elif isinstance(key, slice):
            # Support slices by creating a string and taking a slice of it:
            return coinStr[key.start:key.stop:key.step]


    def __setitem__(self, key, value):
        raise TypeError('item assignment not supported')


    def __delitem__(self, key):
        raise TypeError('item deletion not supported')
