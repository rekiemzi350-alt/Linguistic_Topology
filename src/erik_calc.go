package main

import (
	"encoding/csv"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

// Global Configuration
var consonants = "tnshrdlcmwf gpbvkjxqz"
var vowels = "eaoiu"
var letterValues = make(map[rune]int)
var commonWords = map[string]int{
	"the": 1, "be": 2, "to": 3, "of": 4, "and": 5, "a": 6, "in": 7, "that": 8, "have": 9, "i": 10,
} // Snip for brevity, the logic remains

func init() {
	for i, char := range strings.ReplaceAll(consonants, " ", "") {
		letterValues[char] = i + 1
	}
	for i, char := range vowels {
		letterValues[char] = i + 1
	}
	letterValues['y'] = 0
}

func getWordTrack1(word string) int {
	sum := 0
	for _, char := range strings.ToLower(word) {
		if val, ok := letterValues[char]; ok {
			sum += val
		}
	}
	return sum
}

func getWordTrack2(word string, t1 int) float64 {
	rank, ok := commonWords[strings.ToLower(word)]
	if !ok {
		rank = 1000
	}
	return float64(t1) * math.Log(float64(rank+1))
}

func getPlotValue(val float64) float64 {
	if val == 0 {
		return 0
	}
	if int(math.Abs(val))%2 != 0 {
		return val
	}
	return -val
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: erik_calc <input.txt>")
		return
	}

	content, _ := os.ReadFile(os.Args[1])
	text := string(content)

	// 1. ATOMIC LETTERS
	f1, _ := os.Create("waveform_level1_letters_" + os.Args[1] + ".csv")
	w1 := csv.NewWriter(f1)
	w1.Write([]string{"Sequence", "Char", "Value", "Plot_Y"})

	seq := 0
	for _, char := range text {
		lower := rune(strings.ToLower(string(char))[0])
		if (lower >= 'a' && lower <= 'z') {
			val := letterValues[lower]
			plot := getPlotValue(float64(val))
			if lower == 'y' { plot = 0 }
			w1.Write([]string{strconv.Itoa(seq), string(char), strconv.Itoa(val), fmt.Sprintf("%.0f", plot)})
			seq++
		}
	}
	w1.Flush()
	f1.Close()
    fmt.Println("Go: Atomic Waveform complete.")

    // Level 2/3/4 will be triggered by Python to ensure we keep the 
    // Grammatical tagging synced.
}
