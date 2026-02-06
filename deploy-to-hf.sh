#!/bin/bash
# Deployment script for Hugging Face Spaces

set -e

echo "🚀 Todo App AI Chatbot - Hugging Face Deployment"
echo "=================================================="
echo ""

# Check if HF username is provided
if [ -z "$1" ]; then
    echo "❌ Error: Hugging Face username required"
    echo "Usage: ./deploy-to-hf.sh <hf-username> <space-name>"
    echo "Example: ./deploy-to-hf.sh myusername todo-ai-chatbot"
    exit 1
fi

if [ -z "$2" ]; then
    echo "❌ Error: Space name required"
    echo "Usage: ./deploy-to-hf.sh <hf-username> <space-name>"
    echo "Example: ./deploy-to-hf.sh myusername todo-ai-chatbot"
    exit 1
fi

HF_USERNAME=$1
SPACE_NAME=$2
HF_REPO="https://huggingface.co/spaces/${HF_USERNAME}/${SPACE_NAME}"

echo "📋 Deployment Details:"
echo "   Username: $HF_USERNAME"
echo "   Space: $SPACE_NAME"
echo "   Repository: $HF_REPO"
echo ""

# Check if git remote exists
if git remote get-url hf > /dev/null 2>&1; then
    echo "✅ Hugging Face remote already configured"
else
    echo "🔗 Adding Hugging Face remote..."
    git remote add hf $HF_REPO
    echo "✅ Remote added successfully"
fi

echo ""
echo "📦 Checking for uncommitted changes..."
if [[ -n $(git status -s) ]]; then
    echo "⚠️  Warning: You have uncommitted changes"
    echo ""
    read -p "Commit changes before deploying? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        read -p "Enter commit message: " commit_msg
        git commit -m "$commit_msg"
        echo "✅ Changes committed"
    fi
fi

echo ""
echo "🚀 Pushing to Hugging Face Spaces..."
echo "   This may take a few minutes..."
echo ""

# Push to Hugging Face
git push hf main:main

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "📍 Next steps:"
echo "   1. Go to: $HF_REPO"
echo "   2. Click 'Settings' and add environment variables (secrets)"
echo "   3. Wait for build to complete (check Logs tab)"
echo "   4. Access your app at: https://${HF_USERNAME}-${SPACE_NAME}.hf.space"
echo ""
echo "📚 For detailed instructions, see: README-DEPLOYMENT.md"
echo ""
