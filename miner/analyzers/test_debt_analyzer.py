def analyze_testing_debt(commit, debt_data, test_directories):
    modified_files = commit.modified_files
    feature_additions = 0
    test_additions = 0

    for mod in modified_files:
        if mod.new_path:
            # Count feature additions
            if not any(directory in mod.new_path for directory in test_directories):
                feature_additions += mod.added_lines

            # Count test additions
            elif any(directory in mod.new_path for directory in test_directories):
                test_additions += mod.added_lines


    if feature_additions > 0:
        debt_data["total_feature_additions"] += feature_additions
        if test_additions > 0:
            debt_data["commits_with_tests"] += 1
            debt_data["total_test_additions"] += test_additions
        else:
            debt_data["commits_without_tests"] += 1
            debt_data["debt_commits"].append({
                "hash": commit.hash,
                "message": commit.msg,
                "author": commit.author.name,
                "date": commit.committer_date,
                "feature_additions": feature_additions
            })