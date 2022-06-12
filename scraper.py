from lib2to3.pgen2.pgen import ParserGenerator
from re import S
import re
import requests
from bs4 import BeautifulSoup
import json

def get_player_photo(data):
    try:
        return data.find("img").attrs["src"]
    except AttributeError:
        return None


def get_team_photo(data):
    try:
        return data.find("a", href=True).find("img")["srcset"].strip().split(" ")[0]
    except AttributeError:
        return None


def get_header_info(data, index):
    try:
        return data[index]
    except:
        return None


def get_transfer_values(data):
    try:
        transfers = []
        n = 0

        for element in data.find_all("div", class_="tm-player-transfer-history-grid"):
            if n == 0:
                n += 1
                next
            else:
                if len(element.find_all("div")) >= 6:
                    transfer_data = {
                        "season" : element.find_all("div")[0].text.strip(),
                        "data" : element.find_all("div")[1].text.strip(),
                        "from" : element.find_all("div")[2].text.strip(),
                        "to" : element.find_all("div")[3].text.strip(),
                        "value" : element.find_all("div")[4].text.strip()
                    }
                    transfers.append(transfer_data)
        return transfers
    except:
        return None


def get_team(data):
    try:
        teams = {
            "photo" : get_team_photo(data.find("div", class_="data-header__box--big")), 
            "name" : data.find("div", class_="data-header__club-info").find("span", class_="data-header__club").find("a").text,
            "league" : data.find("div", class_="data-header__club-info").find("span", class_="data-header__league").find("a").text.strip(),
            "league_rang" : data.find("div", class_="data-header__club-info").find_all("span", class_="data-header__content")[0].text.strip(),
            "started_in_team" : data.find("div", class_="data-header__club-info").find_all("span", class_="data-header__content")[1].text.strip(),
            "contract_expiration_date" : data.find("div", class_="data-header__club-info").find_all("span", class_="data-header__content")[2].text.strip(),
        }

        return teams
    except:
        return None


def get_height(data):
    try:
        return data.find("span", itemprop="height").text.strip()
    except:
        return None


def get_city(data):
    try:
        return data.find("span", itemprop="birthPlace").text.strip()
    except:
        return None


def get_nationality(data):
    try:
        return data.find("span", itemprop="nationality").text.strip()
    except:
        return None


def get_date_of_birth(data):
    try:
        return (" ").join(data.find("span", itemprop="birthDate").text.split()[:-1])
    except:
        return None

def get_age(data):
    try:
        return data.find("span", itemprop="birthDate").text.split()[-1].strip("()")
    except:
        return None


def get_games_played(data):
    try:
        return data.find("div", id="yw1").find("tbody").find_all("td", "zentriert")[0].text.strip()
    except:
        return None


def get_last_time_updated(data):
    try:
        return data.find("p", class_="data-header__last-update").text.split(":")[1].lstrip()
    except:
        return None


def get_max_tranfer_value(data):
    try:
        return data.find("div", class_="tm-player-market-value-development__max-value").text.strip()
    except:
        return None

def get_leg(data):
    try:
        return data.find("span", string="Noga:").find_next_sibling().text.strip()
    except:
        return None

def get_position(data):
    try:
        return data.find("span", string="Pozycja:").find_next_sibling().text.strip()
    except:
        return None

def get_manager(data):
    try:
        return data.find("span", string="Menadżerowie:").find_next_sibling().text.strip()
    except:
        return None

def switch(header):
    switcher = {
                "Występy" : "games_played",
                "Bramki" :  "goals_scored",
                "Asysty" : "assists",
                "Żółte kartki" : "yellow_cards",
                "Kartki żółte i czerwone" : "second_yellow_cards",
                "Czerwone kartki" : "red_cards",
                "Stracone bramki" : "lost_goals",
                "Mecze bez straty bramki" : "clean_sheets"
            }
    return switcher.get(header, "-")

def get_performance(data):
    try:
        url = "https://www.transfermarkt.pl"
        main_page = data.find("a", class_="content-link", string="Łączne podsumowanie występów")["href"]

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
        headers = {'User-Agent': user_agent}
        cookies = {"cookie":"COPY_HERE_YOUR_COOKIE_FROM_BROWSER"}

        response = requests.get(url + main_page, headers=headers , cookies=cookies)
        soup = BeautifulSoup(response.content, "html.parser")

        header = soup.find("table", class_="items").find("thead").find_all(class_="zentriert")
        footer = soup.find("table", class_="items").find("tfoot").find_all(class_="zentriert")
        
        performance_data = {
            "games_played" : "-",
            "assists" : "-",
            "goals_scored" : "-",
            "yellow_cards" : "-",
            "second_yellow_cards" : "-",
            "red_cards" : "-",
            "lost_goals" : "-",
            "clean_sheets" : "-"
        }

        iterator = 0
        for i in header:
            argument = i.find("span")["title"]
            updater = {switch(argument) : footer[iterator].text}
            performance_data.update(updater)
            iterator += 1

        return performance_data
    except:
        return None

