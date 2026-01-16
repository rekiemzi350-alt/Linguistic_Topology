package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
	"unicode/utf8"
)

// Language represents the parsed .lang file
type Language struct {
	Name        string            `json:"name"`
	MathType    string            `json:"math_type"`
	DirectRules map[int]string    `json:"-"`
	Tens        map[int]string    `json:"-"`
	Rules       map[string]string `json:"-"`
}

// ResultGroup represents a "River" of convergence
type ResultGroup struct {
	RiverID     int    `json:"river_id"`
	Count       int    `json:"count"`
	Percentage  int    `json:"percentage"`
	TailPreview string `json:"tail_preview"`
	Members     []int  `json:"members"`
}

// AnalysisResult holds the final output
type AnalysisResult struct {
	LanguageName   string        `json:"language_name"`
	DistinctRivers int           `json:"distinct_rivers"`
	Rivers         []ResultGroup `json:"rivers"`
}

func main() {
	filePath := flag.String("file", "", "Path to the .lang file")
	flag.Parse()

	if *filePath == "" {
		fmt.Println("Error: Please provide a file path using -file")
		os.Exit(1)
	}

	lang, err := parseLangFile(*filePath)
	if err != nil {
		fmt.Printf("Error parsing file: %v\n", err)
		os.Exit(1)
	}

	results := analyzeLanguage(lang)
	
	// Output JSON to stdout
	jsonData, _ := json.MarshalIndent(results, "", "  ")
	fmt.Println(string(jsonData))
}

// --- Parsing Logic ---

func parseLangFile(path string) (*Language, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	lang := &Language{
		Name:        "Unknown",
		MathType:    "western",
		DirectRules: make(map[int]string),
		Tens:        make(map[int]string),
		Rules:       make(map[string]string),
	}

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}
		
		parts := strings.SplitN(line, ":", 2)
		if len(parts) != 2 {
			continue
		}

		key := strings.TrimSpace(parts[0])
		val := strings.TrimSpace(parts[1])
		if idx := strings.Index(val, "#"); idx != -1 {
			val = strings.TrimSpace(val[:idx])
		}

		switch key {
		case "name":
			lang.Name = val
		case "math_type":
			lang.MathType = strings.ToLower(val)
		case "hundred", "hundred_sep", "ten_sep":
			lang.Rules[key] = val
		default:
			if n, err := strconv.Atoi(key); err == nil {
				lang.DirectRules[n] = val
				if n >= 20 && n <= 90 && n%10 == 0 {
					lang.Tens[n/10] = val
				}
			}
		}
	}
	return lang, scanner.Err()
}

// --- Analysis Logic ---

func analyzeLanguage(lang *Language) AnalysisResult {
	paths := make(map[int][]int)

	// Determine length function
	var lenFunc func(int, *Language) int
	switch lang.MathType {
	case "sumerian":
		lenFunc = getSumerianLen
	case "hebrew":
		lenFunc = getHebrewLen
	default:
		lenFunc = getWesternLen
	}

	// Simulation Loop
	for start := 0; start <= 100; start++ {
		path := []int{}
		curr := start
		for curr < 800 && len(path) < 100 {
			path = append(path, curr)
			l := lenFunc(curr, lang)
			if l == 0 {
				break
			}
			curr += l
		}
		paths[start] = path
	}

	// Grouping Logic

uniqueRivers := [][]int{}
	groups := make(map[int][]int)

	for start := 0; start <= 100; start++ {
		path := paths[start]
		if len(path) < 5 {
			continue
		}
		
		// Tail logic: last 5 elements
	tail := path[len(path)-5:]
		
		foundID := -1
		for i, river := range uniqueRivers {
			if compareSlices(tail, river) {
				foundID = i
				break
			}
		}

		if foundID == -1 {
		
uniqueRivers = append(uniqueRivers, tail)
			foundID = len(uniqueRivers) - 1
		}
		groups[foundID] = append(groups[foundID], start)
	}

	// Format Results
	finalGroups := []ResultGroup{}
	for id, members := range groups {
		tailStr := fmt.Sprintf("%v", uniqueRivers[id])
		tailStr = "..." + tailStr[1:len(tailStr)-1] // formatting [1 2 3] -> ...1 2 3
		
		finalGroups = append(finalGroups, ResultGroup{
			RiverID:     id,
			Count:       len(members),
			Percentage:  len(members), // Since total is roughly 100 (0-100 is 101, but close enough for UI)
			TailPreview: tailStr,
			Members:     members,
		})
	}

	// Sort by count descending
	sort.Slice(finalGroups, func(i, j int) bool {
		return finalGroups[i].Count > finalGroups[j].Count
	})

	// Renumber IDs for display
	for i := range finalGroups {
		finalGroups[i].RiverID = i + 1
	}

	return AnalysisResult{
		LanguageName:   lang.Name,
		DistinctRivers: len(finalGroups),
		Rivers:         finalGroups,
	}
}

