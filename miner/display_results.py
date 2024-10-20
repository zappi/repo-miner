def display_commit_results(results):
    print("\nSummary of Commit Analysis:")
    print(f"Total commits with 'fix' in the message: {results['fix_commit_count']}")
    print(f"Commits with a single spec file changed: {results['single_spec_file_commits']}")
    print(f"Commits with multiple spec files changed: {results['multiple_spec_file_commits']}")

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