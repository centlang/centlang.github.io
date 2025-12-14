# Frontend Structure

## Templates

Templates are stored in the `templates` directory. To use a template, start your
file with `{% extends <template name> %}`. Templates can extend other templates
as well.

Variables use the `{{ <variable name> }}` syntax:

```html
{{ content }} {{ page.base }}
```

## Adding content

Documentation and blog posts are written in Markdown. To add new content, create
a `.md` file in the `docs` or `news` directory. Don't forget to use the
appropriate template.

```md
{% extends docs %}

# Title

## Section

Content.
```

## Translations

Translations for HTML documents are defined in `translations.json`.
`{{ t.<key> }}` expands to the translated content for each language.

Translations for Markdown documents should be placed in the corresponding
language directory, e.g. to translate `docs/install.md`, put the translation at
`ru/docs/install.md`.

## Syntax highlighting

Syntax is highlighted by running `:TOhtml` in a headless Neovim process. The
build script expects `nvim` to be available in `$PATH`.
