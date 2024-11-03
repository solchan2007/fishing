from json_util.json_io import dict_to_json_file, json_file_to_dict
import json
import pyupbit # type: ignore
import random

'''
낚시 성공했을 때 저장(구현 완료, 예외 처리 완료)
input
{
	"username": "username", // 유저 이름
}
output
{
	"success": "true" #성공 여부
	"errormessage":  #에러 메세지
}
'''

def fished_successed_save(save_info: dict):
	data_dict = json_file_to_dict()
	username = save_info['username']
	result = {"success": False, "errormessage": ""}
	if(username in data_dict):
		i = 0
		while(i < len(data_dict[username]['inventory']['fishing_rods']) and data_dict[username]['inventory']['fishing_rods'][i]['equipped'] != 1):
			i += 1
		if(i < len(data_dict[username]['inventory']['fishing_rods'])):
			# 물고기 정보 불러오기
			file1 = open("fishdata.json", "r", encoding='UTF-8')
			jsondata1 = json.load(file1)
			file1.close()
			possible_fishes = []
			if(data_dict[username]['inventory']['fishing_rods'][i]['grade'] == 'shallow'):
				for fish in jsondata1['fishes']:
					if(fish['grade'] == 'shallow' and fish['available'] == 1):
						possible_fishes.append(fish)
			elif(data_dict[username]['inventory']['fishing_rods'][i]['grade'] == 'thermocline'):
				for fish in jsondata1['fishes']:
					if(fish['grade'] == 'shallow' and fish['available'] == 1):
						possible_fishes.append(fish)
					if(fish['grade'] == 'thermocline' and fish['available'] == 1):
						possible_fishes.append(fish)
			elif(data_dict[username]['inventory']['fishing_rods'][i]['grade'] == 'deep'):
				for fish in jsondata1['fishes']:
					if(fish['grade'] == 'shallow' and fish['available'] == 1):
						possible_fishes.append(fish)
					if(fish['grade'] == 'thermocline' and fish['available'] == 1):
						possible_fishes.append(fish)
					if(fish['grade'] == 'deep' and fish['available'] == 1):
						possible_fishes.append(fish)
			
			catched_fish = possible_fishes[random.randint(0, len(possible_fishes) - 1)]
			j = 0
			while(j<len(data_dict[username]['inventory']['items']) and catched_fish['name'] != data_dict[username]['inventory']['items'][j]['name']):
				j += 1
			if(data_dict[username]['inventory']['fishing_rods'][i]['durability'] >= 5):
				data_dict[username]['hunger'] -= 5
				data_dict[username]['inventory']['fishing_rods'][i]['durability'] -= 5
				data_dict[username]['inventory']['items'][j]['quantity'] += 1
				result.update({"success": True, "errormessage": ""})
			else:
				result.update({"success": False, "errormessage": "낚싯대의 내구도가 부족하여 낚시하지 못했습니다."})
			dict_to_json_file(data_dict)
		else:
			result.update({"success": False, "errormessage": "장착된 낚싯대를 찾을 수 없습니다."})
	else:
		result.update({"success": False, "errormessage": "존재하지 않는 아이디입니다."})
	
	dict_to_json_file(data_dict)
	return result

'''
낚시 실패했을 때 저장(구현 완료, 예외 처리 완료)
input
{
	"username": "username"
}
output
{
	"success": "true" #성공 여부
	"errormessage":  #에러 메세지
}
'''
def fished_failed_save(save_info: dict):
	data_dict = json_file_to_dict()
	username = save_info['username']
	result = {"success": False, "errormessage": ""}
	if(username in data_dict):
		i = 0
		while(i < len(data_dict[username]['inventory']['fishing_rods']) and data_dict[username]['inventory']['fishing_rods'][i]['equipped'] != 1):
			i += 1
		if(i < len(data_dict[username]['inventory']['fishing_rods'])):
			if(data_dict[username]['inventory']['fishing_rods'][i]['durability'] >= 5):
				data_dict[username]['hunger'] -= 5
				data_dict[username]['inventory']['fishing_rods'][i]['durability'] -= 5
			else:
				data_dict[username]['inventory']['fishing_rods'][i]['durability'] = 0
			result.update({"success": True, "errormessage": ""})
		else:
			result.update({"success": False, "errormessage": "장착된 낚싯대를 찾을 수 없습니다."})
	else:
		result.update({"success": False, "errormessage": "존재하지 않는 아이디입니다."})
	
	dict_to_json_file(data_dict)
	return result

