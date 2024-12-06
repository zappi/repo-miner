def filter_fix_commits(commit):
    if commit.modified_files:
        with open("commits_with_fix_message.txt", "a") as file:
            file.write(f"{commit.hash}\n")

