# SelfDB Scripts

This directory contains utility scripts for the SelfDB project.

## Available Scripts

### Package Script (`package.sh`)
Builds distribution packages for the project.
```bash
./package.sh
```

### Upload Script (`upload.sh.template`)
Template for uploading packages to PyPI.

To use:
1. Create a copy of the template:
   ```bash
   cp upload.sh.template upload.sh
   chmod +x upload.sh
   ```
2. Set your PyPI token as an environment variable:
   ```bash
   export PYPI_API_TOKEN=your-token-here
   ```
3. Run the upload script:
   ```bash
   ./upload.sh
   ```

Note: The actual `upload.sh` file is ignored by git to prevent committing credentials.

### Cleanup Script (`cleanup.sh`)
Removes build artifacts like the `build/` and `dist/` directories.
```bash
./cleanup.sh
```

## Development Workflow

Typical workflow for releasing a new version:

1. Make your code changes
2. Run `./cleanup.sh` to remove previous build artifacts
3. Run `./package.sh` to build new distribution packages
4. Run `./upload.sh` to upload to PyPI (after setting up credentials) 