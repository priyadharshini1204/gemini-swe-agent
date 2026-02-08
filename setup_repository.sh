
#!/bin/bash
# Navigate to testbed
cd /testbed

# Reset to base commit
git reset --hard 84cc4ed5697b83a849e9106a09bfed501169cc20
git clean -fd

# Checkout the specific test file for the task
git checkout c4eebe6677acc4629cb541a98d5e91311444f5d4 -- openlibrary/tests/core/test_imports.py

echo "Environment ready."
