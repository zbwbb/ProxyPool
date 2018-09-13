from proxypool.scheduler import Scheduler


def main():
    try:
        s = Scheduler()
        s.run()
    except Exception as e:
        print(e)
        main()


if __name__ == '__main__':
    main()