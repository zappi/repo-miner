`poetry install`

`poetry run miner`



### Commit analyzer

Browse through commits with the given number and keyword in message.
Currently, the message keyword is set to `["fix", "bug", "fail", "error", "problem", "wrong"]`

Returns the result of how many test files have changed in total.
However, it distinguishes commits so that it returns whether one or more test files have been modified in a commit.

Currently, writes commit hashes to a text file.

### Test debt analyzer

Browse through commits.

Dummy analyzer, to be improved.


###  Code churn analyzer

Analyze and classify both relative and absolute code churn.

Relative churn:
Indicate how much a file changes relative to its size, over time.
By capturing the frequency of changes (lines added, deleted, or modified) as a ratio to each file’s total lines of code, this approach offers a way to assess the stability of different parts of the codebase.
Files with high relative churn may indicate areas of potential instability, signaling higher volatility due to frequent adjustments or fixes.

Absolute churn:
Indicates the total volume of changes a file undergoes, without considering its size.
Absolute churn focuses on the raw count of lines added, deleted, or modified.
Unlike relative churn, which normalizes changes by file size, absolute churn highlights files with the highest number of changes overall, regardless of their total lines of code.

### File path analyzer

Browse through commits based on given file path.

To be improved.