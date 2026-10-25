# Changelog

All notable changes to this project are listed here. Versions follow
[Semantic Versioning](https://semver.org/), and the version lives in
`.claude-plugin/plugin.json`.

## [Unreleased]

## [1.2.0] - 2026-10-25

### Added

- **`rust-review` skill.** Point your agent at a file, crate, or diff and get a
  prioritized review: must fix, should fix, and consider. Every finding cites a
  `file:line` location, the rule it breaks with its source, and the smallest code change
  that fixes it. It runs fmt, clippy, and tests when a toolchain is available.
  On the inventory eval it passed 11 of 12 checks against 7 of 12 without the skill;
  the difference was rule citations, code fixes, and line references.
- **Drop-in lints** in `lints/`: a `[lints]` block for `Cargo.toml` and a `clippy.toml`.
  They make clippy enforce the machine-checkable rules, including no `unwrap()` outside
  tests, `// SAFETY:` on every unsafe block, reasons on every suppression, and no `bool`
  parameters. Every lint name was verified against clippy 0.1.99.
- An example review report in `examples/review-inventory.md`.
- An eval case for the review skill under `skills/rust-review/evals/`.
- README install instructions for agents other than Claude Code, since both skills are
  standard Agent Skills, and a before/after example of what the writing skill changes.
- This changelog.

### Verified

- Every Rust code example in the skills, the reference digests, and the README now
  compiles on stable Rust 1.99.

### Changed

- `rust-best-practices` points to the lints config when a project has no `[lints]` table.

## [1.1.0] - 2026-10-24

Tightened the skill based on a with/without comparison on three realistic tasks.
With the skill, 29 of 30 assertions passed; without it, 24 of 30.

- `bool` parameters are out of public and shared signatures. Use a two-variant
  enum or two methods instead. An existing `bool` is a smell to remove when refactoring.
- New section on refactoring someone else's code: fix every smell on the list, keep
  public behavior identical, show before and after for any signature you change, and
  flag quirks instead of silently fixing them.
- A hand-written `Ord` must come with matching `PartialEq` and `Hash`.
- Added three eval cases under `skills/rust-best-practices/evals/` and a Testing
  section in the README.

## [1.0.0] - 2026-10-23

First release.

- The `rust-best-practices` skill, distilled from the Google Rust Style Guide, the
  Rust API Guidelines, Effective Rust, Rust Design Patterns, and Microsoft's
  Pragmatic Rust Guidelines, with one reference digest per source.
- Packaged as a Claude Code plugin that is its own marketplace.
- MIT license, source attribution, and a plugin icon.

[Unreleased]: https://github.com/morganlinton/BeautifulRust/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/morganlinton/BeautifulRust/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/morganlinton/BeautifulRust/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/morganlinton/BeautifulRust/releases/tag/v1.0.0
