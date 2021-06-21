from wtforms import SelectMultipleField
from wtforms import widgets

from app import priority_options, status_options
from app.models import Tag

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.

    Adapted from https://wtforms.readthedocs.io/en/stable/specific_problems/
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

