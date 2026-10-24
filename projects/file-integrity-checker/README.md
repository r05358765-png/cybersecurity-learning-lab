# File Integrity Checker

A beginner Python project that compares a file's current SHA-256 fingerprint with a saved fingerprint.

## What you will learn

- A hash is a fingerprint calculated from file contents.
- Changing the contents changes the fingerprint with extremely high probability.
- A trusted baseline lets you detect changes; it does not tell you who changed a file or whether a change was malicious.
- Python can read files, handle errors, and report results through exit codes.

## Run the practice exercise on Windows

You need Python 3.8 or later. No additional packages are required.

1. Download this repository: on its main page, click **Code → Download ZIP**.
2. Extract the ZIP, open the extracted folder, and open **projects/file-integrity-checker**.
3. Click the File Explorer address bar, type `powershell`, and press Enter.
4. Save the original fingerprint:

   ```powershell
   py checker.py baseline sample.txt
   ```

   Expected: `BASELINE SAVED: baseline.json`

5. Check the unchanged file:

   ```powershell
   py checker.py check sample.txt
   ```

   Expected: `UNCHANGED: File matches the saved baseline.`

6. Open `sample.txt` in Notepad, add a sentence, save, and run the same check again.

   Expected: `CHANGED: File differs from the saved baseline.`

If `py` is unavailable but Python is installed, try `python` instead. On macOS/Linux, use `python3` from a terminal in this folder.

## Understand the code

- `argparse` reads your command: baseline or check.
- `sha256_file()` reads the file in small chunks and calculates its fingerprint.
- `baseline` saves that fingerprint and the absolute file path in JSON.
- `check` calculates a new fingerprint and compares it with the saved one.
- Exit codes: **0** = baseline saved or unchanged, **1** = changed, **2** = error.

## Baseline handling and limits

The tool refuses to overwrite an existing baseline. To start a new practice run, deliberately remove your old baseline after reviewing the file, then create a new one.

The baseline records an absolute path, so moving the file requires a new baseline. Keep real baselines somewhere trusted: anyone who can modify both the file and baseline could hide changes. This tool checks one file on demand; it does not continuously monitor your computer or detect malware.

Local baseline files are ignored by Git because they can contain private file paths. Do not commit real baselines.

## Your lab notes

After you run it, record:
1. What command did you use?
2. What happened before and after editing the sample?
3. Why does the baseline need protection?
4. What would you improve next?

Project code was prepared with AI assistance. Running it, understanding it, and documenting your observations are the learner's next steps.
