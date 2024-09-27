# Contributing

Thank you for contributing to Qiskit Metriq!

In Qiskit Metriq, we aim at creating an excellent work-space where all of us can feel welcomed, useful, respected and valued. If you are thinking to contribute to this project, you agree to abide by our [code of conduct](CODE_OF_CONDUCT.md) which we strongly recommend you read before continuing.

Following these guidelines communicates you value the time and effort of the core contributors and maintainers of this site and so, thank you!


## Table of contents

- [Start contributing](#start-contributing)
- [Before you start](#before-you-start)
- [Opening issues](#opening-issues)
- [Contributing code](#contributing-code)
  - [Tools](#tools)
  - [Clone your fork](#clone-your-fork)
  - [Assigning yourself](#assigning-yourself)
  - [Working on an issue](#working-on-an-issue)
  - [Adding tests](#adding-tests)
  - [Pull requests](#pull-requests)
  - [Code review](#code-review)
  - [Merging](#merging)
- [Secrets](#secrets)
  - [To Admins](#to-admins)


## Start contributing

This repository is for developing and maintaining the Qiskit Metriq project.

There are many ways of contributing: from catching a typo to coming up with a way
of improving performance or accessibility; you can open an issue, or you can prepare
a patch. In any case, read the contribution guidelines for opening new issues and
submitting pull requests.


## Before you start

Contributing to Qiskit Metriq assumes you have some level of [Git](https://git-scm.com) knowledge. 
For external contributors, a basic understanding of repositories, remotes, branches and commits is needed. 
For core contributors, you should know about resolving conflicts and rebasing too.

There are tons of useful resources about Git [out there](https://try.github.io/).


## Opening issues

You can open an [issue](https://github.com/qiskit-community/qiskit-metriq/issues/new) to:
* Report a bug: Provide steps to reproduce and expected behaviour.
* Suggest improvements to the current code.
* Request a new feature that we are not supporting.

Please include a detailed description in your issue.

## Contributing code

### Tools

You'll need to install these tools on your development environment:

1. [python](https://www.python.org/): the language qiskit-metriq is written in (Note that we currently support Python >=3.8,<3.11).
1. [git](https://git-scm.com/): for source control
1. [tox](https://tox.wiki/en): to run tests and build the documentation

Note: Installing the `pip` and `venv` python libraries will also be useful

To run a benchmark experiment using the latest version of `Qiskit`(RCs excluded):
```bash
tox -e py311
```
**Note:**
To run a specific version of `Qiskit`, you can manually update the `tox.ini` file with the required version.
Versions >=0.13,<=0.15 require numpy<1.20 and python<=3.8. You can run the tox environments `terra13`, `terra14` or `terra15` as:
```bash
tox -e py38-terra13
```

### Clone your fork

So you decided to get your hands dirty and start working on a patch? Then you
need to know that the project follows the
[Forking Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow)
with [Feature Branches](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow).

The above means we expect you to fork the project on your own GitHub account and make your `main` branch to
track this repository. A typical Git setup after
[forking the project](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo) is:

```sh
# After forking the repository in GitHub
git clone https://github.com/<your_username>/qiskit-metriq.git
cd qiskit-metriq
git remote add upstream https://github.com/Qiskit/qiskit-metriq.git
git remote set-url --push upstream no_push
git remote update upstream
git checkout main
git branch -u upstream/main
git pull
```

### Assigning yourself

The very first step to working on an issue is
[assigning yourself](https://docs.github.com/en/issues/tracking-your-work-with-issues/assigning-issues-and-pull-requests-to-other-github-users#assigning-an-individual-issue-or-pull-request)
the issue. This gives all contributors the visibility into who is working on what.

In case you are not a contributor just participate in the issue that you are interested to help, and we will
let you know the status of that issue.


### Working on an issue

When you are going to start working on an issue, make sure you are in your `main`
branch and that it is entirely up-to-date and create a new branch with a
meaningful name. The typical terminal code for this is:

```sh
git checkout main
git fetch upstream
git rebase upstream main
git checkout -b <my_branch_name>
```

Now start adding your changes and remember to commit often:

```sh
git commit
```

And include a summary and some notes or clarifications if needed:

```
Add a new feature.

The new feature will provide the possibility to do something awesome.
```

From time to time, you want to check if your `main` branch is still up-to-date. If not, you will need to
[rebase](https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase)
(or [merge](https://www.atlassian.com/git/tutorials/using-branches/git-merge)), then continue working:

```sh
git checkout main
git fetch upstream
git rebase upstream main
git checkout <my_branch_name>
git rebase main <my_branch_name>
```


### Testing

The team has a plan to introduce automated tests.
Contributions are welcome :)


### Pull requests

Pull requests serve a double purpose:
1. Share the code with the team. So almost everybody is aware of how the code base is evolving.
2. Provide an opportunity for improving code quality.

When you think your work is done, push the branch to your repository:

```sh
git push origin <my_branch_name>
# Start a pull request in GitHub
```

And
[create a pull request](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request)
against `main` (or a feature branch).
When creating the pull request, provide a description and, if applicable, 
[link with the issue that is being solved](https://docs.github.com/en/free-pro-team@latest/github/managing-your-work-on-github/linking-a-pull-request-to-an-issue).

Linking the issue has the advantage of automatically closing the related issue when the pull request is merged.

Describe the changes introduced by your PR in detail.
 including:
- summary
- list of main changes
- instructions to test your PR (environment, steps)
- does it require documentation update?


### Code review

When you open a PR you will see a template in the pull request body. Please read it carefully and fill in the necessary
information to help the code review process go smoothly.

Once you have sent a PR, the code contributors get notified, and there may be a code
review. The code review helps to solve implementation, semantic and maintainability issues.

During code reviews, there are two prominent roles: the reviewer and the contributor.
The reviewer acts as the keeper of best-practices and code quality, asking
clarifying questions, highlighting implementation errors and recommending changes.
We expect the contributor to take recommendations seriously and be willing to
implement suggested changes or take some other action instead.

Notice we don't expect the contributors to address **all** the comments, nor
the reviewer highlight **all** the issues, we hope both take some compromises to provide
as much value and quality as it fits in the estimated effort.

We don't expect discussions to happen in the pull requests. If there is a disagreement,
our recommendation is for the contributor to yield to the reviewer and for the reviewer
to suggest other alternatives.


### Merging

Once there is a positive review, the pull request can be merged. 
If you are an external contributor, expect your PR to be merged by a core contributor.

## Secrets
The secrets in this repository is managed by Qiskit Metriq admins.
The following tokens are stored as GitHub environment variables and used in our code:

`METRIQ_TOKEN`: Used to access Metriq client API
`BOT_ACCESS_TOKEN`: Used for automated experiment runs and creating new pull request for new benchmark results using GitHub Actions

### To Admins

`BOT_ACCESS_TOKEN` is a (classic) [Personal Access Token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) used to with `repo` and `workflow` scopes.

Current `BOT_ACCESS_TOKEN` expires: Dec 26 2024

(Please update expiration date above whenever this token is renewed)
