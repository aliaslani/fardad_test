import os
import sys
import git

def clone_and_checkout_repo(repo_url, folder1, folder2):
    # Check if the target folders exist; if not, create them
    if not os.path.exists(folder1):
        os.makedirs(folder1)
    if not os.path.exists(folder2):
        os.makedirs(folder2)

    # Clone the repository
    repo = git.Repo.clone_from(repo_url, folder1)

    # Get the two most recent commits
    commits = list(repo.iter_commits('master', max_count=2))

    if len(commits) < 2:
        print("There are fewer than two commits in the repository.")
        sys.exit(1)

    # Check out the two most recent commits in separate folders
    repo.git.checkout(commits[0], b='commit1')
    repo.git.checkout(commits[1], b='commit2')

    # Create a second repository instance for the second folder
    repo2 = git.Repo.clone_from(repo_url, folder2)

    # Check out the second commit in the second folder
    repo2.git.checkout(commits[1])

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <repo_url> <folder1> <folder2>")
        sys.exit(1)

    repo_url = sys.argv[1]
    folder1 = sys.argv[2]
    folder2 = sys.argv[3]

    clone_and_checkout_repo(repo_url, folder1, folder2)
