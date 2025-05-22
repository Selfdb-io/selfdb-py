#!/bin/bash
# Cleanup script to remove build artifacts

cd "$(dirname "$0")/.." 

echo "Cleaning up build artifacts..."

# Remove build directory
if [ -d "build" ]; then
  rm -rf build
  echo "Removed build directory"
fi

# Remove dist directory
if [ -d "dist" ]; then
  rm -rf dist
  echo "Removed dist directory"
fi

# Remove *.egg-info directories
find . -name "*.egg-info" -type d -exec rm -rf {} +

echo "Cleanup complete!" 