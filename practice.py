def is_prime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def test_is_prime():
    n = 5
    assert is_prime(n) == True
    n = 4
    assert is_prime(n) == False

test_is_prime()