def get_contusion(data):
    try:
        url = "https://www.transfermarkt.pl"
        main_page = data

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
        headers = {'User-Agent': user_agent}
        cookies = {"cookie":"COPY_HERE_YOUR_COOKIE_FROM_BROWSER"}

        response = requests.get(url + main_page, headers=headers , cookies=cookies)
        soup = BeautifulSoup(response.content, "html.parser")

        contusions = []

        for contusion in soup.find("table", class_="items").find_all("tr"):
            if contusion.find_all("td") == []:
                contusion_data = None
            else:
                contusion_data = {
                    "season" : contusion.find_all("td")[0].text,
                    "description" : contusion.find_all("td")[1].text,
                    "from_data" : contusion.find_all("td")[2].text,
                    "to_data" : contusion.find_all("td")[3].text,
                    "absences" : contusion.find_all("td")[4].text,
                }

            contusions.append(contusion_data)

        return(contusions)

    except:
        return None


def get_value_history(data):
    try:
        script = data.find_all('script')
        script = ' '.join([str(elem) for elem in script])
        chartCode = script.split("var chart = new Highcharts.Chart")[1]
        data_with_padding = chartCode.split("'data':")[1]
        data = data_with_padding.split("}],'legend'")[0]
        data = data.encode().decode('unicode-escape')
        data = data.replace("\'", "\"")
        data = json.loads(data)

        values_history = []

        for i in range(len(data)):
            history_record = {
                "club" : data[i]["verein"],
                "date" : data[i]["datum_mw"],
                "value" : data[i]["mw"]
            }
            values_history.append(history_record)

        return values_history
    except:
        return None

def main():
    url = "https://www.transfermarkt.pl"
    main_page = "/ekstraklasa/startseite/wettbewerb/PL1/"
    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
    headers = {'User-Agent': user_agent}
    cookies = {"cookie":"COPY_HERE_YOUR_COOKIE_FROM_BROWSER"}
    
    response = requests.get(url + main_page, headers=headers , cookies=cookies)
    soup = BeautifulSoup(response.content, "html.parser")
    
    teams_table = soup.find(id="yw1")
    teams_urls = teams_table.find_all("td", class_="hauptlink no-border-links")
    
    json_object = {}

    for a in teams_urls:
        response = requests.get(url + a.find("a", href=True)["href"], headers=headers , cookies=cookies)
        soup = BeautifulSoup(response.content, "html.parser")

        players_table = soup.find(id="yw1").find("tbody")
        players_urls = players_table.find_all("td", class_="posrela")

        for player in players_urls:
            first_child = next(player.find("td", class_="hauptlink").children, None)
            response = requests.get(url + first_child.find("a", href=True)["href"], headers=headers , cookies=cookies)
            soup = BeautifulSoup(response.content, "html.parser")

            main_info = soup.find("div", class_="data-header__info-box")

            json_object[first_child.find("a", href=True)["href"].split("/")[1]] = {
                "photo" : get_player_photo(soup.find("div", class_="modal-trigger")),
                "number" : get_header_info(soup.find("h1", class_="data-header__headline-wrapper").text.split(), 0),
                "first_name" : get_header_info(soup.find("h1", class_="data-header__headline-wrapper").text.split(), 1),
                "last_name" : get_header_info(soup.find("h1", class_="data-header__headline-wrapper").text.split(), 2),
                "team" : get_team(soup),
                "date_of_birth" : get_date_of_birth(main_info),
                "age" : get_age(main_info),
                "nationality" : get_nationality(main_info),
                "city" : get_city(main_info),
                "height" : get_height(main_info),
                "leg" : get_leg(soup),
                "position" : get_position(soup),
                "manager" : get_manager(soup),
                "contusions" : get_contusion(first_child.find("a", href=True)["href"].replace("profil", "verletzungen")),
                "transfer_values" : get_transfer_values(soup),
                "value_history" : get_value_history(soup),
                "max_tranfer_value" : get_max_tranfer_value(soup),
                "performance" : get_performance(soup),
                "last_time_updated" : get_last_time_updated(soup)
            }

    return json_object

with open("players_info.json", "w") as outfile:
    json.dump(main(), outfile)
