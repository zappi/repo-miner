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



def classify_churn(churn_data, relative_threshold=0.2):
    good_relative_churn = []
    bad_relative_churn = []

    for file_path, file_data in churn_data["file_churn"].items():

        # Calculate average relative churn rate
        if file_data["modifications"] > 0:
            avg_relative_churn = file_data["relative_churn"] / file_data["modifications"]
        else:
            avg_relative_churn = 0

        if avg_relative_churn < relative_threshold:
            good_relative_churn.append(file_path)
        else:
            bad_relative_churn.append(file_path)

    return good_relative_churn, bad_relative_churn

def report_code_churn(churn_data, developer_contribution):
    print("\nSummary of Code Churn Analysis:")
    print(f"Total commits analyzed: {churn_data['total_commits']}")
    print(f"Total lines added: {churn_data['total_lines_added']}")
    print(f"Total lines deleted: {churn_data['total_lines_deleted']}")
    print(f"Total files changed: {len(churn_data['total_files_changed'])}")

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

    # Classify relative churn as good or bad
    good_relative_churn, bad_relative_churn = classify_churn(churn_data)


    print(f"\nGood Churn Files: {len(good_relative_churn)}")
    print(f"\nBad Churn Files: {len(bad_relative_churn)}")
    # for file in bad_churn:
    #    print(f"  - {file}")

    print("\nDeveloper contributions")
    for dev, commits in developer_contribution.items():
        print(f"{dev}: {commits} commits")