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


### File path analyzer

Browse through commits based on given file path.

To be improved.