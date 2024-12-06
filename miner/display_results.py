from miner.constants import FIX_KEYWORDS


def display_commit_results(results):
    print("\nSummary of Commit Analysis:")
    print(f"Total commits with {FIX_KEYWORDS} in the message: {results['fix_commit_count']}")
    print(f"Commits with a single test file changed: {results['single_test_file_commits']}")
    print(f"Commits with multiple test files changed: {results['multiple_test_file_commits']}")

def display_testing_debt_results(results):
    print("\nTesting Debt Analysis:")
    print(f"Commits with tests: {results['commits_with_tests']}")
    print(f"Commits without tests: {results['commits_without_tests']}")
    print(f"Total feature additions: {results['total_feature_additions']}")
    print(f"Total test additions: {results['total_test_additions']}")

    if results["debt_commits"]:
        print("\nCommits with feature additions but no tests:")
        for debt_commit in results['debt_commits']:
            print("=" * 80)
            print(f"Commit Hash: {debt_commit['hash']}")
            print(f"Author:      {debt_commit['author']}")
            print(f"Date:        {debt_commit['date']}")
            print(f"Message:     {debt_commit['message']}")
            print(f"Feature Additions: {debt_commit['feature_additions']} lines")
            print("=" * 80)


def report_code_churn(churn_data, developer_contribution):
    print("\nSummary of Code Churn Analysis:")
    print(f"Total commits analyzed: {churn_data['total_commits']}")
    print(f"Total lines added: {churn_data['total_lines_added']}")
    print(f"Total lines deleted: {churn_data['total_lines_deleted']}")
    print(f"Total files changed: {len(churn_data['total_files_changed'])}")

    metrics = {}
    for file_path, data in churn_data["file_churn"].items():
        churned_loc = data["churned_loc"]
        deleted_loc = data["deleted_loc"]
        total_loc = data["total_loc"]
        churn_count = data["churn_count"]

        metrics[file_path] = {
            "M1 (Churned LOC / Total LOC)": churned_loc / total_loc if total_loc > 0 else 0,
            "M2 (Deleted LOC / Total LOC)": deleted_loc / total_loc if total_loc > 0 else 0,
            "M3 (Files Churned / File Count)": len(churn_data["total_files_changed"]) / len(churn_data["file_churn"]) if len(churn_data["file_churn"]) > 0 else 0,
            "M4 (Churn Count / Files Churned)": churn_count / len(churn_data["file_churn"]) if len(churn_data["file_churn"]) > 0 else 0,
            # "M5 (Weeks of Churn / File Count)": churn_data["weeks_of_churn"] / len(churn_data["file_churn"]) if len(churn_data["file_churn"]) > 0 else 0,
            # "M6 (Lines Worked On / Weeks of Churn)": churn_data["lines_worked_on"] / churn_data["weeks_of_churn"] if churn_data["weeks_of_churn"] > 0 else 0,
            "M7 (Churned LOC / Deleted LOC)": churned_loc / deleted_loc if deleted_loc > 0 else 0,
            # "M8 (Lines Worked On / Churn Count)": churn_data["lines_worked_on"] / churn_count if churn_count > 0 else 0,
        }

    for file_path, metrics_data in metrics.items():
        print(f"\nMetrics for {file_path}:")
        for metric, value in metrics_data.items():
            print(f"  {metric}: {value:.2f}")

    # Sort and display the results
    # sorted_files = sorted(
    #     churn_data["file_churn"].items(),
    #     key=lambda item: item[1]["churn_frequency"],
    #     reverse=True
    # )

    # Display top 15 files with the highest churn frequency
    # print("\nTop 15 Files with Highest Churn Frequency:")
    # for file_path, file_data in sorted_files[:15]:
    #     print(f"File: {file_path}")
    #     print(f" - Modifications: {file_data['modifications']}")
    #     print(f" - Lines Added: {file_data['lines_added']}")
    #     print(f" - Lines Deleted: {file_data['lines_deleted']}")
    #     print(f" - Churn Frequency: {file_data['churn_frequency']}")
    #     print(f" - Contributors: {', '.join(file_data['contributors'])}")
    #     print("=" * 80)
