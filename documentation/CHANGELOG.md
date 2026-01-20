# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - YYYY-MM-DD

### Added

- Config-driven dynamic CLI with init command, action executor, and console entrypoint.
- Step-based actions supporting shell and LLM steps, with templateable step output references.
- Command-level parameters with aggregated CLI options.
- New commit-message action.
- Rich-powered console features: colored output, status spinner, improved error panels, and enhanced output styling.
- Ability to copy CLI results to the clipboard.
- Pydantic-based Config model and improved init experience with action listing.

### Changed

- Project rebranded to Factotum; updated CLI naming, config paths, build scripts, release workflow, and documentation.
- README overhauled with installation and usage guidance.
- CLI help enhanced with epilog showing config path and init usage instructions.
- Imports reordered to follow PEP 8 grouping.

### Removed

- Legacy commands removed in favor of the new config-driven CLI.
- Extra/obsolete documentation removed.

### Fixed

- Removed extraneous plus sign formatting.

## [v0.4.0] - 2025-10-18

### Added

- Add follow-up prompt to commit command to allow user to directly commit changes with the generated message.

## [v0.3.0] - 2025-10-18

### Added

- Support for a default style file configuration.

### Changed

- Documentation now describes the default style file configuration flow.
- Replaced the uninstall_binary target with uninstall, which also removes configuration; updated uninstall docs and warnings.

### Removed

- Unnecessary documentation content.
- Obsolete code comments.
- Deprecated uninstall_binary target.

### Fixed

- Ensure the binary is built before installation by adding build_binary as a dependency of the install target.

## [v0.2.2] - 2025-10-18

### Fixed

- --style is now optional; the CLI gracefully warns when a specified style file is missing instead of failing.

## [v0.2.1] - 2025-10-16

### Changed

- Moved installation, usage, changelog, and development docs to the documentation/ directory; updated README links and workflow paths.
- Revised the introduction to be more concise and punchy.

### Removed

- Removed the install.sh installer script and related installation logic.

### Fixed

- Gracefully handle empty LLM responses in post/commit flows; standardized clipboard behavior.
- Safely extract message text from OpenAI responses, handling varying types and missing content.

## [v0.2.0] - 2025-10-16

### Added

- Integrated GPT-5 model for enhanced capabilities.

### Changed

- Refined commit prompt instructions and updated style guide for improved clarity and consistency.

## [v0.1.0] - 2025-10-16

### Added

- Ability to copy generated content directly to the clipboard via `pyperclip`.
- Instructions on how to report issues and bugs.

### Changed

- Install and usage instructions relocated from documentation to the README file; initial version of a CHANGELOG introduced.

### Fixed

- GitHub release workflow updated to use the correct path for pyinstaller.

### Refactored

- Message/content commands renamed to post/commit for greater clarity.
- Utility and prompt-related functions organized into separate modules for improved maintainability.
