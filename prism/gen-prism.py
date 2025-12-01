import json
import argparse
import re
import shutil
from pathlib import Path

# This mapping defines the relationship between Zed's semantic tokens
# and Prism's CSS classes.
ZED_TO_PRISM_MAP = {
    # Zed Token: [Prism Selectors]
    "comment": [".token.comment", ".token.prolog", ".token.doctype", ".token.cdata"],
    "comment.doc": [".token.comment.doc"],
    "punctuation": [".token.punctuation"],
    "keyword": [".token.keyword", ".token.atrule"],
    "operator": [".token.operator"],
    "type": [".token.class-name"],
    "type.builtin": [".token.builtin"],
    "function": [".token.function"],
    "function.builtin": [".token.builtin"],
    "variable.special": [".token.variable"],
    "constant.builtin": [".token.constant"],
    "boolean": [".token.boolean"],
    "number": [".token.number"],
    "string": [
        ".token.string",
        ".token.char",
        ".token.attr-value",
        ".token.text.literal",
    ],
    "property": [".token.property", ".token.attr-name"],
    "link_uri": [".token.url"],
    "error": [".token.deleted", ".token.error"],
    "title": [".token.selector", ".token.title"],
    "emphasis": [".token.italic"],
    "markup.bold": [".token.bold"],
    "markup.quote": [".token.entity"],
}


def generate_css_template(theme_name, editor_styles):
    """Generates the base CSS template for a Prism theme."""
    background = editor_styles.get("editor.background", "#ffffff")
    foreground = editor_styles.get("editor.foreground", "#000000")

    return f"""/**
 * Theme: {theme_name}
 * Generated from a Zed theme file.
 */

code[class*="language-"],
pre[class*="language-"] {{
    background: {background};
    color: {foreground};
    font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
    font-size: 1em;
    text-align: left;
    white-space: pre;
    word-spacing: normal;
    word-break: normal;
    line-height: 1.5;
    -moz-tab-size: 4;
    -o-tab-size: 4;
    tab-size: 4;
    -webkit-hyphens: none;
    -moz-hyphens: none;
    -ms-hyphens: none;
    hyphens: none;
}}

pre[class*="language-"] {{
    padding: 1em;
    margin: 0.5em 0;
    overflow: auto;
    border-radius: 0.3em;
}}

:not(pre) > code[class*="language-"] {{
    padding: 0.1em;
    border-radius: 0.3em;
    white-space: normal;
}}

.token.namespace {{
    opacity: .7;
}}
"""


def generate_theme_css(theme_data):
    """Generates the full CSS string for a single theme."""
    theme_name = theme_data["name"]
    syntax_styles = theme_data["style"]["syntax"]
    editor_styles = theme_data["style"]

    # Group selectors by their style to create compact CSS
    style_to_selectors = {}

    for zed_token, prism_selectors in ZED_TO_PRISM_MAP.items():
        style_data = syntax_styles.get(zed_token)
        if not style_data:
            continue

        color = style_data.get("color")
        font_style = style_data.get("font_style")
        font_weight = style_data.get("font_weight")

        # Create a unique key for this combination of styles
        style_key = (color, font_style, font_weight)

        if style_key not in style_to_selectors:
            style_to_selectors[style_key] = []

        style_to_selectors[style_key].extend(prism_selectors)

    # Build the CSS rules from the grouped styles
    css_rules = []
    for (color, font_style, font_weight), selectors in style_to_selectors.items():
        if not selectors:
            continue

        declarations = []
        if color:
            declarations.append(f"    color: {color};")
        if font_style:
            declarations.append(f"    font-style: {font_style};")
        if font_weight:
            declarations.append(f"    font-weight: {font_weight};")

        if declarations:
            selector_str = ",\n".join(sorted(list(set(selectors))))
            rules_str = "\n".join(declarations)
            css_rules.append(f"{selector_str} {{\n{rules_str}\n}}")

    # Combine base template and generated rules
    base_css = generate_css_template(theme_name, editor_styles)
    return f"{base_css}\n{'\n\n'.join(css_rules)}\n"


def theme_name_to_filename(name):
    """Converts a theme name like 'My Theme Name' to 'my-theme-name.css'."""
    return re.sub(r'[^\w-]+', '', name.lower().replace(" ", "-")) + ".css"


def main():
    parser = argparse.ArgumentParser(
        description="Generate Prism CSS themes from a Zed theme JSON file."
    )
    parser.add_argument("zed_theme_file", help="Path to the Zed theme JSON file.")
    args = parser.parse_args()

    zed_theme_path = Path(args.zed_theme_file)

    try:
        with zed_theme_path.open("r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing file: {e}")
        return

    script_dir = Path(__file__).resolve().parent
    output_dir = script_dir / "css"
    
    if output_dir.exists():
        shutil.rmtree(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)

    for theme in data.get("themes", []):
        try:
            css_content = generate_theme_css(theme)
            filename = theme_name_to_filename(theme["name"])
            output_path = output_dir / filename

            output_path.write_text(css_content)

            print(f"Successfully generated {output_path}")
        except KeyError as e:
            print(
                f"Warning: Skipping theme '{theme.get('name', 'Unknown')}' due to missing key: {e}"
            )


if __name__ == "__main__":
    main()
