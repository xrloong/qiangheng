# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Qiangheng (瑲珩) is a dynamic input method table generator for CJK characters. It generates encoding tables for input methods (Array, Boshiamy, Cangjie, Dayi, ZhengMa, FourCorner) and a drawing method (DynamicComposition) by analyzing character structure descriptions and applying method-specific encoding algorithms.

## Build & Development Commands

Package manager: **uv**. All Python execution goes through `uv run python3`.

```bash
# Install dependencies
make setup-python-environment   # runs: uv sync --all-extras

# Prepare data (converts XML→YAML via xsltproc, required before generating tables)
make prepare

# Generate encoding tables
make yaml                       # all methods
make yaml CMLIST="cj"           # single method (ar|bs|cj|dy|fc|zm|dc)
make xml                        # XML output format
make puretable                  # plain text mappings

# Run a single coding method directly
PYTHONPATH="src:libs:codings/CangJie" uv run python3 src/qiangheng.py -p coding.CangJie

# Run all tests
make test

# Run tests for a specific area
uv run pytest -c tests/pytest-libs.ini --rootdir=.    # library tests
uv run pytest -c tests/pytest-cj.ini --rootdir=.      # Cangjie tests
uv run pytest -c tests/pytest-ar.ini --rootdir=.      # Array tests
# Pattern: tests/pytest-{ar|bs|cj|dy|fc|zm|dc}.ini

# Run a single test file
uv run pytest tests/libs/testTreeParser.py

# Profiling
make profile
```

## Architecture

### Three-Phase Processing Pipeline

For each character: **Structure → Encode → Write**

1. **CharacterStructuringWork** (`src/hanzi/work.py`) — parses character structure from data files, expands component trees recursively using templates and substitutions
2. **CharacterCodeComputingWork** (`src/hanzi/work.py`) — applies the input method's encoding algorithm to the structured character
3. **Writer** (`src/writer.py`) — outputs results as YAML (primary), XML, text, or quiet

Orchestrated by `MainManager` (`src/model/MainManager.py`) which iterates over all characters in sorted order.

### Source Layout

- **`src/`** — main application: entry point (`qiangheng.py`), dependency injection (`injection/`), orchestration (`model/`), character processing (`hanzi/`), workspace management (`workspace/`)
- **`libs/`** — shared libraries: base coding classes (`coding/Base/`), element definitions (`element/`), parsers (`parser/`), tree structures (`tree/`)
- **`codings/`** — pluggable input method implementations (one directory per method)
- **`qhdata/`** — source data: character structure definitions (XML), per-method radix/substitute/adjust rules
- **`gen/`** — generated intermediate data (created by `make prepare`)
- **`xslt/`** — XSLT transforms for XML→YAML conversion and IME format generation
- **`tables/`** — generated output tables (yaml/, xml/, puretable/)

### Plugin Architecture (Adding/Modifying Input Methods)

Each input method lives in `codings/<Name>/coding/<Name>/` and must provide:

- **`__init__.py`** — exports: `CodeInfoEncoder`, `CodingRadixParser`, `fontVariance`, `codeMappingInfoInterpreter`, `codingMethodName`, `codingMethodDir`, `CodingRadixFileList`, `CodingSubstituteFileList`, `CodingAdjustFileList`
- **`<Name>.py`** — implements three classes extending base classes from `libs/coding/Base/`:
  - `CodeInfo` — represents a character's encoding (radix codes, positions)
  - `CodeInfoEncoder` — encodes characters based on composition operators (Turtle/龜, Loong/龍, Sparrow/雀, Silkworm/蚕, Goose/鴻, Loop/回, etc.)
  - `CodingRadixParser` — parses method-specific radical definitions from YAML

Method codes: `ar` (Array/行列), `bs` (Boshiamy/嘸蝦米), `cj` (Cangjie/倉頡), `dy` (Dayi/大易), `zm` (ZhengMa/鄭碼), `fc` (FourCorner/四角號碼), `dc` (DynamicComposition/動態組字)

### Dependency Injection

Uses the `injector` library. Modules defined in `src/injection/module.py`: `PackageModule`, `ManagerModule`, `IOModule`, `CharacterModule`, `ParserModule`. Key bindings in `src/injection/key.py`.

### PYTHONPATH Requirements

When running the application or tests, PYTHONPATH must include `src`, `libs`, and the relevant coding directory (e.g., `codings/CangJie`). The Makefile and pytest `.ini` files handle this automatically. Each pytest config (`tests/pytest-{method}.ini`) sets `pythonpath` to include the appropriate coding directory.

### Data Pipeline

```
qhdata/*.xml  →  xsltproc  →  gen/qhdata/*.yaml  →  Python processing  →  tables/
```

The `make prepare` step is required before any table generation. It uses `xsltproc` and `xmllint` to convert XML source data to YAML intermediates. Character structure data is in Chinese (XML tags like `<字符>`, `<字根>`, `<組字/>`).

### Composition Operators

Character structures are described using operators named after animals/concepts (defined in `libs/element/operator.py`): 龜(Turtle), 龍(Loong), 雀(Sparrow), 蚕(Silkworm), 鴻(Goose), 回(Loop), etc. These represent spatial relationships between components (top-bottom, left-right, enclosed, etc.). The `CodeInfoEncoder.setByComps()` method dispatches to operator-specific encoding via match/case.
