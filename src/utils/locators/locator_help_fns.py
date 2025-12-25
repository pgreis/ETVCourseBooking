def fill_and_resolve_locators(template_class, base_placeholders, extra_fields=None):
      """Copy placeholders, apply extra fields, and resolve the locators.

      - `template_class` should provide a `resolve_all(**placeholders)` classmethod.
      - `base_placeholders` is the dict from `locator_fillings[...]`.
      - `extra_fields` is a dict of placeholder keys -> values to add/override.
      """
      placeholders = base_placeholders.copy()
      if extra_fields:
            placeholders.update(extra_fields)
      return template_class.resolve_all(**placeholders)