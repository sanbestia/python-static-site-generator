import re
import pytest
from enum import Enum
from blocktype import BlockType
from html_functions import block_to_block_type


# ── HEADING ──────────────────────────────────────────────────────────────────

class TestHeading:
    def test_h1(self):
        assert block_to_block_type('# Heading') == BlockType.HEADING

    def test_h2(self):
        assert block_to_block_type('## Another heading') == BlockType.HEADING

    def test_h3(self):
        assert block_to_block_type('### Another nother heading') == BlockType.HEADING

    def test_h6_max_valid(self):
        assert block_to_block_type('###### Max level heading') == BlockType.HEADING

    def test_h7_too_many_hashes(self):
        assert block_to_block_type('####### Too many hashes') == BlockType.PARAGRAPH

    def test_no_space_after_hash(self):
        assert block_to_block_type('#No space heading') == BlockType.PARAGRAPH

    def test_hash_not_at_start(self):
        assert block_to_block_type('a # Trailing char heading') == BlockType.PARAGRAPH


# ── MULTILINE CODE ────────────────────────────────────────────────────────────

class TestMultilineCode:
    def test_basic_code_block(self):
        assert block_to_block_type('```\nThis is code\n```') == BlockType.MULTILINE_CODE

    def test_multiline_code_block(self):
        assert block_to_block_type('```\nline1\nline2\nline3\n```') == BlockType.MULTILINE_CODE

    def test_empty_code_block(self):
        assert block_to_block_type('```\n```') == BlockType.MULTILINE_CODE

    def test_closing_backticks_no_newline(self):
        assert block_to_block_type('```\nThis is also code```') == BlockType.MULTILINE_CODE

    def test_opening_backticks_no_newline(self):
        assert block_to_block_type('```This is not code\n```') == BlockType.PARAGRAPH


# ── QUOTE ─────────────────────────────────────────────────────────────────────

class TestQuote:
    def test_single_line_no_space(self):
        assert block_to_block_type('>single line quote') == BlockType.QUOTE

    def test_single_line_with_space(self):
        assert block_to_block_type('> single line quote with space') == BlockType.QUOTE

    def test_multiline_no_spaces(self):
        assert block_to_block_type('>line one\n>line two\n>line three') == BlockType.QUOTE

    def test_multiline_with_spaces(self):
        assert block_to_block_type('> line one\n> line two\n> line three') == BlockType.QUOTE

    def test_multiline_mixed_spacing(self):
        assert block_to_block_type('>line one\n> line two\n>line three') == BlockType.QUOTE

    def test_line_missing_arrow(self):
        assert block_to_block_type('>line one\nline two') == BlockType.PARAGRAPH

    def test_no_arrow_at_all(self):
        assert block_to_block_type('no arrow') == BlockType.PARAGRAPH

    def test_space_before_arrow(self):
        assert block_to_block_type('>line one\n >indented arrow') == BlockType.PARAGRAPH


# ── UNORDERED LIST ────────────────────────────────────────────────────────────

class TestUnorderedList:
    def test_single_item(self):
        assert block_to_block_type('- item one') == BlockType.UNORDERED_LIST

    def test_multiple_items(self):
        assert block_to_block_type('- item one\n- item two\n- item three') == BlockType.UNORDERED_LIST

    def test_line_missing_dash(self):
        assert block_to_block_type('- item one\n- item two\nbad item') == BlockType.PARAGRAPH

    def test_no_space_after_dash(self):
        assert block_to_block_type('-no space') == BlockType.PARAGRAPH

    def test_indented_dash(self):
        assert block_to_block_type('- item\n -indented dash') == BlockType.PARAGRAPH


# ── ORDERED LIST ──────────────────────────────────────────────────────────────

class TestOrderedList:
    def test_single_item(self):
        assert block_to_block_type('1. First item') == BlockType.ORDERED_LIST

    def test_multiple_items(self):
        assert block_to_block_type('1. First\n2. Second\n3. Third') == BlockType.ORDERED_LIST

    def test_skipped_number(self):
        assert block_to_block_type('1. First\n2. Second\n4. Fourth') == BlockType.PARAGRAPH

    def test_starts_at_zero(self):
        assert block_to_block_type('0. Starts at zero') == BlockType.PARAGRAPH

    def test_line_missing_number(self):
        assert block_to_block_type('1. First\n2. Second\nbad item') == BlockType.PARAGRAPH

    def test_no_space_after_period(self):
        assert block_to_block_type('1.No space') == BlockType.PARAGRAPH

    def test_starts_at_two(self):
        assert block_to_block_type('2. Starts at two\n3. Third') == BlockType.PARAGRAPH


# ── PARAGRAPH ─────────────────────────────────────────────────────────────────

class TestParagraph:
    def test_plain_text(self):
        assert block_to_block_type('Just a plain paragraph.') == BlockType.PARAGRAPH

    def test_multiline_paragraph(self):
        assert block_to_block_type('Two lines\nof a paragraph') == BlockType.PARAGRAPH

    def test_empty_string(self):
        assert block_to_block_type('') == BlockType.PARAGRAPH

    def test_mixed_markers(self):
        assert block_to_block_type('Mixed # heading and > quote') == BlockType.PARAGRAPH