#!/bin/bash

# Script to fix git case-sensitivity issues on Windows/WSL
# This renames directories and files to lowercase in git tracking

set -e  # Exit on error

echo "=========================================="
echo "Git Case-Sensitivity Fix Script"
echo "=========================================="
echo ""

# Check if we're in a git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "ERROR: Not in a git repository!"
    exit 1
fi

echo "Current branch: $(git branch --show-current)"
echo ""
echo "This script will:"
echo "  1. Rename Data/ → data/"
echo "  2. Rename Images/ → images/"
echo "  3. Rename Images/Cleaned_Shoes/ → images/cleaned_shoes/"
echo "  4. Rename all other Images subdirectories to lowercase"
echo ""
read -p "Press ENTER to continue or Ctrl+C to cancel..."

# Step 1: Create backup branch
echo ""
echo "[1/6] Creating backup branch..."
BACKUP_BRANCH="backup-before-case-fix-$(date +%Y%m%d-%H%M%S)"
git branch "$BACKUP_BRANCH"
echo "✓ Created backup branch: $BACKUP_BRANCH"

# Step 2: Configure git to be case-sensitive temporarily
echo ""
echo "[2/6] Configuring git for case-sensitive operations..."
git config core.ignorecase false
echo "✓ Set core.ignorecase = false"

# Step 3: Fix Data → data
echo ""
echo "[3/6] Renaming Data/ → data/..."
if git ls-files | grep -q "^Data/"; then
    git mv Data Data_TEMP
    git mv Data_TEMP data
    echo "✓ Renamed Data/ → data/"
else
    echo "⊘ Data/ not found in git, skipping"
fi

# Step 4: Fix Images → images (parent directory)
echo ""
echo "[4/6] Renaming Images/ → images/..."
if git ls-files | grep -q "^Images/"; then
    # We'll handle this by renaming each subdirectory individually
    # because Windows doesn't like renaming the parent directly
    echo "  Processing Images subdirectories..."

    # Get list of immediate subdirectories in Images/
    SUBDIRS=$(git ls-files | grep "^Images/" | cut -d'/' -f2 | sort -u)

    for subdir in $SUBDIRS; do
        if [ -n "$subdir" ]; then
            lowercase_subdir=$(echo "$subdir" | tr '[:upper:]' '[:lower:]')

            if [ "$subdir" != "$lowercase_subdir" ]; then
                echo "    • Images/$subdir → images/$lowercase_subdir"

                # Create images/ directory if it doesn't exist in git
                mkdir -p images 2>/dev/null || true

                # Two-step rename via temp
                git mv "Images/$subdir" "Images/${subdir}_TEMP" 2>/dev/null || true
                git mv "Images/${subdir}_TEMP" "images/$lowercase_subdir" 2>/dev/null || true
            else
                # Already lowercase, just move to images/
                echo "    • Images/$subdir → images/$subdir (already lowercase)"
                mkdir -p images 2>/dev/null || true
                git mv "Images/$subdir" "images/$subdir" 2>/dev/null || true
            fi
        fi
    done

    echo "✓ Renamed all Images/ subdirectories to images/"
else
    echo "⊘ Images/ not found in git, skipping"
fi

# Step 5: Clean up any remaining Images/ references
echo ""
echo "[5/6] Cleaning up..."
# Remove empty Images directory from git if it exists
if git ls-files | grep -q "^Images/"; then
    echo "  Warning: Some Images/ files still exist in git index"
    echo "  Run 'git status' to see what remains"
fi

# Step 6: Restore git config
echo ""
echo "[6/6] Restoring git configuration..."
git config core.ignorecase true
echo "✓ Set core.ignorecase = true"

# Show status
echo ""
echo "=========================================="
echo "✓ Case-sensitivity fix complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Review changes: git status"
echo "  2. Commit changes: git commit -m 'Fix case-sensitivity in directory names'"
echo "  3. If something went wrong, restore: git reset --hard $BACKUP_BRANCH"
echo ""
echo "Backup branch created: $BACKUP_BRANCH"
echo ""
