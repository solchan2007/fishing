from json_util.json_io import dict_to_json_file, json_file_to_dict
import json
import pyupbit # type: ignore

"""
인벤토리 조회(구현 완료)
input
{
	"username": "new_user", #사용자 이름
}
output
{
	"success" : true, #성공 여부
	"errormessage" :  #에러 메세지
	"items": {
		{"name": "아이템이름", "type": "아이템 타입", "desc": "이 아이템은 어쩌고.", "quantity": 10}
	}
}
"""
def check_inventory(check_info: dict):
	data_dict = json_file_to_dict()
	username = check_info['username']
	result = {"success": False, "errormessage": ""}
	if(username in data_dict):
		result['items'] = data_dict[username]['inventory']['items']
		result.update({"success": True, "errormessage": ""})
	else:
		result.update({"success": False, "errormessage": "존재하지 않는 아이디입니다."})
		
	return result

'''
상점 조회(구현 완료, 물고기 10개 이하 조건 추가 완료)
input
{
	"username": "username",
	"fishes": [
		"name",
		"name"
	]
}
output
{
	"success": true
	"fishes": [
		{"name": "name", "price": 2000}, // 검색한것에 대해서만 출력
		{"name": "name", "price": 2000},
	]
}
'''
def market(check_info: dict):
	# 물고기 정보 불러오기
	file1 = open("fishdata.json", "r", encoding='UTF-8')
	jsondata1 = json.load(file1)
	file1.close()
	fishes = check_info['fishes']
	result = {"success": False, "errormessage": ""}

	load_fishes = []
	available_check_fish = 10
	for fish in fishes:
		i = 0
		while(i < len(jsondata1['fishes']) and fish != jsondata1['fishes'][i]['name']):
			i += 1
		if(i < len(jsondata1['fishes']) and available_check_fish > 0):
			available_check_fish -= 1
			# 코인 시세 불러오기
			upbitcoinprice = pyupbit.get_current_price(jsondata1['fishes'][i]['upbit'])
			print(f'{jsondata1['fishes'][i]['upbit']} 가격: {upbitcoinprice}')
			load_fishes.append({"name": jsondata1['fishes'][i]['name'], "price": upbitcoinprice})
	result.update({"success": True, "errormessage": "", "fishes": load_fishes})
	return result

'''
리더보드(구현 완료)
input
{
	"username": "username",
}
output
{
	"rank": 2, // 검색한 유저의 랭킹
	"ranking": [
		{"username": "username", "score": 1000}, // 랭킹 순서대로
		{"username": "username", "score": 1000},
		{"username": "username", "score": 1000},
		{"username": "username", "score": 1000},
	]
}
'''
def leaderboard(check_info: dict):
	data_dict = json_file_to_dict()
	username = check_info['username'][0]
	ranking = []
	result = {"success": False, "errormessage": ""}
	for name in data_dict.keys():
		ranking.append({"username": name, "score": data_dict[name]['price']})
	
	for i in range(len(ranking)):
		for j in range(i, len(ranking)):
			if(ranking[i]['score'] < ranking[j]['score']):
				ranking[i], ranking[j] = ranking[j], ranking[i]
	
	for i in range(len(ranking)):
		data_dict[ranking[i]['username']]['ranking'] = i + 1
	dict_to_json_file(data_dict)
	if(username in data_dict):
		result.update({"success": True, "errormessage": "", "rank": data_dict[username]['ranking'], "ranking": ranking})
	else:
		result.update({"success": False, "errormessage": "검색하신 유저가 존재하지 않습니다.", "rank": 0, "ranking": ranking})
	return result
