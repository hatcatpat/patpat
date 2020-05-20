import sys
import time
import global_variables


def main():
    global_variables.init()

    try:
        global_variables.osc.serve_server()

        while True:
            time.sleep(1000)
    except (KeyboardInterrupt, SystemExit):
        print("leaving")
        global_variables.quit = True


if __name__ == "__main__":
    main()
