# PDF Extraction Backend Documentation

This directory contains the Sphinx documentation for the PDF Extraction Backend API.

## Building the Documentation

### Prerequisites

Install the documentation dependencies:

```bash
pip install -e ".[docs]"
```

### Build HTML Documentation

To build the HTML documentation:

```bash
# Using make (Linux/macOS)
make html

# Using make.bat (Windows)
make.bat html

# Using sphinx-build directly
sphinx-build . _build/html
```

The built documentation will be available in `_build/html/index.html`.

### Live Development Server

For development with auto-reload:

```bash
# Install sphinx-autobuild if not already installed
pip install sphinx-autobuild

# Start live server
make livehtml
```

This will start a development server at `http://127.0.0.1:8000` that automatically rebuilds when files change.

### Other Output Formats

```bash
# PDF documentation (requires LaTeX)
make pdf

# Check for broken links
make linkcheck

# Run doctests
make doctest

# Generate coverage report
make coverage
```

## Documentation Structure

The documentation is organized into the following sections:

- **index.rst**: Main documentation index and overview
- **overview.rst**: API architecture and general information
- **endpoints.rst**: Detailed API endpoint documentation
- **extraction.rst**: PDF extraction tool documentation
- **benchmarking.rst**: Performance benchmarking guide
- **schemas.rst**: Data models and schema reference
- **examples.rst**: Usage examples and code samples

## Configuration

The documentation is configured in `conf.py` with the following key settings:

- **Theme**: Read the Docs theme (`sphinx_rtd_theme`)
- **Extensions**: Includes autodoc, napoleon, intersphinx, and MyST parser
- **Output formats**: HTML, PDF, and other standard Sphinx formats

## Contributing to Documentation

When making changes to the documentation:

1. Edit the appropriate `.rst` files in this directory
2. Use the live development server to preview changes
3. Ensure all links work by running `make linkcheck`
4. Test the build with `make html` before committing

### Writing Guidelines

- Use reStructuredText syntax (`.rst` files)
- Follow the existing formatting and structure
- Include code examples where appropriate
- Add cross-references between related sections
- Use proper section headings and hierarchy

### Adding New Documentation

1. Create new `.rst` files in this directory
2. Add them to the `toctree` in `index.rst`
3. Update any relevant cross-references
4. Test the build to ensure proper rendering

## Viewing the Documentation

Once built, you can view the documentation by:

1. Opening `_build/html/index.html` in a web browser
2. Using the live development server at `http://127.0.0.1:8000`
3. Accessing the API documentation at `http://localhost:8000/docs` (when the API server is running)

## API Documentation

In addition to this Sphinx documentation, the FastAPI application provides interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These interfaces are automatically generated from the API code and provide interactive testing capabilities.

## Troubleshooting

### Build Issues

If you encounter build errors:

1. Ensure all dependencies are installed: `pip install -e ".[docs]"`
2. Check for syntax errors in `.rst` files
3. Verify all image and file references are correct
4. Run `make clean` before rebuilding

### Missing Extensions

If you see errors about missing extensions:

```bash
pip install sphinx-rtd-theme sphinxcontrib-openapi myst-parser
```

### LaTeX Issues (PDF Build)

For PDF generation, you need a LaTeX distribution:

- **Windows**: MiKTeX or TeX Live
- **macOS**: MacTeX
- **Linux**: TeX Live (usually available via package manager)

## Deployment

To deploy the documentation:

1. Build the HTML documentation: `make html`
2. Copy the contents of `_build/html/` to your web server
3. Ensure proper MIME types are configured for `.html` files

For GitHub Pages or similar static hosting, you can use GitHub Actions to automatically build and deploy the documentation.