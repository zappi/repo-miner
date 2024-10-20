def analyze_commits(commit, commit_data, test_directories):
    spec_files = []

    if commit.modified_files:
        for mod in commit.modified_files:
            if mod.new_path and any(mod.new_path.startswith(directory) for directory in test_directories):
                spec_files.append(mod)

        if spec_files:
            print("="*80)
            print(f"Commit Hash:   {commit.hash}")
            print(f"Author:        {commit.author.name}")
            print(f"Date:          {commit.committer_date.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Message:       {commit.msg}")
            print("-"*80)

            for mod in spec_files:
                print(f"Modified File: {mod.new_path}")
                print("Diff:\n")
                print(mod.diff)
                print("="*80)
                print("\n\n")

            if len(spec_files) == 1:
                commit_data["single_spec_file_commits"] += 1
            else:
                commit_data["multiple_spec_file_commits"] += 1