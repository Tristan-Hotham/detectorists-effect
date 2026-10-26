# Did Detectorists start a boom? Data and code

Tristan Hotham, Independent researcher, 2026

Monthly data used to test whether the BBC comedy *Detectorists* (BBC Four 2014, 2015, 2017; BBC Two special 2022) changed metal detecting in Britain.

## Files
- `google_trends_gb.csv`: Google Trends, United Kingdom, web search, all categories, January 2004 to October 2026. Terms: "metal detecting", "metal detector", "detectorists", fetched together so they share one 0–100 scale. Retrieved October 2026.
- `pas_monthly.csv`: Portable Antiquities Scheme (British Museum) database counts per month, 2003 to September 2026: `created` (records created), `created_md` (records created whose discovery method is "Metal detector"), `discovered` (records by date of discovery). Counted with the public search API at api.finds.org.uk, October 2026. Counts change as records are added and edited.
- `analysis.py`: interrupted time-series models (log scale, linear trend, calendar-month terms, Covid and bulk-upload terms, on-air months, level steps after each series) with Newey-West errors, plus placebo breaks.
- `placebo_onair.py`: refits the on-air effect with the broadcast months moved to fake years.
- `results.json`, `placebo_onair.json`: model output.

## Notes
Finds recorded depend on finds liaison officers' capacity, not only on detecting activity. Finds by date of discovery are only used to 2019, because later finds are still being recorded. March 2007, March 2010 and January 2015 contain bulk uploads.

Licence: CC BY 4.0 for the data compilation and code. Google Trends and PAS data remain subject to their providers' terms.

AI use: I wrote the text, with drafting and editing assistance from Claude (Anthropic), which also helped collect the data and prepare the analysis code.
