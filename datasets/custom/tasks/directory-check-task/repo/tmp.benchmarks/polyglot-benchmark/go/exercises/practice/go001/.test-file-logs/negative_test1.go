package main

import "regexp"

func findSubstringsWithNDistinctChars(s string, n int) []string {
	if len(s) < 1 || len(s) > 100 || n < 1 || n > 26 {
		return nil
	}

	// Bug Introduced: Only ckecks for non-space character
	// Broken Constraint:
	//  - `s` (1 <= len(s) <= 100): It is a string and it should consist of lowercase English letters only.
	// Affected Tests:
	//  - TestFindSubstringsWithNDistinctChars/test_HC_2
	//  - TestFindSubstringsWithNDistinctChars/test_HC_3
	//  - TestFindSubstringsWithNDistinctChars/test_HC_4
	//  - TestFindSubstringsWithNDistinctChars/test_HC_6
	//  - TestFindSubstringsWithNDistinctChars/test_HC_7
	//  - TestFindSubstringsWithNDistinctChars/test_NC_7
	//  - TestFindSubstringsWithNDistinctChars/test_EC_1

	if !regexp.MustCompile(`^[\S]+$`).MatchString(s) {
		return nil
	}

	/*
		// string must contain only lowercase letters.
		if !regexp.MustCompile(`^[a-z]+$`).MatchString(s) {
			return nil
		}
	*/

	result := []string{}
	seen := make(map[string]bool)

	for i := 0; i < len(s); i++ {
		j := (i + n)
		if j > len(s)-1 {
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
