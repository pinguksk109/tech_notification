from lambda_function import lambda_handler


def main():
    """
    ローカルでLambdaを動かすための関数
    """
    event = {}
    context = {}

    print(lambda_handler(event, context))


if __name__ == "__main__":
    main()
