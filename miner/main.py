from miner.controller import AnalysisController

REPO_PATH = "<PATH TO REPO>"
TEST_DIRECTORIES = ["tests/", "spec/", "test/", "cypress/"]

def main():
    controller = AnalysisController(REPO_PATH, TEST_DIRECTORIES)
    controller.start()

if __name__ == "__main__":
    main()