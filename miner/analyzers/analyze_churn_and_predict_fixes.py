import os
from datetime import datetime
from pydriller import Repository
import numpy as np
from miner.constants import FIX_KEYWORDS
from sklearn.linear_model import LogisticRegression

# M1 = churned LOC / Total LOC
# M2 = deleted LOC / Total LOC
# Other things, file count ratio etc.

def rename_existing_file(file_path):
    counter = 1
    while True:
        new_name = f"{os.path.splitext(file_path)[0]}-draft-{counter}.txt"
        if not os.path.exists(new_name):
            os.rename(file_path, new_name)
            break
        counter += 1


def setup_fix_commits_file(file_name):
    if os.path.exists(file_name):
        rename_existing_file(file_name)
    open(file_name, "w").close()


def count_files_with_extensions_in_repo(repo_path, extensions):
    extensions = tuple(f".{ext}" if not ext.startswith(".") else ext for ext in extensions)

    file_count = 0
    for root, _, files in os.walk(repo_path):
        file_count += sum(1 for file in files if file.endswith(extensions))

    print(file_count)
    return file_count



def analyze_churn_and_predict_fixes(repo_path):
    fix_commits_file = "commits_with_fix_message.txt"
    setup_fix_commits_file(fix_commits_file)

    fix_commit_hashes = set()
    allowed_suffixes = (".ts", ".js", ".java", ".rb", ".tsx", ".jsx")

    # Get the total file count in the repository with the given suffixes
    total_file_count = count_files_with_extensions_in_repo(repo_path, allowed_suffixes)
    print(f"Total file count with allowed suffixes: {total_file_count}")

    data = []

    def process_commit(commit):
        # Determine if this commit is fix-related
        is_fix = any(keyword in commit.msg.lower() for keyword in FIX_KEYWORDS)
        if is_fix and commit.hash not in fix_commit_hashes:
            with open(fix_commits_file, "a") as f:
                f.write(f"{commit.hash}\n")
            fix_commit_hashes.add(commit.hash)

        lines_added = 0
        lines_deleted = 0

        total_churned_loc = 0
        total_deleted_loc = 0
        total_file_loc = 0

        churned_files_count = 0

        for mod in commit.modified_files:
            file_path = mod.new_path or mod.old_path
            if file_path and file_path.endswith(allowed_suffixes):
                file_added = mod.added_lines if mod.added_lines else 0
                file_deleted = mod.deleted_lines if mod.deleted_lines else 0
                file_total = mod.nloc if mod.nloc and mod.nloc > 0 else 1

                lines_added += file_added
                lines_deleted += file_deleted

                churned_loc = file_added + file_deleted
                total_churned_loc += churned_loc
                total_deleted_loc += file_deleted
                total_file_loc += file_total

                if churned_loc > 0:
                    churned_files_count += 1

        net_churn = lines_added + lines_deleted

        # Compute M1, M2 if total_file_loc > 0
        if total_file_loc > 0:
            M1_commit = total_churned_loc / total_file_loc
            M2_commit = total_deleted_loc / total_file_loc
        else:
            M1_commit = 0
            M2_commit = 0

        # Compute M3: files_churned / total_file_count
        M3_commit = (churned_files_count / total_file_count) if total_file_count > 0 else 0

        # Only consider this commit if net_churn > 0
        if net_churn > 0:
            data.append((M1_commit, M2_commit, M3_commit, 1 if commit.hash in fix_commit_hashes else 0))

    # Adjust date range as needed
    since_date = datetime(2023, 1, 1, 17, 0, 0)
    to_date = datetime(2023, 3, 30, 23, 59, 59)
    for commit in Repository(repo_path, since=since_date, to=to_date, filepath=None, only_in_branch='main').traverse_commits():
        process_commit(commit)

    if len(data) == 0:
        print("No data collected. Check your repository path and date range.")
        return

    data_arr = np.array(data)
    X = data_arr[:, 0:3]  # M1, M2, M3
    y = data_arr[:, 3]    # is_fix (0 or 1)

    print(X)

    # Use a logistic regression model to see if higher churn metrics (M1, M2, M3) correlate with fix commits
    model = LogisticRegression()
    model.fit(X, y)

    print("Logistic Regression Coefficients:")
    print(f"M1 coefficient: {model.coef_[0][0]}")
    print(f"M2 coefficient: {model.coef_[0][1]}")
    print(f"M3 coefficient: {model.coef_[0][2]}")
    print(f"Intercept: {model.intercept_[0]}")

    probabilities = model.predict_proba(X)[:, 1]
    avg_probability_fix = np.mean(probabilities)
    print(f"Average predicted probability of being a fix commit: {avg_probability_fix:.2f}")