'''
상점에서 아이템 샀을 때 저장(구현 완료)
input
{
	"username": "username", #유저 이름
	"market_item": "아이템 이름",
	"isfood": 1
}
output
{
	"success": "true" #성공 여부
	"errormessage":  #에러 메세지
}
'''
def purchase_item(saveinfo: dict):
	data_dict = json_file_to_dict()
	# 음식 정보 불러오기
	file1 = open("fooddata.json", "r", encoding='UTF-8')
	jsondata1 = json.load(file1)
	file1.close()
	# 낚싯대 정보 불러오기
	file2 = open("fishingroddata.json", "r", encoding='UTF-8')
	jsondata2 = json.load(file2)
	file2.close()
	username = saveinfo['username']
	marketitem = saveinfo['market_item']
	isfood = saveinfo['isfood']
	result = {"success": False, "errormessage": ""}

	if(username in data_dict):
		if(isfood):
			i = 0
			while(i < len(jsondata1['foods']) and marketitem != jsondata1['foods'][i]['name']):
				i += 1
			if(i < len(jsondata1['foods'])):
				if(data_dict[username]['price'] >= jsondata1['foods'][i]['price']):
					data_dict[username]['price'] -= jsondata1['foods'][i]['price']
					j = 0
					while(j < len(data_dict[username]['inventory']['items']) and marketitem != data_dict[username]['inventory']['items'][j]['name']):
						j += 1
					data_dict[username]['inventory']['items'][j]['quantity'] += 1
					result = {"success": True, "errormessage": ""}
				else:
					result = {"success": False, "errormessage": "돈이 부족하여 구매에 실패했습니다."}
			else:
				result = {"success": False, "errormessage": "존재하지 않는 음식 이름입니다."}
		else:
			i = 0
			while(i < len(jsondata2['fishing_rods']) and marketitem != jsondata2['fishing_rods'][i]['name']):
				i += 1
			if(i < len(jsondata2['fishing_rods'])):
				if(data_dict[username]['price'] >= jsondata2['fishing_rods'][i]['price']):
					data_dict[username]['price'] -= jsondata2['fishing_rods'][i]['price']
					j = 0
					while(j < len(data_dict[username]['inventory']['fishing_rods']) and marketitem != data_dict[username]['inventory']['fishing_rods'][j]['name']):
						j += 1
					data_dict[username]['inventory']['fishing_rods'][j]['durability'] = jsondata2['fishing_rods'][i]['durability']
					result = {"success": True, "errormessage": ""}
				else:
					result = {"success": False, "errormessage": "돈이 부족하여 구매에 실패했습니다."}
			else:
				result = {"success": False, "errormessage": "존재하지 않는 낚싯대 이름입니다."}
	else:
		result = {"success": False, "errormessage": "존재하지 않는 아이디입니다."}
	dict_to_json_file(data_dict)
	return result
	

'''
물고기 팔았을 때 저장(구현 완료, 예외 처리 완료)
input
{
	"username": "username",
	"fish_name": "name",
	"quantity": 1
}
output
{
	"success": "true" #성공 여부
	"errormessage":  #에러 메세지
}
'''
def sell_fish(saveinfo: dict):
	data_dict = json_file_to_dict()
	# 물고기 정보 불러오기
	file1 = open("fishdata.json", "r", encoding='UTF-8')
	jsondata1 = json.load(file1)
	file1.close()
	username = saveinfo['username']
	fishname = saveinfo['fish_name']
	quantity = saveinfo['quantity']
	result = {"success": False, "errormessage": ""}
	
	if(username in data_dict):
		i = 0
		while(i<len(jsondata1['fishes']) and fishname != jsondata1['fishes'][i]['name']):
			i += 1
		# 코인 시세 불러오기
		upbitcoinprice = pyupbit.get_current_price(jsondata1['fishes'][i]['upbit'])
		print(upbitcoinprice)
		j = 0
		while(j < len(data_dict[username]['inventory']['items']) and fishname != data_dict[username]['inventory']['items'][j]['name']):
			j += 1
		if(j < len(data_dict[username]['inventory']['items'])):
			if(data_dict[username]['inventory']['items'][j]['quantity'] >= quantity):
				data_dict[username]['inventory']['items'][j]['quantity'] -= quantity
				data_dict[username]['price'] += upbitcoinprice * quantity
				result = {"success": True, "errormessage": ""}
			else:
				result = {"success": False, "errormessage": "수량이 부족하여 판매하지 못했습니다."}
		else:
			result = {"success": False, "errormessage": "물고기 종류를 찾을 수 없습니다."}
	else:
		result = {"success": False, "errormessage": "존재하지 않는 아이디입니다."}
	dict_to_json_file(data_dict)
	return result
