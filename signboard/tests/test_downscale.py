import numpy as np
import pytest


@pytest.fixture()
def Mosaic():
    from signboard.downscale import Mosaic
    return Mosaic


class TestMosaic():
    @pytest.mark.parametrize('tile_size, tile_count, aspect_ratio, layout, expected',
                             [
                                 ((160, 90), 9, 16/9, None, (3, 3)),
                                 ((160, 90), 10, 16/9, None, (4, 3)),
                                 ((90, 160), 10, 16/9, None, (6, 2)),
                                 ((160, 90), 5, 16/9, None, (3, 2)),
                                 ((90, 160), 5, 16/9, None, (4, 2)),
                                 ((100, 100), 7, 1.0, None, (3, 3)),
                                 ((80, 120), 5, 1.0, None, (3, 2)),
                             ])
    def test_autoarrange(self, Mosaic, tile_size, tile_count, aspect_ratio, layout, expected):
        m = Mosaic(tile_size, tile_count, aspect_ratio=aspect_ratio, layout=layout)
        assert all(m.layout == np.array(expected))
