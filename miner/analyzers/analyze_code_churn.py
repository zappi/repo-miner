def analyze_code_churn(commit, churn_data, developer_contribution):
    churn_count = 0
    lines_worked_on = 0
    total_loc = 0
    files_changed = set()
    ignored_files = ["yarn.lock", "Gemfile.lock"]

    # Analyze each modified file in the commit
    for mod in commit.modified_files:
        file_path = mod.new_path or mod.old_path
        if any(ignored_file in file_path for ignored_file in ignored_files) or file_path.endswith((".json", ".yml", ".snap", ".md")):
            continue

        total_lines = mod.nloc if mod.nloc else 1
        churned_loc = mod.added_lines + mod.deleted_lines
        deleted_loc = mod.deleted_lines

        churn_data["total_lines_added"] += mod.added_lines
        churn_data["total_lines_deleted"] += deleted_loc
        churn_data["total_files_changed"].add(file_path)

        churn_count += 1
        lines_worked_on += churned_loc + deleted_loc
        total_loc += total_lines
        files_changed.add(file_path)

        # Add file path to analyze data if it is not there yet
        if file_path not in churn_data["file_churn"]:
            churn_data["file_churn"][file_path] = {
                "churned_loc": 0,
                "deleted_loc": 0,
                "total_loc": 0,
                "churn_count": 0
            }

        # Update churn data for the file
        churn_data["file_churn"][file_path]["churned_loc"] += churned_loc
        churn_data["file_churn"][file_path]["deleted_loc"] += deleted_loc
        churn_data["file_churn"][file_path]["total_loc"] = total_lines
        churn_data["file_churn"][file_path]["churn_count"] += 1


    churn_data["total_commits"] += 1
    churn_data["total_files_changed"].update(files_changed)

    # Track developer contribution (commits per developer) for no reason
    # if commit.author.name not in developer_contribution:
    #    developer_contribution[commit.author.name] = 0
    # developer_contribution[commit.author.name] += 1