from json_util.json_io import dict_to_json_file, json_file_to_dict
import pyupbit
import json

"""
회원가입
input
{
    "username": "new_user", #사용자 이름
    "password": "password123", #비밀번호
}
output
{
	"success" : "True or False",
}
"""
def register(register_info: dict):
	data_dict = json_file_to_dict()
	username = register_info['username']
	password = register_info['password']
	result = {"success": False}

	if(username in data_dict):
		result.update({"success": False})
	else:
		data_dict[username] = {
			"username": username,
			"password": password,
			"price": 0,
			"inventory": {
				"items": [],
				"fishing_rods": [
					{
						"name": "초보자 낚싯대",
						"durability": 100,
						"equipped": 1,
						"grade": "shallow"
					}
				]
			},
			"hunger": 100,
			"current_depth_level": "shallow",
			"game_progress": {
				"date": 0,
				"time_of_day": "morning"
			},
			"ranking": {
				"rank": 0,
				"earnings": 0
			}
		}
		# 음식 정보 불러오기
		file1 = open("fooddata.json", "r", encoding='UTF-8')
		jsondata1 = json.load(file1)
		file1.close()
		# 물고기 정보 불러오기
		file2 = open("fishdata.json", "r", encoding='UTF-8')
		jsondata2 = json.load(file2)
		file2.close()
		# 낚싯대 정보 불러오기
		file3 = open("fishingroddata.json", "r", encoding='UTF-8')
		jsondata3 = json.load(file3)
		file3.close()

		for food in jsondata1['foods']:
			data_dict[username]['inventory']['items'].append({"name": food['name'], "type": "food", "desc": food['desc'], "quantity": 0})
		for fish in jsondata2['fishes']:
			if(fish['available']):
				data_dict[username]['inventory']['items'].append({"name": fish['name'], "type": "fish", "desc": fish['desc'], "quantity": 0})
		for fishingrod in jsondata3['fishing_rods']:
			data_dict[username]['inventory']['fishing_rods'].append({"name": fishingrod['name'], "durability": 0, "equipped": 0, "grade": fishingrod['grade']})
		result.update({"success": True})
	dict_to_json_file(data_dict)
	return result

"""
로그인
input
{
    "username": "player1", #사용자 이름
    "password": "user_password" #사용자 비밀번호
}

output
{
	"success": true,
	"errormessage": ""
}
"""
def login(login_info: dict):
	data_dict = json_file_to_dict()
	username = login_info['username']
	password = login_info['password']
	result = {"success": False, "errormessage": ""}

	if(username in data_dict):
		if(password == data_dict[username]['password']):
			result.update({"success": True, "errormessage": ""})
		else:
			result.update({"success": False, "errormessage": "비밀번호가 일치하지 않습니다."})
	else:
		result.update({"success": False, "errormessage": "존재하지 않는 아이디입니다."})
	return result

"""
사용자 정보 불러오기
input
{
    "username": "player1"
}
output
{
	"success": true,
	"errormessage": "",
	"username": "player1",
	"price": 0,
	"inventory": {
		"slots": 10,
		"fishing_rods": [
			{
				"name": "초보자 낚시대",
				"durability": 95
			}
		],
		"fish": [
		],
		"food": [],
		"equipped": {
			"fishing_rod": "초보자 낚시대"
		}
	},
	"hunger": 95,
	"current_depth_level": "shallow",
	"game_progress": {
		"date": 0,
		"time_of_day": "morning"
	},
	"ranking": {
		"rank": 0,
		"earnings": 0
	}
}
"""
def userinfo(user_info: dict):
	data_dict = json_file_to_dict()
	username = user_info['username']
	result = {"success": False, "errormessage": ""}

	if(username in data_dict):
		result.update(data_dict[username])
		del result['password']
		result.update({"success": True, "errormessage": ""})
	else:
		result.update({"success": False, "errormessage": "존재하지 않는 아이디입니다."})
	return result
