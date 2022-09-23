from playwright.sync_api import Page
import pytest

def test_title(page: Page):
    page.goto("/")
    assert page.title() == "博客來-會員登入"