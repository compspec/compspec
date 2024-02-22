# Contributing

When contributing to Compspec Python, it is important to properly communicate the gist of the contribution.
If it is a simple code or editorial fix, simply explaining this within the GitHub Pull Request (PR) will suffice. But if this is a larger
fix or Enhancement, it should be first discussed with the project leader or developers.

Please note that this project has a [Code of Conduct](https://github.com/compspec/compspec/tree/main/.github/CODE_OF_CONDUCT.md).
Please follow it in all your interactions with the project members and users.

## Pull Request Process

1. All pull requests should go to the main branch.
2. Follow the existing code style precedent. The testing includes linting that will help, but generally we use black, isort, mypy, and pyflakes.
3. Test your PR locally, and provide the steps necessary to test for the reviewers.
4. The project's default copyright and header have been included in any new source files.
5. All (major) changes to Singularity Registry must be documented in the CHANGELOG.md in the root of the repository, and documentation updated here.
6. If necessary, update the README.md.
7. The pull request will be reviewed by others, and the final merge must be done by an OWNER.

If you have any questions, please don't hesitate to [open an issue](https://github.com/compspec/compspec/issues).

### Documentation

Want to contribute to the documentation here? Great! You'll need Jekyll and git.

#### Install git

Initially (on OS X), you will need to setup [Brew](http://brew.sh/) which is a package manager for OS X and [Git](https://git-scm.com/). To install Brew and Git, run the following commands:

```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install git
```
If you are on Debian/Ubuntu, then you can easily install git with `apt-get`

```bash
apt-get update && apt-get install -y git
```
