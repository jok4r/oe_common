import oe_common


def main():
    logger = oe_common.Logger(to_console=True, file='zora.txt')
    logger.log('first', 'second')


if __name__ == '__main__':
    main()
