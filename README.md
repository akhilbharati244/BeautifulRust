<p align="center">
  <img src="assets/banner.png" alt="Pixel art banner: a crab on a rocky shore at sunset, under the title Beautiful Rust and the subtitle Idiomatic Rust, distilled">
</p>

# Beautiful Rust

A Claude Code plugin with one skill, `rust-best-practices`, that teaches Claude to write
idiomatic, robust, maintainable Rust. Once installed, it loads automatically whenever a
task involves Rust, cargo, crates, the borrow checker, clippy, or `.rs` files.

The guidance is distilled from five sources, with a condensed digest of each bundled in
the skill so Claude can consult the original reasoning when it needs to:

- [Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/) (official rust-lang checklist)
- [Effective Rust](https://www.lurklurk.org/effective-rust/) by David Drysdale
- [Rust Design Patterns](https://rust-unofficial.github.io/patterns/) (idioms, patterns, anti-patterns)
- [Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)

Where the sources disagree, the skill picks a side and says why.

## Install in Claude Code

One step, from a terminal:

```bash
claude plugin install beautiful-rust --marketplace morganlinton/BeautifulRust
```

Or inside a Claude Code session:

```
/plugin marketplace add morganlinton/BeautifulRust
/plugin install beautiful-rust@beautiful-rust
```

Add `--scope project` to the terminal command to enable it for everyone working in the
current repository (each collaborator still runs the install once).

To try it for a single session without installing:

```bash
git clone https://github.com/morganlinton/BeautifulRust
claude --plugin-dir ./BeautifulRust
```

The skill is namespaced under the plugin, so you can invoke it explicitly with
`/beautiful-rust:rust-best-practices`. You rarely need to: it triggers on its own.

## Install in claude.ai

claude.ai takes a zip of the skill folder, with the folder as the zip root:

```bash
cd skills && zip -r ../rust-best-practices.zip rust-best-practices -x '*.DS_Store'
```

Upload it under **Customize > Skills** (on some plans this lives under Settings).
Code execution must be enabled first. Skills uploaded to claude.ai also sync down into
Claude Code sessions signed in with the same account.

## What the skill covers

`skills/rust-best-practices/SKILL.md` is about 500 lines, organized so Claude can scan
it while coding:

1. Mindset: Rust-shaped code, invalid states unrepresentable, application vs library
2. Pre-handback checklist: fmt, clippy with `-D warnings`, test, doc; lint policy
3. Ownership and borrowing: what to do instead of cloning for the borrow checker
4. Types and API design: naming, newtypes, common traits, builders, visibility, generics vs `dyn`
5. Errors and panics: `Option` vs `Result` vs panic, library vs application error types
6. Everyday idioms: iterators, combinators, `format!`, imports, drop guards
7. Concurrency and async: `Send` assertions, lock discipline, `async fn`, yield points
8. Unsafe and FFI: when it's allowed, `SAFETY:` comments, soundness, bindgen
9. Crates, modules, dependencies: workspace layout, features, semver
10. Documentation and comments
11. Tests
12. Performance, in order
13. Final checklist

`skills/rust-best-practices/references/` holds one digest per source for deeper lookups.

## Layout

```
BeautifulRust/
├── .claude-plugin/
│   ├── plugin.json         plugin manifest
│   └── marketplace.json    lets this repo act as its own marketplace
├── skills/
│   └── rust-best-practices/
│       ├── SKILL.md
│       └── references/
│           ├── google-rust-style-guide.md
│           ├── rust-api-guidelines.md
│           ├── effective-rust.md
│           ├── rust-design-patterns.md
│           └── microsoft-rust-guidelines.md
└── README.md
```

## Updating

Edit the skill, bump `version` in `.claude-plugin/plugin.json`, commit, and push.
Installed users pick up the new version with:

```bash
claude plugin update beautiful-rust
```

Validate before pushing:

```bash
claude plugin validate .
```

## License

MIT. See [LICENSE](LICENSE).
