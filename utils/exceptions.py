#here we will customize our error exception by defininf class and overriding it whereever we want

class InvalidDataError(Exception):

    pass

class InvalidAmountError(Exception):

     pass

class InvalidCategoryError(Exception):
     pass

class CategoryNotFoundError(Exception):
     pass

class InvalidTransactionTypeError(Exception):
     pass

class TransactionNotFoundError(Exception):
      pass

