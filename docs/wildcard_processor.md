# HB Wildcard Processor

Advanced wildcard processor for ComfyUI prompts.

---

# Features

- Recursive inline wildcard parsing
- Weighted wildcard selections
- File-based wildcards
- Subfolder wildcard support
- Multi-line prompt processing
- Wildcard report generation
- Deterministic seed behavior

---

# Inputs

| Name | Type | Description |
|---|---|---|
| text | STRING | Prompt containing wildcard syntax |
| seed | INT | Seed controlling deterministic selection |

---

# Outputs

| Name | Type | Description |
|---|---|---|
| text | STRING | Final processed prompt |
| report | STRING | Structured wildcard report |

---

# Supported Syntax

## Inline Wildcards

```txt
{3::Red|1::Blue|Green}
```

Weighted selections are supported.

---

## Nested Inline Wildcards

```txt
{2::{1::fast|slow}|{2::red|blue}}
```

Recursive parsing supported.

---

## File Wildcards

```txt
__colors__
```

Loads:

```txt
wildcards/colors.txt
```

---

## Subfolder Wildcards

```txt
__hair/long__
```

Loads:

```txt
wildcards/hair/long.txt
```

---

## Locked Wildcards

```txt
__!places__
```

Locks selection for reuse.

---

## Increment Offset

```txt
__+places__
```

Advances offset position.

---

## Multi-line Selection

```txt
__2$$places__
```

Selects multiple lines.

---

## Keyword Filtering

```txt
__places|Green__
```

Filters matching lines.

---

# Report System

Lines beginning with:

```txt
[Title]
```

are extracted into the report output.

Example:

```txt
[Library] bookshelves, desks
```

Produces:

```txt
[Places]: Library
```

---

# Example

## Input

```txt
He is at a __!places__ with a __colors__ bag.
```

## Output

```txt
He is at a bookshelves, desks with a Red bag.
```

---

# Notes

- Supports UTF-8 wildcard files
- Compatible with Windows/macOS/Linux
- Uses deterministic seeded randomization