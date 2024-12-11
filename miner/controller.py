from miner.analyzers.analyze_churn_and_predict_fixes import analyze_churn_and_predict_fixes
from miner.analyzers.analyze_code_churn import analyze_code_churn
from miner.analyzers.commit_analyzer import analyze_commits
from miner.analyzers.file_path_analyzer import analyze_file_path
from miner.analyzers.filter_fix_commits import filter_fix_commits
from miner.analyzers.test_debt_analyzer import analyze_testing_debt
from miner.constants import FIX_KEYWORDS
from miner.user_inputs import get_commit_limit, choose_analyzer, get_date, get_filepath
from miner.display_results import display_commit_results, display_testing_debt_results, report_code_churn
from pydriller import Repository

class AnalysisController:
    def __init__(self, repo_path, test_directories):
        self.repo_path = repo_path
        self.test_directories = test_directories
        self.commit_count = 0

        self.analyzers = {
            "Filtered Fix Commits": {
                "method": self.filtered_fix_commits,
                "description": "Find commits which message includes a fix keyword"
            },
            "Analyze Fix VS. Non-Fix Code churn": {
                "method": lambda: analyze_churn_and_predict_fixes(self.repo_path),
                "description": "Does code churn differ between commits with fixes and non-fixes. (Mann-Whitney U-test)"
            },
            # "Commit Analyzer": {
            #     "method": self.run_commit_analyzer,
            #     "description": "Analyzes commits for test file changes and fix keywords"
            # },
            # "Test Debt Analyzer": {
            #     "method": self.run_test_debt_analyzer,
            #     "description": "Analyzes commits for test additions, feature additions, and testing debt"
            # },
            "Code Churn Analyzer": {
                "method": self.run_code_churn_analyzer,
                "description": "Analyzes code churn metrics across all commits."
            },
            # "File Path Analyzer": {
            #     "method": self.run_code_file_path_analyzer,
            #     "description": "Analyzes changes to a specific file path in the repository."
            # }
        }

    @staticmethod
    def contains_fix_keyword(commit):
        return any(keyword in commit.msg.lower() for keyword in FIX_KEYWORDS)

    def traverse_commits(self, process_commit, filters=None, order="reverse", filepath=None):
        limit = get_commit_limit()

        for commit in Repository(self.repo_path, order=order, since=None, to=None, filepath=filepath).traverse_commits():
            if filters and not all(f(commit) for f in filters):
                continue

            if limit and self.commit_count >= limit:
                break

            process_commit(commit)
            self.commit_count += 1

    def filtered_fix_commits(self):
        def process_commit(commit):
            filter_fix_commits(commit)

        self.traverse_commits(process_commit, filters=[self.contains_fix_keyword])




    # def run_commit_analyzer(self):
    #     commit_data = {
    #         "single_test_file_commits": 0,
    #         "multiple_test_file_commits": 0
    #     }
    #
    #     def process_commit(commit):
    #         analyze_commits(commit, commit_data, self.test_directories)
    #
    #     self.traverse_commits(process_commit, filters=[self.contains_fix_keyword])
    #     commit_data["fix_commit_count"] = self.commit_count
    #
    #     display_commit_results(commit_data)

    # def run_test_debt_analyzer(self):
    #     debt_data = {
    #         "commits_with_tests": 0,
    #         "commits_without_tests": 0,
    #         "total_feature_additions": 0,
    #         "total_test_additions": 0,
    #         "debt_commits": []
    #     }
    #
    #     def process_commit(commit):
    #         analyze_testing_debt(commit, debt_data, self.test_directories)
    #
    #     self.traverse_commits(process_commit)
    #
    #     display_testing_debt_results(debt_data)

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
            chosen_analyzer = choose_analyzer(self.analyzers)

            self.analyzers[chosen_analyzer]["method"]()

            run_again = input("\nWould you like to run the analysis again? (y/n): ").strip().lower()
            if run_again != "y":
                print("Exiting...")
                break