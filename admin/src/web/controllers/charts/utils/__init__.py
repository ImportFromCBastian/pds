import matplotlib.pyplot as plt
import io
import base64


def generate_bar_chart_img(x_array, counts, y_label, title):
    """
    Generate a chart image from the given data.
    """
    fig, ax = plt.subplots(figsize=(10, 7.5))

    max_index = counts.index(max(counts))
    bar_colors = ['tab:blue' if i !=
                  max_index else 'tab:red' for i in range(len(x_array))]

    ax.bar(x_array, counts, color=bar_colors)
    ax.set_ylabel(f'{y_label}')
    ax.set_title(f'{title}')

    ax.set_xticklabels(x_array, rotation=25, ha='right')

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    chart = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return chart
