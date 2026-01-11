def fill_and_resolve_locators(template_class, base_placeholders, extra_fields=None):
      placeholders = base_placeholders.copy()
      if extra_fields:
            placeholders.update(extra_fields)
      return template_class.resolve_all(**placeholders)