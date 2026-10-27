# Reddit post: Did Detectorists start a boom?

## Title

[OC] Did the BBC comedy Detectorists start a metal detecting boom? UK searches for "metal detecting" rose 41% in the months it was on air, but there was no lasting rise in searches or recorded finds after any series (Google Trends and the Portable Antiquities Scheme, 2004 to 2026)

## Body (optional)

I lined up monthly UK Google searches with the Portable Antiquities Scheme's finds register and modelled each series against trend and season. In months the show was on air, searches for "metal detecting" were 41% higher than the same months in other years, more than any of eight fake broadcast years, and finds recorded were 16% higher. But objects actually found in those months (by date of discovery) were only 4% up, within normal variation, and I found no lasting step after any series. The real jump in "metal detector" searches came later, peaking in the 2020 lockdown. Caveat: the register measures recording, which depends on finds officers' capacity, not detecting itself.

Interactive version: https://tristan-hotham.github.io/detectorists-effect/

## Source comment

Source: Google Trends, United Kingdom, web search, all categories, "metal detecting", "metal detector" and "detectorists" fetched together on one 0 to 100 scale, January 2004 to October 2026, retrieved October 2026 (Google Trends terms of use); Portable Antiquities Scheme database (British Museum, finds.org.uk), monthly counts of records created, metal-detector records and records by date of discovery, counted via the public API at api.finds.org.uk in October 2026 (PAS terms apply). Models: interrupted time series on a log scale with trend, calendar month, Covid and bulk-upload terms, Newey-West errors, plus placebo broadcast years and placebo breaks. Data compilation and code CC BY 4.0.

Tools: Python (pandas, NumPy, statsmodels, matplotlib)

Interactive: https://tristan-hotham.github.io/detectorists-effect/
