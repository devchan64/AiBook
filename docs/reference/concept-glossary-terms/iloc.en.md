<a id="iloc"></a>

## iloc

- Meaning: `iloc` is the Pandas selector used to choose rows and columns by integer position. If `loc` selects by label, `iloc` selects by position, such as the third row or the second column.
- Why it matters: Table code becomes much clearer when readers separate label-based selection from position-based selection. `iloc` also prevents a common beginner mistake: assuming that a numeric-looking index label is always the same thing as row position.
- Related concepts: `loc`, `index`, `column`
- Core Section: `P2-12.2`
- Appears in: `P2-12.3`