'''
음식 먹었을 때 저장(구현 완료, 예외 처리 완료)
input
{
	"userId": "player1", #유저 이름
	"food": "사과", #음식
	"full": 10 #배가 차는 정도
}
output
{
	"success": "true" #성공 여부
	"errormessage":  #에러 메세지
}
'''
def eat_food(saveinfo: dict):
	data_dict = json_file_to_dict()
	# 음식 정보 불러오기
	file1 = open("fooddata.json", "r", encoding='UTF-8')
	jsondata1 = json.load(file1)
	file1.close()
	username = saveinfo['username']
	foodname = saveinfo['food_name']
	result = {"success": False, "errormessage": ""}

	if(username in data_dict):
		i = 0
		while(i<len(jsondata1['foods']) and foodname != jsondata1['foods'][i]['name']):
			i += 1
		if(i<len(jsondata1['foods'])):
			if((data_dict[username]['hunger'] + jsondata1['foods'][i]['full']) > 100):
				j = 0
				while(j<len(data_dict[username]['inventory']['items']) and foodname != data_dict[username]['inventory']['items'][j]['name']):
					j += 1
				if(data_dict[username]['inventory']['items'][j]['quantity'] > 0):
					data_dict[username]['inventory']['items'][j]['quantity'] -= 1
					data_dict[username]['hunger'] = 100
					result = {"success": True, "errormessage": ""}
				else:
					result = {"success": False, "errormessage": "수량이 부족하여 먹기에 실패하였습니다."}
			else:
				j = 0
				while(j<len(data_dict[username]['inventory']['items']) and foodname != data_dict[username]['inventory']['items'][j]['name']):
					j += 1
				if(data_dict[username]['inventory']['items'][j]['quantity'] > 0):
					data_dict[username]['inventory']['items'][j]['quantity'] -= 1
					data_dict[username]['hunger'] += jsondata1['foods'][i]['full']
					result = {"success": True, "errormessage": ""}
				else:
					result = {"success": False, "errormessage": "수량이 부족하여 먹기에 실패하였습니다."}
		else:
			result = {"success": False, "errormessage": "존재하지 않는 음식 이름입니다."}
	else:
		result = {"success": False, "errormessage": "존재하지 않는 아이디입니다."}
	dict_to_json_file(data_dict)
	return result

'''
낚싯대 장착할 때 저장(구현 완료)
input
{
	"username": "username", // 유저 이름
	"fishing_rod": "name" // 낚시대 이름
}
output
{
	"success": "true" #성공 여부
	"errormessage":  #에러 메세지
}
'''
def change_fishing_rod(saveinfo: dict):
	data_dict = json_file_to_dict()
	username = saveinfo['username']
	fishingrod = saveinfo['fishing_rod']
	result = {"success": False, "errormessage": ""}
	if(username in data_dict):
		i = 0
		while(i < len(data_dict[username]['inventory']['fishing_rods']) and fishingrod != data_dict[username]['inventory']['fishing_rods'][i]['name']):
			i += 1
		if(i < len(data_dict[username]['inventory']['fishing_rods'])):
			j = 0
			while(j < len(data_dict[username]['inventory']['fishing_rods']) and data_dict[username]['inventory']['fishing_rods'][j]['equipped'] != 1):
				j += 1
			if(data_dict[username]['inventory']['fishing_rods'][i]['durability'] > 0):
				data_dict[username]['inventory']['fishing_rods'][j]['equipped'] = 0
				data_dict[username]['inventory']['fishing_rods'][i]['equipped'] = 1
				result.update({"success": True, "errormessage": ""})
			else:
				result.update({"success": False, "errormessage": "내구도가 부족하여 낚싯대를 장착하지 못했습니다."})
		else:
			result.update({"success": False, "errormessage": "존재하지 않는 낚싯대 이름입니다."})
	else:
		result.update({"success": False, "errormessage": "존재하지 않는 아이디입니다."})
	dict_to_json_file(data_dict)
	return result
