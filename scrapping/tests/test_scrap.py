from scrapping.src.scrap import StackTab, ScrapStackOverflow
import pytest


def test_initialized_wrong_enum():
    with pytest.raises(Exception):
        ScrapStackOverflow(tab='Lonely')

def test_get_scrapped_url():
    so = ScrapStackOverflow(StackTab.ACTIVE)
    assert so.scrapped_url == 'https://stackoverflow.com/questions?tab=Active&pagesize=50'

def test_scrap_func_with_not_int():
    so = ScrapStackOverflow(StackTab.ACTIVE)
    with pytest.raises(Exception):
        so = ScrapStackOverflow(StackTab.ACTIVE)
        so.scrap(12.45)


def test_scrapped_item_length():
    so = ScrapStackOverflow(StackTab.BOUNTIFIED)
    val = 10
    data = so.scrap(val)
    assert data.shape[0] == val
