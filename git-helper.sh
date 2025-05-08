#!/bin/bash

# Ask which branch to work on
read -p "Which branch do you want to push to? (development/main): " branch

# Save current branch
current_branch=$(git rev-parse --abbrev-ref HEAD)

if [ "$branch" == "development" ]; then
    # Ask for commit message only for development
    read -p "Enter commit message: " commit_message

    # Switch to development if not already there
    if [ "$current_branch" != "development" ]; then
        git checkout development
    fi

    git add .
    git commit -m "$commit_message"
    git push origin development
    echo "Changes committed and pushed to development branch."

elif [ "$branch" == "main" ]; then
    echo "Preparing to merge development into main..."

    # Switch to main, update it, merge development, and push
    git checkout main
    git fetch origin
    git pull origin main
    git merge development
    git push origin main
    git checkout development

    echo "Development branch merged into main and pushed."

else
    echo "Invalid branch name. Please choose 'development' or 'main'."
fi
