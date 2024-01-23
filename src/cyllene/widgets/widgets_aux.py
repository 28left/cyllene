from IPython.display import display, clear_output, Markdown
import ipywidgets as widgets
import markdown
import random


def update_output_widget(widget: widgets.Output, content: str):

    with widget:
        clear_output()
        # display(widgets.HTMLMath(markdown.markdown(content)))
        display(Markdown(content))
        # display(widgets.HTMLMath(content))


def shuffle_answers(num_choices):
    indices = [i for i in range(num_choices)]
    random.shuffle(indices)
    correct = indices.index(0)

    return indices, correct
