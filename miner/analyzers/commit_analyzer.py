def analyze_commits(commit, commit_data, test_directories):
    test_files = []

    if commit.modified_files:
        for mod in commit.modified_files:
            if mod.new_path and any(mod.new_path.startswith(directory) for directory in test_directories):
                test_files.append(mod)

        if test_files:
            with open("commit_hashes.txt", "a") as file:
                file.write(f"{commit.hash}\n")

            print("="*80)
            print(f"Commit Hash:   {commit.hash}")
            print(f"Author:        {commit.author.name}")
            print(f"Date:          {commit.committer_date.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Message:       {commit.msg}")
            print("-"*80)

            for mod in test_files:
                print(f"Modified File: {mod.new_path}")
                print("Diff:\n")
                print(mod.diff)
                print("="*80)
                print("\n\n")

            if len(test_files) == 1:
                commit_data["single_test_file_commits"] += 1
            else:
                commit_data["multiple_test_file_commits"] += 1