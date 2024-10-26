def analyze_file_path(commit, file_path):
    if commit.modified_files:
        for mod in commit.modified_files:
            if mod.new_path == file_path or mod.old_path == file_path:
                print("=" * 80)
                print(f"Commit Hash:   {commit.hash}")
                print(f"Author:        {commit.author.name}")
                print(f"Date:          {commit.committer_date.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Message:       {commit.msg}")
                print("-" * 80)

                print(f"Modified File: {mod.new_path}")
                print("Diff:\n")
                print(mod.diff)
                print("=" * 80)
                print("\n\n")