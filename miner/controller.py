from miner.analyzers.churn_analyzer import analyze_code_churn
from miner.analyzers.commit_analyzer import analyze_commits
from miner.analyzers.file_path_analyzer import analyze_file_path
from miner.analyzers.test_debt_analyzer import analyze_testing_debt
from miner.user_inputs import get_commit_limit, choose_analyzer, get_date, get_filepath
from miner.display_results import display_commit_results, display_testing_debt_results, report_code_churn
from pydriller import Repository

class AnalysisController:
    def __init__(self, repo_path, test_directories):
        self.repo_path = repo_path
        self.test_directories = test_directories
        self.commit_count = 0

    @staticmethod
    def contains_fix_keyword(commit):
        return "fix" in commit.msg.lower()

    def traverse_commits(self, process_commit, filters=None, order="reverse", filepath=None):
        limit = get_commit_limit()
        # since_date = get_date("starting")
        # to_date = get_date("ending")

        for commit in Repository(self.repo_path, order=order, since=None, to=None, filepath=filepath).traverse_commits():
            if filters:
                if not all(f(commit) for f in filters):
                    continue

            if limit and self.commit_count >= limit:
                break

            process_commit(commit)
            self.commit_count += 1

    def run_commit_analyzer(self):
        commit_data = {
            "single_test_file_commits": 0,
            "multiple_test_file_commits": 0
        }

        def process_commit(commit):
            analyze_commits(commit, commit_data, self.test_directories)

        self.traverse_commits(process_commit, filters=[self.contains_fix_keyword])
        commit_data["fix_commit_count"] = self.commit_count

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

    def run_code_churn_analyzer(self):
        churn_data = {
            "total_commits": 0,
            "total_lines_added": 0,
            "total_lines_deleted": 0,
            "total_files_changed": set(),
            "file_churn": {}
        }

        developer_contribution = {}

        def process_commit(commit):
            analyze_code_churn(commit, churn_data, developer_contribution)

        self.traverse_commits(process_commit)

        report_code_churn(churn_data, developer_contribution)

    def run_code_file_path_analyzer(self):
        filepath = get_filepath()

        def process_commit(commit):
            analyze_file_path(commit, filepath)

        self.traverse_commits(process_commit, order="date-order", filepath=filepath)



    def start(self):
        while True:
            analyzer = choose_analyzer()

            if analyzer == 1:
                self.run_commit_analyzer()
            elif analyzer == 2:
                self.run_test_debt_analyzer()
            elif analyzer == 3:
                self.run_code_churn_analyzer()
            elif analyzer == 4:
                self.run_code_file_path_analyzer()

            run_again = input("\nWould you like to run the analysis again? (y/n): ").strip().lower()
            if run_again != "y":
                print("Exiting...")
                break