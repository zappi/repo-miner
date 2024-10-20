from miner.analyzers.commit_analyzer import analyze_commits
from miner.analyzers.test_debt_analyzer import analyze_testing_debt
from miner.user_inputs import get_commit_limit, choose_analyzer
from miner.display_results import display_commit_results, display_testing_debt_results
from pydriller import Repository

class AnalysisController:
    def __init__(self, repo_path, test_directories):
        self.repo_path = repo_path
        self.test_directories = test_directories

    @staticmethod
    def contains_fix_keyword(commit):
        return "fix" in commit.msg.lower()

    def traverse_commits(self, process_commit, filters=None, order="reverse"):
        commit_count = 0

        limit = get_commit_limit()

        for commit in Repository(self.repo_path, order=order).traverse_commits():
            if filters:
                if not all(f(commit) for f in filters):
                    continue

            if limit and commit_count >= limit:
                break

            process_commit(commit)
            commit_count += 1

    def run_commit_analyzer(self):
        commit_data = {
            "fix_commit_count": 0,
            "single_spec_file_commits": 0,
            "multiple_spec_file_commits": 0
        }

        def process_commit(commit):
            analyze_commits(commit, commit_data)

        self.traverse_commits(process_commit, filters=[self.contains_fix_keyword])
        display_commit_results(commit_data)

    def run_test_debt_analyzer(self):
        debt_data = {
            "commits_with_tests": 0,
            "commits_without_tests": 0,
            "total_feature_additions": 0,
            "total_test_additions": 0,
            "debt_commits": []
        }

        def process_commit(commit):
            analyze_testing_debt(commit, debt_data, self.test_directories)

        self.traverse_commits(process_commit)

        display_testing_debt_results(debt_data)

    def start(self):
        while True:
            analyzer = choose_analyzer()

            if analyzer == 1:
                self.run_commit_analyzer()
            elif analyzer == 2:
                self.run_test_debt_analyzer()

            run_again = input("\nWould you like to run the analysis again? (y/n): ").strip().lower()
            if run_again != "y":
                print("Exiting...")
                break