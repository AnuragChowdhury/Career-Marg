"""
Document Understanding & Layout Analysis Service for Career मार्ग.
Analyzes layout structure, page count, column presence, tables, visual hierarchy,
formatting consistency, and ATS readability warnings.
"""

import os
import re
import fitz  # PyMuPDF
from typing import Dict, Any, Tuple
from models.schemas import DocumentAnalysis


class DocumentService:
    def detect_file_type(self, file_bytes: bytes, file_name: str, extracted_text: str) -> str:
        """
        Determines file type classification:
        - Digital PDF
        - Scanned PDF
        - Image Resume (JPG / JPEG / PNG)
        """
        ext = os.path.splitext(file_name)[1].lower()
        if ext in [".jpg", ".jpeg", ".png"]:
            return "Image-based Resume"
        
        if ext == ".pdf":
            # Check text length relative to page count
            clean_t = extracted_text.strip()
            if len(clean_t) < 100 or "scanned pdf" in clean_t.lower():
                return "Scanned PDF"
            return "Digital PDF"
            
        return "Unknown File Type"

    def analyze_layout(self, file_bytes: bytes, file_name: str, extracted_text: str) -> DocumentAnalysis:
        """
        Analyzes document visual/layout structure, formatting, tables, columns, and readability.
        """
        ext = os.path.splitext(file_name)[1].lower()
        file_type = self.detect_file_type(file_bytes, file_name, extracted_text)
        
        page_count = 1
        has_columns = False
        has_tables = False
        formatting_warnings = []
        
        if ext == ".pdf":
            try:
                doc = fitz.open(stream=file_bytes, filetype="pdf")
                page_count = len(doc)
                
                for page in doc:
                    # Check text blocks for multi-column heuristic
                    blocks = page.get_text("blocks")
                    # If blocks have overlapping horizontal X coordinates with distinct Y coordinates
                    x_coords = [b[0] for b in blocks if len(b) >= 4]
                    if len(x_coords) > 4:
                        # Check variance in starting X positions
                        distinct_x = len(set(round(x, -1) for x in x_coords))
                        if distinct_x >= 3:
                            has_columns = True
                    
                    # Table detection heuristic (drawings or rects)
                    drawings = page.get_drawings()
                    if len(drawings) > 15:
                        has_tables = True
            except Exception:
                pass

        # Text-based layout heuristics
        if "│" in extracted_text or "┌" in extracted_text or "|" in extracted_text:
            has_tables = True

        # Layout quality calculation (0 - 100)
        layout_quality = 90.0
        
        if has_columns:
            layout_quality -= 10.0
            formatting_warnings.append("Multi-column layout detected — may cause parsing issues in legacy ATS systems.")
            
        if has_tables:
            layout_quality -= 10.0
            formatting_warnings.append("Table structures detected — some ATS systems skip content inside complex table cells.")
            
        if page_count > 2:
            layout_quality -= 15.0
            formatting_warnings.append("Resume exceeds 2 pages — concise 1-2 page resumes receive higher ATS and recruiter engagement.")
            
        if file_type == "Scanned PDF":
            layout_quality -= 15.0
            formatting_warnings.append("Scanned PDF detected — text searchability relies heavily on OCR accuracy.")

        # Readability score calculation
        words = extracted_text.split()
        avg_word_length = sum(len(w) for w in words) / len(words) if words else 5.0
        readability_score = min(100.0, max(40.0, 100.0 - (avg_word_length * 3.0)))
        
        if not formatting_warnings:
            formatting_warnings.append("Clean document structure detected with good ATS readability.")

        return DocumentAnalysis(
            page_count=page_count,
            file_type=file_type,
            has_columns=has_columns,
            has_tables=has_tables,
            layout_quality=round(layout_quality, 1),
            readability_score=round(readability_score, 1),
            formatting_warnings=formatting_warnings
        )
