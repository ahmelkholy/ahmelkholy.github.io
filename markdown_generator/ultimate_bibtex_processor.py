#!/usr/bin/env python3
"""
Enhanced BibTeX processor to create ultimate publication markdown files
"""

import os
import re
import shutil
import unicodedata
from datetime import datetime
from pathlib import Path


class UltimateBibTeXProcessor:
    def __init__(self, publications_dir):
        self.publications_dir = Path(publications_dir)
        self.existing_files = {}
        self.processed_keys = set()

        # Load existing files to check for duplicates
        self.scan_existing_files()

    def scan_existing_files(self):
        """Scan existing files and extract their keys"""
        for file in self.publications_dir.glob("*.md"):
            if file.name.endswith(".bib"):
                continue
            try:
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Extract title for duplicate detection
                    title_match = re.search(r'title:\s*"([^"]+)"', content)
                    if title_match:
                        title = title_match.group(1).lower().strip()
                        self.existing_files[title] = file.name

                    # Also extract key if available in comments
                    key_match = re.search(r"<!-- BibTeX Key: ([^-]+) -->", content)
                    if key_match:
                        key = key_match.group(1).strip()
                        self.processed_keys.add(key)
            except:
                pass

    def clean_text(self, text):
        """Clean and format text content with improved Unicode handling"""
        if not text:
            return ""

        # Remove extra whitespace and newlines
        text = re.sub(r"\s+", " ", text.strip())

        # Handle LaTeX-style formatting
        text = text.replace("{{", "").replace("}}", "")
        text = text.replace("{", "").replace("}", "")
        text = text.replace("\\&", "&")
        text = text.replace("\\_", "_")
        text = text.replace("\\textit", "")
        text = text.replace("\\", "")
        text = text.replace("--", "-")

        # Handle Unicode normalization for better compatibility
        text = unicodedata.normalize("NFKD", text)

        return text

    def clean_filename_text(self, text):
        """Clean text specifically for filenames, handling Cyrillic and special chars"""
        if not text:
            return "untitled"

        # First clean the text normally
        text = self.clean_text(text)

        # Transliterate Cyrillic to Latin
        text = self.transliterate_cyrillic(text)

        # Remove problematic characters for filenames
        text = re.sub(r"[^\w\s\-.]", "", text)
        text = re.sub(r"[\s_]+", "-", text)
        text = text.strip("-")

        return text[:60] if text else "untitled"

    def transliterate_cyrillic(self, text):
        """Simple Cyrillic to Latin transliteration"""
        cyrillic_map = {
            "а": "a",
            "б": "b",
            "в": "v",
            "г": "g",
            "д": "d",
            "е": "e",
            "ё": "yo",
            "ж": "zh",
            "з": "z",
            "и": "i",
            "й": "y",
            "к": "k",
            "л": "l",
            "м": "m",
            "н": "n",
            "о": "o",
            "п": "p",
            "р": "r",
            "с": "s",
            "т": "t",
            "у": "u",
            "ф": "f",
            "х": "kh",
            "ц": "ts",
            "ч": "ch",
            "ш": "sh",
            "щ": "shch",
            "ъ": "",
            "ы": "y",
            "ь": "",
            "э": "e",
            "ю": "yu",
            "я": "ya",
            "А": "A",
            "Б": "B",
            "В": "V",
            "Г": "G",
            "Д": "D",
            "Е": "E",
            "Ё": "Yo",
            "Ж": "Zh",
            "З": "Z",
            "И": "I",
            "Й": "Y",
            "К": "K",
            "Л": "L",
            "М": "M",
            "Н": "N",
            "О": "O",
            "П": "P",
            "Р": "R",
            "С": "S",
            "Т": "T",
            "У": "U",
            "Ф": "F",
            "Х": "Kh",
            "Ц": "Ts",
            "Ч": "Ch",
            "Ш": "Sh",
            "Щ": "Shch",
            "Ъ": "",
            "Ы": "Y",
            "Ь": "",
            "Э": "E",
            "Ю": "Yu",
            "Я": "Ya",
        }

        for cyrillic, latin in cyrillic_map.items():
            text = text.replace(cyrillic, latin)

        return text

    def extract_year_from_date(self, entry):
        """Extract year from various date formats"""
        # Try year field first
        if "year" in entry and entry["year"]:
            try:
                return int(entry["year"])
            except:
                pass

        # Try date field
        if "date" in entry and entry["date"]:
            date_str = entry["date"]
            # Match YYYY-MM-DD or YYYY format
            year_match = re.search(r"(\d{4})", date_str)
            if year_match:
                try:
                    return int(year_match.group(1))
                except:
                    pass

        # Default fallback
        return 2020

    def extract_authors(self, author_string):
        """Extract and format authors with better handling"""
        if not author_string:
            return "Unknown Author"

        authors = []
        # Split by 'and' and clean
        author_parts = re.split(r"\s+and\s+", author_string)

        for author in author_parts:
            # Clean author name
            author = self.clean_text(author)
            if author:
                authors.append(author)

        return "; ".join(authors) if authors else "Unknown Author"

    def format_date(self, year, month=None, day=None):
        """Format date for filename and frontmatter"""
        try:
            year_int = int(year) if year else 2020
            if day and month:
                return f"{year_int}-{month:02d}-{day:02d}"
            elif month:
                return f"{year_int}-{month:02d}-01"
            else:
                return f"{year_int}-01-01"
        except:
            return "2020-01-01"

    def get_title_or_fallback(self, entry):
        """Get title with fallback options"""
        title = self.clean_text(entry.get("title", ""))

        if title and title.lower() != "untitled":
            return title

        # Try shorttitle
        shorttitle = self.clean_text(entry.get("shorttitle", ""))
        if shorttitle:
            return shorttitle

        # Create fallback based on entry type
        entry_type = entry.get("ENTRYTYPE", "").lower()
        key = entry.get("KEY", "unknown")

        fallback_titles = {
            "article": f"Research Article ({key})",
            "inproceedings": f"Conference Paper ({key})",
            "thesis": f"Thesis ({key})",
            "software": f"Software ({key})",
            "book": f"Book ({key})",
            "incollection": f"Book Chapter ({key})",
            "misc": f"Publication ({key})",
        }

        return fallback_titles.get(entry_type, f"Publication ({key})")

    def create_filename(self, entry):
        """Create filename from entry with robust handling"""
        year = self.extract_year_from_date(entry)
        title = self.get_title_or_fallback(entry)

        # Create slug from title with better handling
        slug = self.clean_filename_text(title)

        # Format date
        date_str = self.format_date(year)

        filename = f"{date_str}-{slug}.md"
        return filename

    def get_venue_info(self, entry):
        """Extract venue information with robust fallback"""
        entry_type = entry.get("ENTRYTYPE", "").lower()

        venue = ""
        if entry_type == "article":
            venue = entry.get("journal", entry.get("journaltitle", ""))
        elif entry_type == "inproceedings":
            venue = entry.get("booktitle", entry.get("conference", ""))
        elif entry_type == "thesis":
            venue = entry.get("institution", entry.get("school", ""))
        elif entry_type == "software":
            venue = entry.get("organization", entry.get("publisher", ""))
        elif entry_type == "book":
            venue = entry.get("publisher", "")
        elif entry_type == "incollection":
            venue = entry.get("booktitle", entry.get("publisher", ""))
        elif entry_type == "misc":
            venue = entry.get(
                "publisher", entry.get("journal", entry.get("howpublished", ""))
            )
        else:
            # Try multiple fields as fallback
            venue = entry.get(
                "journal",
                entry.get(
                    "booktitle",
                    entry.get(
                        "institution",
                        entry.get("publisher", entry.get("organization", "")),
                    ),
                ),
            )

        venue = self.clean_text(venue)

        # Provide meaningful fallback if no venue found
        if not venue:
            fallback_venues = {
                "article": "Academic Journal",
                "inproceedings": "Conference Proceedings",
                "thesis": "Academic Institution",
                "software": "Software Repository",
                "book": "Academic Publisher",
                "incollection": "Book Chapter",
                "misc": "Publication",
            }
            venue = fallback_venues.get(entry_type, "Academic Publication")

        return venue

    def create_citation(self, entry):
        """Create formatted citation with robust handling"""
        authors = self.extract_authors(entry.get("author", ""))
        title = self.get_title_or_fallback(entry)
        year = self.extract_year_from_date(entry)
        venue = self.get_venue_info(entry)

        citation = f'{authors} ({year}). "{title}."'

        if venue:
            citation += f" <i>{venue}</i>."

        # Add volume/pages if available
        volume = entry.get("volume", "")
        number = entry.get("number", "")
        pages = entry.get("pages", "")

        if volume:
            citation += f" {volume}"
            if number:
                citation += f"({number})"
            if pages:
                citation += f":{pages}"
            citation += "."
        elif pages:
            citation += f" {pages}."

        return citation

    def get_paper_url(self, entry):
        """Extract paper URL"""
        doi = entry.get("doi", "")
        url = entry.get("url", "")

        if doi:
            doi = doi.strip()
            if doi.startswith("http"):
                return doi
            elif doi.startswith("doi.org"):
                return f"https://{doi}"
            elif doi.startswith("10."):
                return f"https://doi.org/{doi}"
            else:
                # Clean up doi
                doi = (
                    doi.replace("doi.org/", "")
                    .replace("https://", "")
                    .replace("http://", "")
                )
                if doi.startswith("10."):
                    return f"https://doi.org/{doi}"

        if url:
            return url

        return ""

    def is_duplicate(self, entry):
        """Check if publication is duplicate using multiple criteria"""
        title = self.get_title_or_fallback(entry)
        clean_title = title.lower().strip()

        # Check exact title match in existing files
        if clean_title in self.existing_files:
            return True

        # Check for similar titles (simple similarity check)
        for existing_title in self.existing_files.keys():
            # Remove common words and compare
            title_words = set(re.findall(r"\w+", clean_title.lower()))
            existing_words = set(re.findall(r"\w+", existing_title.lower()))

            # If titles share most words and are similar length, consider duplicate
            if len(title_words) > 3 and len(existing_words) > 3:
                intersection = title_words.intersection(existing_words)
                union = title_words.union(existing_words)
                similarity = len(intersection) / len(union) if union else 0

                if similarity > 0.8:  # 80% similarity threshold
                    return True

        return False

    def create_markdown_content(self, entry):
        """Create ultimate markdown content for publication with robust handling"""
        title = self.get_title_or_fallback(entry)
        authors = self.extract_authors(entry.get("author", ""))
        year = self.extract_year_from_date(entry)
        venue = self.get_venue_info(entry)
        abstract = self.clean_text(entry.get("abstract", ""))
        citation = self.create_citation(entry)
        paper_url = self.get_paper_url(entry)
        keywords = entry.get("keywords", "")
        entry_type = entry.get("ENTRYTYPE", "").lower()

        # Create permalink
        slug = self.clean_filename_text(title)
        permalink = f"/publication/{year}-{slug}"

        # Create excerpt
        if abstract:
            excerpt = abstract[:250] + "..." if len(abstract) > 250 else abstract
            excerpt = excerpt.replace("'", "\\'").replace('"', '\\"')
        else:
            entry_types = {
                "article": "journal article",
                "inproceedings": "conference paper",
                "thesis": "thesis",
                "software": "software",
                "book": "book",
                "incollection": "book chapter",
                "misc": "publication",
            }
            type_name = entry_types.get(entry_type, "publication")
            excerpt = f"This {type_name} presents research in power systems and electrical engineering."

        # Format date
        date_str = self.format_date(year)

        # Build frontmatter
        content = f"""---
title: "{title}"
collection: publications
permalink: {permalink}
excerpt: '{excerpt}'
date: {date_str}
venue: '{venue}'"""

        if paper_url:
            content += f"\npaperurl: '{paper_url}'"

        content += f"\ncitation: '{citation}'"

        if keywords:
            clean_keywords = self.clean_text(keywords)
            content += f"\nkeywords: '{clean_keywords}'"

        content += "\n---\n\n"

        # Add abstract if available
        if abstract:
            content += f"## Abstract\n\n{abstract}\n\n"
        else:
            # Add a generic description based on entry type
            descriptions = {
                "article": "This journal article presents original research findings.",
                "inproceedings": "This conference paper presents research findings and methodologies.",
                "thesis": "This thesis presents comprehensive research and analysis.",
                "software": "This software provides tools and implementations for research.",
                "book": "This book provides comprehensive coverage of the topic.",
                "incollection": "This book chapter contributes to the broader understanding of the field.",
                "misc": "This publication contributes to the academic literature.",
            }
            description = descriptions.get(
                entry_type, "This publication contributes to the academic literature."
            )
            content += f"## Description\n\n{description}\n\n"

        # Add publication details
        content += f"## Publication Details\n\n"
        content += f"- **Authors**: {authors}\n"
        content += f"- **Year**: {year}\n"
        content += f"- **Type**: {entry_type.title()}\n"
        content += f"- **Venue**: {venue}\n"

        # Add volume/pages if available
        volume = entry.get("volume", "")
        number = entry.get("number", "")
        pages = entry.get("pages", "")

        if volume:
            content += f"- **Volume**: {volume}\n"
        if number:
            content += f"- **Number**: {number}\n"
        if pages:
            content += f"- **Pages**: {pages}\n"

        # Add additional fields if available
        doi = entry.get("doi", "")
        if doi:
            content += f"- **DOI**: {doi}\n"

        # Add DOI/URL if available
        if paper_url:
            content += f"- **URL**: [{paper_url}]({paper_url})\n"

        content += "\n"

        # Add download link if available
        if paper_url:
            content += f"[Download paper here]({paper_url})\n\n"

        # Add recommended citation
        content += f"## Recommended Citation\n\n{citation}\n"

        return content

    def parse_bibtex_entry(self, entry_text):
        """Parse a single BibTeX entry with improved handling of nested braces"""
        # Extract entry type and key
        header_match = re.match(r"@(\w+)\{([^,]+),", entry_text)
        if not header_match:
            return None

        entry_type = header_match.group(1).lower()
        entry_key = header_match.group(2).strip()

        entry = {"ENTRYTYPE": entry_type, "KEY": entry_key}

        # Extract fields using improved pattern handling nested braces
        field_content = entry_text[header_match.end() :]

        # Remove trailing }
        field_content = field_content.rstrip().rstrip("}")

        # Use regex to find field patterns with nested brace handling
        pos = 0
        while pos < len(field_content):
            # Look for field pattern
            field_match = re.search(r"(\w+)\s*=\s*", field_content[pos:])
            if not field_match:
                break

            field_name = field_match.group(1).lower()
            field_start = pos + field_match.end()

            # Find the field value (handle both {} and "" quotes)
            if field_start >= len(field_content):
                break

            if field_content[field_start] == "{":
                # Handle brace-delimited value with nesting
                brace_count = 0
                value_start = field_start + 1
                value_end = value_start

                for i in range(value_start, len(field_content)):
                    if field_content[i] == "{":
                        brace_count += 1
                    elif field_content[i] == "}":
                        if brace_count == 0:
                            value_end = i
                            break
                        brace_count -= 1

                if value_end > value_start:
                    field_value = field_content[value_start:value_end].strip()
                    entry[field_name] = field_value
                    pos = value_end + 1
                else:
                    pos = field_start + 1

            elif field_content[field_start] == '"':
                # Handle quote-delimited value
                value_start = field_start + 1
                value_end = field_content.find('"', value_start)

                if value_end != -1:
                    field_value = field_content[value_start:value_end].strip()
                    entry[field_name] = field_value
                    pos = value_end + 1
                else:
                    pos = field_start + 1
            else:
                # Look for next comma or end
                next_field = re.search(r",\s*\w+\s*=", field_content[field_start:])
                if next_field:
                    field_value = field_content[
                        field_start : field_start + next_field.start()
                    ].strip()
                else:
                    field_value = field_content[field_start:].strip()

                # Clean up the value
                field_value = field_value.rstrip(",").strip()
                if field_value:
                    entry[field_name] = field_value

                if next_field:
                    pos = field_start + next_field.start() + 1
                else:
                    break

        return entry

    def parse_bibtex_file(self, file_path):
        """Parse BibTeX file and extract entries"""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        entries = []
        # Find all entries
        entry_pattern = r"@\w+\{[^@]*?(?=@\w+\{|$)"

        for match in re.finditer(entry_pattern, content, re.DOTALL):
            entry_text = match.group(0).strip()

            if entry_text:
                entry = self.parse_bibtex_entry(entry_text)
                if entry:  # Don't filter by processed_keys here, do it in main loop
                    entries.append(entry)

        return entries

    def cleanup_duplicates(self):
        """Remove files with corrupted characters or obvious duplicates"""
        files_to_remove = []

        for file in self.publications_dir.glob("*.md"):
            filename = file.name

            # Remove files with corrupted characters
            if "cyr" in filename.lower():
                files_to_remove.append(file)
            # Remove files that look like they have encoding issues
            elif any(char in filename for char in ["Ã", "©", "â"]):
                files_to_remove.append(file)

        for file in files_to_remove:
            print(f"Removing corrupted file: {file.name}")
            file.unlink()

    def process_files(self, bibtex_files):
        """Process all BibTeX files and create ultimate publications"""
        print("Cleaning up existing corrupted files...")
        self.cleanup_duplicates()

        all_entries = []

        for file_path in bibtex_files:
            print(f"Processing {file_path}...")
            try:
                entries = self.parse_bibtex_file(file_path)
                all_entries.extend(entries)
                print(f"Found {len(entries)} entries in {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

        # Create markdown files
        created_count = 0
        skipped_count = 0
        error_count = 0
        current_run_keys = set()  # Track keys processed in this run

        for entry in all_entries:
            try:
                # Check for duplicates within current run
                key = entry.get("KEY", "")
                if key in current_run_keys:
                    print(f"Skipping duplicate key in current run: {key}")
                    skipped_count += 1
                    continue

                # Check for duplicates against existing files
                if self.is_duplicate(entry):
                    title = self.get_title_or_fallback(entry)
                    print(f"Skipping existing duplicate: {title[:50]}...")
                    skipped_count += 1
                    continue

                filename = self.create_filename(entry)

                # Create markdown content
                content = self.create_markdown_content(entry)

                # Write file
                output_path = self.publications_dir / filename
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(content)

                print(f"Created: {filename}")
                created_count += 1

                # Update tracking
                title = self.get_title_or_fallback(entry)
                self.existing_files[title.lower()] = filename
                current_run_keys.add(key)

            except Exception as e:
                error_count += 1
                entry_key = entry.get("KEY", "unknown")
                entry_title = entry.get("title", "unknown title")
                print(
                    f"Error creating file for entry {entry_key} ({entry_title[:30]}...): {e}"
                )
                # Continue processing other entries even if one fails

        print(f"\nSummary:")
        print(f"- Created {created_count} new publication files")
        print(f"- Skipped {skipped_count} duplicates")
        print(f"- Encountered {error_count} errors")
        print(
            f"- Total publications now: {len(list(self.publications_dir.glob('*.md')))}"
        )

        if error_count > 0:
            print(
                f"\nNote: {error_count} entries had errors but processing continued for other entries."
            )

        return created_count


def main():
    # Define paths - use relative paths from script location
    script_dir = Path(__file__).parent
    publications_dir = script_dir.parent / "_publications"

    bibtex_files = [
        script_dir / "Exported Items.bib",
    ]

    # Process files
    processor = UltimateBibTeXProcessor(publications_dir)
    processor.process_files(bibtex_files)


if __name__ == "__main__":
    main()
