from miner.controller import AnalysisController

REPO_PATH = "<REPO_PATH>"
TEST_DIRECTORIES = ["tests/", "spec/", "/test", "/cypress"]

def main():
    controller = AnalysisController(REPO_PATH, TEST_DIRECTORIES)
    controller.start()

if __name__ == "__main__":
    main()