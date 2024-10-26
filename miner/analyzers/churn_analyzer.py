def analyze_code_churn(commit, churn_data, developer_contribution):
    lines_added = 0
    lines_deleted = 0
    files_changed = set()
    ignored_files = ["yarn.lock", "Gemfile.lock"]

    # Analyze each modified file in the commit
    for mod in commit.modified_files:
        file_path = mod.new_path or mod.old_path
        if any(ignored_file in file_path for ignored_file in ignored_files) or file_path.endswith((".json", ".yml", ".snap", ".md")):
            continue


        # Calculate relative churn per commit
        total_lines = mod.nloc if mod.nloc else 1
        churned_lines = mod.added_lines + mod.deleted_lines
        relative_churn = churned_lines / total_lines if total_lines > 0 else 0

        # Accumulate total lines added and deleted for churned LOC / Total LOC
        lines_added += mod.added_lines
        lines_deleted += mod.deleted_lines
        files_changed.add(file_path)

        # Add file path to analyze data if it is not there yet
        if file_path not in churn_data["file_churn"]:
            churn_data["file_churn"][file_path] = {
                "modifications": 0,
                "lines_added": 0,
                "lines_deleted": 0,
                "churn_frequency": 0,
                "relative_churn": 0.0,
                "contributors": set()
            }

        # Update churn data for the file
        churn_data["file_churn"][file_path]["modifications"] += 1
        churn_data["file_churn"][file_path]["lines_added"] += mod.added_lines
        churn_data["file_churn"][file_path]["lines_deleted"] += mod.deleted_lines
        churn_data["file_churn"][file_path]["churn_frequency"] += 1
        churn_data["file_churn"][file_path]["contributors"].add(commit.author.name)
        churn_data["file_churn"][file_path]["relative_churn"] += relative_churn

    churn_data["total_commits"] += 1
    churn_data["total_lines_added"] += lines_added
    churn_data["total_lines_deleted"] += lines_deleted
    churn_data["total_files_changed"].update(files_changed)

    # Track developer contribution (commits per developer) for no reason
    if commit.author.name not in developer_contribution:
        developer_contribution[commit.author.name] = 0
    developer_contribution[commit.author.name] += 1
