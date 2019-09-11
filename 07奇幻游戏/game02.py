def solve_something():
    b = 0
    a = int(input("Enter a number'a':"))
    assert a > 0
    print("a = {}, b = {}, Now doing a/b".format(a, b))
    a += a / b
    d = x + a
    e = 2 * d


def some_function():
    try:
        solve_something()
    except NameError as e:
        print("Uh oh..Name Error.", e.args)
    except AssertionError:
        print("Assertion Error")
    except Exception as e:
        print("Logging the error:", e)
        raise


if __name__ == '__main__':
    some_function()