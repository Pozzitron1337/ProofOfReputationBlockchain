
class MockReputationModel: 


    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        pass

    def reputation(self, ioc: int): 
        '''
        ioc - is indicator of comprometation
        R: X1*X2*...*Xn -> [0,1]
        In this implementation R: Z -> N
        In words, this implementation get on input any integer and return positive value
        '''
        return ioc
