import os

print(os.environ['PATH'].split(':'))

dirs = os.environ['PATH'].split(':')
try: