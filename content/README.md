# Structured content

Krybor RL stores reusable learning entities here. Narrative concept pages are MDX
files with YAML front matter; the metadata is validated before the web product
renders it.

Run the validator with:

```bash
make install-content
make content-check
```

Concept filenames must match their permanent IDs. Files beginning with `_` are
authoring templates and are not published or included in graph validation.
