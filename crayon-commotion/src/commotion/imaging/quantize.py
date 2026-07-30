from __future__ import annotations

from commotion.models import GridCell, Palette, PaletteColor


def _srgb_channel_to_linear(c: int) -> float:
    c = c / 255
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def _lab_f(t: float) -> float:
    if t > 0.008856:
        return t ** (1 / 3)
    return 7.787 * t + 16 / 116


def rgb_to_lab(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    """
    Convert sRGB to CIE L*a*b* (D65 white point). Lab separates lightness
    (L) from hue (a/b), so two colors that are equally bright but different
    hues -- e.g. a pale blue and a pale pink -- end up far apart, unlike
    raw RGB distance, which mostly just measures brightness.
    """
    r = _srgb_channel_to_linear(rgb[0])
    g = _srgb_channel_to_linear(rgb[1])
    b = _srgb_channel_to_linear(rgb[2])

    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505

    x = x / 0.95047
    y = y / 1.0
    z = z / 1.08883

    fx = _lab_f(x)
    fy = _lab_f(y)
    fz = _lab_f(z)

    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def color_distance(
    rgb1: tuple[int, int, int],
    rgb2: tuple[int, int, int],
) -> float:
    """
    Squared distance in CIE L*a*b* space (perceptually uniform, unlike raw
    squared RGB distance).
    """
    lab1 = rgb_to_lab(rgb1)
    lab2 = rgb_to_lab(rgb2)
    return (
        (lab1[0] - lab2[0]) ** 2
        + (lab1[1] - lab2[1]) ** 2
        + (lab1[2] - lab2[2]) ** 2
    )

def nearest_palette_color(
    rgb: tuple[int, int, int],
    palette: Palette,
) -> PaletteColor:
    """
    Return the closest palette color.
    """

    best = palette.colors[0]
    best_distance = color_distance(
        rgb,
        (best.r, best.g, best.b),
    )

    for color in palette.colors[1:]:
        distance = color_distance(
            rgb,
            (color.r, color.g, color.b),
        )

        if distance < best_distance:
            best = color
            best_distance = distance

    return best

def quantize_image(
    pixels: list[list[tuple[int, int, int]]],
    palette: Palette,
) -> list[list[GridCell]]:
    """
    Convert every pixel to its nearest palette color.
    """

    result = []

    for row_index in range(len(pixels)):
        row = pixels[row_index]
        output_row = []

        for col_index in range(len(row)):
            rgb = row[col_index]

            output_row.append(
                GridCell(
                    row=row_index,
                    col=col_index,
                    rgb=rgb,
                    color=nearest_palette_color(
                        rgb,
                        palette,
                    ),
                )
            )

        result.append(output_row)

    return result