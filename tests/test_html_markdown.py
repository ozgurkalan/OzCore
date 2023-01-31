"""HTML and Markdown functions"""

from ozcore import core

def test_html_to_markdown():
    result = core.utils.html_to_markdown("<h1>hello</h1>")
    expected = "# hello\n\n"
    
    assert result == expected
    
def test_markdown_to_html():
    result = core.utils.markdown_to_html("# hello\n\n")
    expected = "<h1>hello</h1>\n"

    assert result == expected