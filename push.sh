#!/bin/bash

# Script to commit & push current branch with a default message if none is provided
# @Param #1: new branch name
# @Param #2: commit message

BRANCH_PARAM="master"
COMMENT="$2"

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
COMMIT_COMMENT="${COMMENT:-"Progress"}"
BRANCH="${BRANCH_PARAM:-$CURRENT_BRANCH}"

./build.sh

if [ "${BRANCH_PARAM}" = "--help" ]; then
	echo "push.sh BranchName or \"\" (for current one) \"Commit-Message\""
	exit 1
else
	git add .
	git commit -m "${COMMIT_COMMENT}"

	echo "
----------------------------------------------
Pushing to "${BRANCH}", with Commit: "${COMMIT_COMMENT}"
----------------------------------------------
	"

	git push origin ${BRANCH}
	exit
fi
