import requests


def main():
    instruction = input()
    while instruction != "exit":
        print(instruction)

        instruction = input()
    print("exited from CLI")


if __name__ == '__main__':
    main()
