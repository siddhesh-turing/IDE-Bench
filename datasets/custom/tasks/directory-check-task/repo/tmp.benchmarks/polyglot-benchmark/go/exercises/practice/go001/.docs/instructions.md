You are given a string `s` and an integer `n`. Your task is to find all substrings of `s` that contain exactly `n` distinct characters.

Write a Golang function `findSubstringsWithNDistinctChars(s string, n int) []string` that returns a list of all such substrings. The substrings should be **distinct** and should appear in the same order as they appear in the original string.

### Input:
- `s` (1 <= len(s) <= 100): It is a string and it should consist of lowercase English letters only.
- `n` (1 <= n <= 26): An integer representing the number and length of distinct characters required in each substring.

### Output:
- A list of distinct substrings containing exactly `n` distinct characters.
- Return `nil` if it provides invalid inputs.

### Example:
**Input:**
```go
s := "abcab"
n := 3
```

**Output should be:**
```bash
["abc", "bca", "cab"]
```

Note:
1. Provide a complete working Go code.
2. Use `package main`
3. Do not include any `func main()`