func compareSlices(a, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

// --- Math Functions ---

func getWesternLen(n int, lang *Language) int {
	name := getWesternName(n, lang)
	// Remove spaces and hyphens
	clean := strings.ReplaceAll(name, " ", "")
	clean = strings.ReplaceAll(clean, "-", "")
	return utf8.RuneCountInString(clean)
}

func getWesternName(n int, lang *Language) string {
	if val, ok := lang.DirectRules[n]; ok {
		return val
	}
	if n > 999 {
		return ""
	}

	parts := []string{}
	langNameLower := strings.ToLower(lang.Name)

	if n >= 100 {
		h := n / 100
		rem := n % 100
		prefix := lang.DirectRules[h]

		// German/Spanish specifics
		if strings.Contains(langNameLower, "german") && h == 1 && prefix == "eins" {
			prefix = "ein"
		}
		if strings.Contains(langNameLower, "spanish") && h == 1 {
			prefix = ""
		}

		parts = append(parts, prefix)
		if hSep, ok := lang.Rules["hundred"]; ok {
			parts = append(parts, hSep)
		}

		if rem > 0 {
			if sep, ok := lang.Rules["hundred_sep"]; ok {
				parts = append(parts, sep)
			}
			parts = append(parts, getWesternName(rem, lang))
		}
		return strings.Join(parts, "")
	}

	if n >= 20 {
		t := n / 10
		rem := n % 10
		tVal := ""
		if val, ok := lang.Tens[t]; ok {
			tVal = val
		}

		if rem > 0 {
			sep := lang.Rules["ten_sep"]
			// Inversion check (German, Arabic)
			if sep == "und" || sep == "و" {
				unitStr := lang.DirectRules[rem]
				if strings.Contains(langNameLower, "german") && rem == 1 && unitStr == "eins" {
					unitStr = "ein"
				}
				parts = append(parts, unitStr, sep, tVal)
			} else {
				parts = append(parts, tVal)
				if sep != "" {
					parts = append(parts, sep)
				}
				parts = append(parts, lang.DirectRules[rem])
			}
		} else {
			parts = append(parts, tVal)
		}
	}
	return strings.Join(parts, "")
}

func getSumerianLen(n int, lang *Language) int {
	if n == 0 {
		return 0
	}
	if val, ok := lang.DirectRules[n]; ok {
		return utf8.RuneCountInString(val)
	}

	h := n / 60
	rem := n % 60
	length := 0

	if h > 0 {
		// Recursive logic for GESH (60s)
		length += getSumerianLen(h, lang)
	}

	if rem > 0 {
		tens := (rem / 10) * 10
		units := rem % 10

		if tens > 0 {
			if val, ok := lang.DirectRules[tens]; ok {
				length += utf8.RuneCountInString(val)
			} else if tVal, ok := lang.Tens[tens/10]; ok {
				length += utf8.RuneCountInString(tVal)
			}
		}
		if units > 0 {
			if val, ok := lang.DirectRules[units]; ok {
				length += utf8.RuneCountInString(val)
			}
		}
	}
	return length
}

func getHebrewLen(n int, lang *Language) int {
	// Standard Hebrew Gematria-style Logic
	if n > 999 { return 15 } // Fallback

	unitsLen := map[int]int{
		0: 3, 1: 3, 2: 4, 3: 4, 4: 4, 5: 4, 6: 3, 7: 4, 8: 4, 9: 4,
	}

	if n <= 10 {
		if val, ok := unitsLen[n]; ok { return val }
		if n == 10 { return 3 }
	}

	if n < 20 {
		if n == 11 { return 6 }
		if n == 12 { return 7 }
		u := n - 10
		return unitsLen[u] + 3
	}

	tensLen := map[int]int{
		20: 4, 30: 5, 40: 5, 50: 5, 60: 4, 70: 5, 80: 5, 90: 5,
	}

	if n < 100 {
		t := (n / 10) * 10
		u := n % 10
		if u == 0 { return tensLen[t] }
		return tensLen[t] + 1 + unitsLen[u] // +1 for "ve"
	}

	if n < 1000 {
		h := n / 100
		rem := n % 100
		base := 0
		if h == 1 {
			base = 3
		} else if h == 2 {
			base = 5
		} else {
			base = unitsLen[h] + 4
		}

		if rem == 0 { return base }
		return base + 1 + getHebrewLen(rem, lang)
	}
	return 0
}
