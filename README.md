hkust-latex-pqe-survey
==================

This is a latex template for the survey of HKUST PhD qualification examination.

Modified from: https://github.com/Cheedoong/hkust-latex-thesis

## Compile on Windows

With TeX Live installed, run `./build-survey.ps1` in PowerShell from this folder.
The script compiles `main.tex` with XeLaTeX and BibTeX through latexmk,
automatically repeating the required passes for references.
The resulting PDF is `output/pdf/survey.pdf`; build files and diagnostics stay in
`build/`. Existing source files and `thesis.pdf` are preserved.

The chapter files are inputs to `main.tex`, not standalone LaTeX documents.
