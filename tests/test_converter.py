import os

from PIL import Image

from ai_cli.converter import convert_png_to_webp


def test_convert_single_png_to_webp(tmp_path):
    png_path = tmp_path / "sample.png"
    img = Image.new("RGB", (10, 10), color="white")
    img.save(png_path)

    results = convert_png_to_webp(str(png_path))
    assert len(results) == 1

    src, dst = results[0]
    assert os.path.exists(dst)
    assert dst.endswith(".webp")
