import sys
sys.path.append("..")
import waybackpy
import pytest


user_agent = "Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/20.0"

def test_clean_url():
    test_url = " https://en.wikipedia.org/wiki/Network security "
    answer = "https://en.wikipedia.org/wiki/Network_security"
    test_result = waybackpy.clean_url(test_url)
    assert answer == test_result

def test_url_check():
    InvalidUrl = "http://wwwgooglecom/"
    with pytest.raises(Exception) as e_info:
        waybackpy.url_check(InvalidUrl)

def test_save():
    # Test for urls that exist and can be archived.
    url1="https://github.com/akamhy/waybackpy"
    archived_url1 = waybackpy.save(url1, UA=user_agent)
    assert url1 in archived_url1
    
    # Test for urls that are incorrect.
    with pytest.raises(Exception) as e_info:
        url2 = "ha ha ha ha"
        waybackpy.save(url2, UA=user_agent)

    # Test for urls not allowed to archive by robot.txt.
    with pytest.raises(Exception) as e_info:
        url3 = "http://www.archive.is/faq.html"
        waybackpy.save(url3, UA=user_agent)
    
    # Non existent urls, test
    with pytest.raises(Exception) as e_info:
        url4 = "https://githfgdhshajagjstgeths537agajaajgsagudadhuss8762346887adsiugujsdgahub.us"
        archived_url4 = waybackpy.save(url4, UA=user_agent)

def test_near():
    url = "google.com"
    archive_near_year = waybackpy.near(url, year=2010, UA=user_agent)
    assert "2010" in archive_near_year

    archive_near_month_year = waybackpy.near(url, year=2015, month=2, UA=user_agent)
    assert ("201502" in archive_near_month_year) or ("201501" in archive_near_month_year) or ("201503" in archive_near_month_year)

    archive_near_day_month_year = waybackpy.near(url, year=2006, month=11, day=15, UA=user_agent)
    assert ("20061114" in archive_near_day_month_year) or ("20061115" in archive_near_day_month_year) or ("2006116" in archive_near_day_month_year)

    archive_near_hour_day_month_year = waybackpy.near("www.python.org", year=2008, month=5, day=9, hour=15, UA=user_agent)
    assert ("2008050915" in archive_near_hour_day_month_year) or ("2008050914" in archive_near_hour_day_month_year) or ("2008050913" in archive_near_hour_day_month_year)

    with pytest.raises(Exception) as e_info:
        NeverArchivedUrl = "https://ee_3n.wrihkeipef4edia.org/rwti5r_ki/Nertr6w_rork_rse7c_urity"
        waybackpy.near(NeverArchivedUrl, year=2010, UA=user_agent)

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

def test_total_archives():

    count1 = total_archives("https://en.wikipedia.org/wiki/Python (programming language)", UA=user_agent)
    assert count1 > 2000

    count2 = total_archives("https://gaha.e4i3n.m5iai3kip6ied.cima/gahh2718gs/ahkst63t7gad8", UA=user_agent)
    assert count2 == 0

if __name__ == "__main__":
    test_clean_url()
    print(".")
    test_url_check()
    print(".")
    test_get()
    print(".")
    test_near()
    print(".")
    test_newest()
    print(".")
    test_save()
    print(".")
    test_oldest()
    print(".")
    test_total_archives()
    print(".")
