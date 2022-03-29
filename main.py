import argparse
import os

from Scanner import Scanner

if __name__ == "__main__":
    scanner = Scanner()

    parser = argparse.ArgumentParser()
    parser.add_argument("--scan", "-s", type=str)
    args = parser.parse_args()
    path_to_scanned_file = args.scan
    if not os.path.exists(path_to_scanned_file):
        print(f"The {path_to_scanned_file} file does not exist!")
    else:
        scanner.scan_file(path_to_scanned_file)
        scanner.printTokens()
