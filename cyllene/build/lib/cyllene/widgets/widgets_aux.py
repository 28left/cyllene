from IPython.display import display, Markdown, clear_output
import ipywidgets as widgets


def update_output_widget(widget: widgets.Output, content: str):

    with widget:
        clear_output()
        display(Markdown(content))
