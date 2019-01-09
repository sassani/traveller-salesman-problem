def check_prime(givenNumber):  
    for num in range(2, int(givenNumber ** 0.5) + 1):
        if givenNumber % num == 0:
            return False
    return True