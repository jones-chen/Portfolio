import os
from google.oauth2.service_account import Credentials
import gspread
import random
import datetime
from collections import defaultdict

sheetUrl = os.getenv('SHEET_URL')

scope = ['https://www.googleapis.com/auth/spreadsheets']

creds = Credentials.from_service_account_file(
    "/etc/secrets/credentials.json", scopes=scope)
gs = gspread.authorize(creds)

sh = gs.open_by_url(sheetUrl)

totalSheet = sh.worksheet('Total')

total_activity_data = totalSheet.get_all_records()

oneLinerSheet = sh.worksheet('One_liner')

one_liner_data = oneLinerSheet.get_all_records()

month_convert_dict = {'01': '一月', '02': '二月', '03': '三月', '04': '四月', '05': '五月',
                      '06': '六月', '07': '七月', '08': '八月', '09': '九月', '10': '十月', '11': '十一月', '12': '十二月'}

tw_city_list = ['台北', '新北', '基隆', '桃園', '新竹', '苗栗', '台中', '彰化', '雲林',
                '南投', '嘉義', '台南', '高雄', '屏東', '台東', '花蓮', '宜蘭', '澎湖', '金門', '馬祖']


def generateValidActivity():
    today = datetime.date.today()
    valid_activity = [
        activity for activity in total_activity_data if isActivityValid(activity, today)]

    return valid_activity


def isActivityValid(activity, today):
    start_date = datetime.datetime.strptime(
        activity['startDate'], '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(
        activity['endDate'], '%Y-%m-%d').date() if activity['endDate'] != '-' else None

    return start_date >= today or (end_date != None and end_date >= today)

def generate_city_dict():
    city_dict = {}

    for row in valid_activity_list:
        location = row['location'].replace('臺', '台')
        if location not in city_dict.keys():
            city_dict[location] = [row]
        else:
            city_dict[location].append(row)

    return city_dict

def generate_city_month_dict(city_dict):
    city_month_dict = defaultdict(dict)

    for key, value in city_dict.items():
        for activity in value:
            start_month = month_convert_dict[activity['startDate'][5:7]]
            end_month = month_convert_dict[activity['endDate']
                                           [5:7]] if activity['endDate'] != '-' else None

            if end_month == None or start_month == end_month:
                if start_month not in city_month_dict[key]:
                    city_month_dict[key][start_month] = [activity]
                else:
                    city_month_dict[key][start_month].append(activity)
            elif end_month != None and start_month != end_month:
                if start_month not in city_month_dict[key]:
                    city_month_dict[key][start_month] = [activity]
                elif start_month in city_month_dict[key]:
                    city_month_dict[key][start_month].append(activity)
                elif end_month not in city_month_dict[key]:
                    city_month_dict[key][end_month] = [activity]
                elif end_month in city_month_dict[key]:
                    city_month_dict[key][end_month].append(activity)

    return city_month_dict

def random_recommend_activity():
    activity = random.choice(valid_activity_list)
    return activity

def random_city_recommend_activity(activity_lst):
    activity = random.choice(activity_lst)
    return activity

def random_one_liner():
    one_liner = random.choice(one_liner_data)
    return one_liner

valid_activity_list = generateValidActivity()
