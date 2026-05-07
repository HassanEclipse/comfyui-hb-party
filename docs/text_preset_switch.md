# HB Text Preset Switch

Dynamic preset dropdown node for ComfyUI.

---

# Features

- Editable dropdown presets
- Workflow-safe persistence
- Node 2.0 compatible
- Undo-safe restoration
- Refresh-safe restoration
- Sortable entries
- App Mode compatible
- Hidden internal storage system

---

# Inputs

| Name | Type | Description |
|---|---|---|
| preset | STRING | Selected preset value |

---

# Outputs

| Name | Type | Description |
|---|---|---|
| string | STRING | Raw selected value |
| integer | INT | Converted numeric value |
| boolean | BOOLEAN | Boolean derived from integer |

---

# Preset Management

The node includes a built-in management UI allowing:

- Add new presets
- Delete presets
- Reorder presets
- Clear all presets
- Persist presets per-node

---

# Output Conversion

## STRING

Returns the raw selected value.

Example:

```txt
"7"
```

---

## INTEGER

Attempts numeric conversion.

Example:

```txt
"7" → 7
"3.8" → 3
"abc" → 0
```

---

## BOOLEAN

Derived from integer output.

Example:

```txt
0 → False
1 → True
7 → True
```

---

# Persistence Features

The node preserves:
- preset lists
- selected values
- sorting order
- custom labels

across:
- workflow save/load
- refresh
- undo/redo
- App Mode

---

# Notes

The node uses:
- hidden internal widgets
- JS-driven dynamic UI rebuilding
- workflow-local storage

to avoid:
- Python validation conflicts
- global state issues
- dropdown reset problems