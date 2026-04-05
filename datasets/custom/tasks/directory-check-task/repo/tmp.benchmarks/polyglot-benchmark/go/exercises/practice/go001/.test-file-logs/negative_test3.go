package main

import "regexp"

func findSubstringsWithNDistinctChars(s string, n int) []string {
	if len(s) < 1 || len(s) > 100 || n < 1 || n > 26 {
		return nil
	}

	// string must contain only lowercase letters.
	if !regexp.MustCompile(`^[a-z]+$`).MatchString(s) {
		return nil
	}
	result := []string{}
	seen := make(map[string]bool)

	for i := 0; i < len(s); i++ {
		j := (i + n)
		if j > len(s) {
			break
		}
		sub := s[i:j] // get substring with length `n`
		distinctCount := countDistinct(sub)
		if distinctCount == n && !seen[sub] {
			result = append(result, sub)
			seen[sub] = true
		}
	}

	return result
}

func countDistinct(s string) int {
	charMap := make(map[rune]bool)
	for _, r := range s {
		charMap[r] = true
	}
	return len(charMap)
}