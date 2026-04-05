package main

import (
	"context"
	"reflect"
	"testing"
	"time"
)

func TestFindSubstringsWithNDistinctChars(t *testing.T) {
	tests := []struct {
		name        string
		inputString string
		n           int
		expected    []string
	}{
		// Valid cases
		{"test_HC_1", "abcabc", 2, []string{"ab", "bc", "ca"}},
		{"test_HC_2", "nhdfdfslsf", 3, []string{"nhd", "hdf", "dfs", "fsl", "lsf"}},
		{"test_HC_3", "abcdefghijklmnopqrstuvwxyz", 10, []string{"abcdefghij", "bcdefghijk", "cdefghijkl", "defghijklm", "efghijklmn", "fghijklmno", "ghijklmnop", "hijklmnopq", "ijklmnopqr", "jklmnopqrs", "klmnopqrst", "lmnopqrstu", "mnopqrstuv", "nopqrstuvw", "opqrstuvwx", "pqrstuvwxy", "qrstuvwxyz"}},
		{"test_HC_4", "abcab", 3, []string{"abc", "bca", "cab"}},
		{"test_HC_5", "aabbcc", 2, []string{"ab", "bc"}},
		{"test_HC_6", "abcdefghijklmnopqrstuvwxyz", 1, []string{"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}},
		{"test_HC_7", "abcdefghijklmnopqrstuvwxyz", 26, []string{"abcdefghijklmnopqrstuvwxyz"}},

		// Invalid input cases
		{"test_NC_1", "", 2, nil},
		{"test_NC_2", "abc", 0, nil},
		{"test_NC_3", "abc", 27, nil},
		{"test_NC_4", "abc", -5, nil},
		{"test_NC_6", "two words", 3, nil},
		{"test_NC_7", "two$+words", 3, nil},

		// Edge cases
		{"test_EC_1", "a", 1, []string{"a"}},
		{"test_EC_2", "aa", 1, []string{"a"}},
		{"test_EC_4", "abdde", 4, []string{}},
		{"test_EC_3", "abc", 4, []string{}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := findSubstringsWithNDistinctChars(tt.inputString, tt.n); !reflect.DeepEqual(got, tt.expected) {
				t.Errorf("findSubstringsWithNDistinctChars() = %v, want %v", got, tt.expected)
			}
		})
	}
}

const _TIMEOUT_IN_SECONDS = 120

func TestPerformance(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), _TIMEOUT_IN_SECONDS*time.Second)
	defer cancel()

	var result []string
	expectedResult := []string{"zx", "xc", "cv", "vb", "bn", "nm", "ma", "as", "sd", "df", "fg", "gh", "hj", "jk", "kl", "lq", "qw", "we", "er", "rt", "ty", "yu", "ui", "io", "op", "pz"}
	success := make(chan struct{}, 1)
	go func() {
		inputString := "zxcvbnmasdfghjklqwertyuiopzxcvbnmasdfghjklqwertyuiopzxcvbnmasdfghjklqwertyuiopzxcvbnmasdfghjklqwerty"
		for i := 0; i < 10; i++ {
			result = findSubstringsWithNDistinctChars(inputString, 2)
		}
		success <- struct{}{}
	}()

	select {
	case <-ctx.Done():
		t.Fail()
		t.Logf("Performance Test: Solution exceeding %d seconds", _TIMEOUT_IN_SECONDS)
	case <-success:
		if !reflect.DeepEqual(result, expectedResult) {
			t.Fail()
			t.Logf("Performance Test: Expected %v, got %v", expectedResult, result)
		}
		// solution sucessfully passed this performance test
	}
	close(success)
}
