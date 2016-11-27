import random

def test():
    x = 3
    if random.randint(0,1):
        x = "x"
    else:
        x = 4.0
    return x

if __name__ == "__main__":
    print(test())
