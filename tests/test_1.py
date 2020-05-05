import sys
sys.path.append("..")
import waybackpy
import pytest


user_agent = "Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/20.0"


def test_save():
    # Test for urls that exist and can be archived.
    url1="https://github.com/akamhy/waybackpy"
    archived_url1 = waybackpy.save(url1, UA=user_agent)
    assert url1 in archived_url1
    
    # Test for urls that are incorrect.
    with pytest.raises(Exception) as e_info:
        url2 = "ha ha ha ha"
        archived_url2 = waybackpy.save(url2, UA=user_agent)

    # Test for urls not allowed to archive by robot.txt.
    with pytest.raises(Exception) as e_info:
        url3 = "http://www.archive.is/faq.html"
        archived_url3 = waybackpy.save(url3, UA=user_agent)
    
    # Non existent urls, test
    with pytest.raises(Exception) as e_info:
        url4 = "https://githfgdhshajagjstgeths537agajaajgsagudadhuss8762346887adsiugujsdgahub.us"
        archived_url4 = waybackpy.save(url4, UA=user_agent)
    
def test_near():
    url = "google.com"
    archive_near_year = waybackpy.near(url, year=2010, UA=user_agent)
    assert "2010" in archive_near_year

    archive_near_month_year = waybackpy.near(url, year=2015, month=2, UA=user_agent)
    assert "201502" in archive_near_month_year
    
    archive_near_day_month_year = waybackpy.near(url, year=2006, month=11, day=15, UA=user_agent)
    assert "20061115" in archive_near_day_month_year

    archive_near_hour_day_month_year = waybackpy.near(url, year=2009, month=8, day=5, hour=13, UA=user_agent)
    assert "2009080513" in archive_near_hour_day_month_year

def test_oldest():
    url = "github.com/akamhy/waybackpy"
    archive_oldest = waybackpy.oldest(url, UA=user_agent)
    assert "20200504141153" in archive_oldest

def test_newest():
    url = "github.com/akamhy/waybackpy"
    archive_newest = waybackpy.newest(url, UA=user_agent)
    assert url in archive_newest
    
def test_get():
    oldest_google_archive = waybackpy.oldest("google.com", UA=user_agent)
    oldest_google_page_text =  waybackpy.get(oldest_google_archive, UA=user_agent)
    assert "Welcome to Google" in oldest_google_page_text
