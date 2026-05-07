# HB Tidy String

Utility node for cleaning and formatting text prompts.

---

# Features

- Removes repeated commas
- Fixes spacing
- Removes formatting artifacts
- Cleans prompt formatting
- Converts newlines into prompt-friendly formatting

---

# Inputs

| Name | Type | Description |
|---|---|---|
| text | STRING | Input text |
| tidy_enabled | DROPDOWN | Enable or disable cleanup |

---

# Outputs

| Name | Type |
|---|---|
| tidied_text | STRING |

---

# What It Cleans

## Multiple Commas

```txt
hello,,,
```

Becomes:

```txt
hello
```

---

## Newlines

```txt
moon
car
tree
```

Becomes:

```txt
moon, car, tree
```

---

## Extra Spaces

```txt
hello     world
```

Becomes:

```txt
hello world
```

---

## Removes Empty Quotes

```txt
""
```

Removed automatically.

---

## Removes Quoted Underscores

```txt
"_"
```

Removed automatically.

---

# Example

## Input

```txt
clean prompot,noSpace,   moreThanOnceSpace, twoCommas,, moreThanOnceComma,,,
moon, car
newLine
```

## Output

```txt
clean prompot, noSpace, moreThanOnceSpace, twoCommas, moreThanOnceComma, moon, car, newLine
```

---

# Notes

Useful for:
- Stable Diffusion prompts
- wildcard pipelines
- cleanup after text generation
- prompt normalization