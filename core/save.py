from json_util.json_io import dict_to_json_file, json_file_to_dict
import json
import pyupbit

'''
낚시했을 때 저장
input
{
	"fishingSuccess" : true,
	"fish" : "아무물고기" #잡은 물고기
	"userId" : "player1" #유저 이름
	"equipped": { #장착한 장비
		"fishingRod": "초보자 낚시대" #낚시대
    	"durability": 95 #내구도
    }
    "hunger" : 95
}
output
{
	"success": "true" #성공 여부
	"errormessage":  #에러 메세지
}
'''

def fished_save(save_info: dict):
	data_dict = json_file_to_dict()
	fish = save_info['fish']
	username = save_info['userId']
	equipped = save_info['equipped']
	hunger = save_info['hunger']
	result = {"success": False, "errormessage": ""}
	if(username in data_dict):
		data_dict[username]['hunger'] = hunger
		i = 0
		while(i<len(data_dict[username]['inventory']['fishing_rods']) and equipped['fishingRod'] != data_dict[username]['inventory']['fishing_rods'][i]['name']):
			i += 1
		print(i)
		data_dict[username]['inventory']['fishing_rods'][i]['durability'] = equipped['durability']
		if(fish != ""):
			data_dict[username]['inventory']['fish'].append(fish)
		result.update({"success": True, "errormessage": ""})
	else:
		result.update({"success": False, "errormessage": "존재하지 않는 아이디입니다."})
	
	dict_to_json_file(data_dict)
	return result

'''
낚시하기 버튼을 클릭했을 때 저장
input
{
	"userId": "player1", #유저 이름
	"equipped": { #장착한 장비
        "fishingRod": "초보자 낚시대", #낚시대
        "durability": 95, #내구도
        "depthLevel": "shallow" #수심 레벨
    }
}
output
{
	"success": "true" #성공 여부
	"errormessage":  #에러 메세지
}
'''
def fished_clicked_save(save_info: dict):
	data_dict = json_file_to_dict()
	username = save_info['userId']
	equipped = save_info['equipped']
	result = {"success": False, "errormessage": ""}
	if(username in data_dict):
		i = 0
		while(i<len(data_dict[username]['inventory']['fishing_rods']) and equipped['fishingRod'] != data_dict[username]['inventory']['fishing_rods'][i]['name']):
			i += 1
		print(i)
		data_dict[username]['inventory']['fishing_rods'][i]['durability'] = equipped['durability']
		result.update({"success": True, "errormessage": ""})
	else:
		result.update({"success": False, "errormessage": "존재하지 않는 아이디입니다."})
	dict_to_json_file(data_dict)
	return result

'''
상점에서 아이템 샀을 때 저장
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
			i = 0
			while(i < len(jsondata2['fishing_rods']) and marketitem != jsondata2['fishing_rods'][i]['name']):
				i += 1
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
		result = {"success": False, "errormessage": "존재하지 않는 아이디입니다."}
	return result
	

'''
물고기 팔았을 때 저장
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
	# 낚싯대 정보 불러오기
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
		upbitcoinprice = pyupbit.get_current_price(jsondata1['fishes'][i]['upbit'])
		print(upbitcoinprice)
		j = 0
		while(j<len(data_dict[username]['inventory']['items']) and fishname != data_dict[username]['inventory']['items'][j]['name']):
			j += 1
		if(data_dict[username]['inventory']['items'][j]['quantity'] >= quantity):
			data_dict[username]['inventory']['items'][j]['quantity'] -= quantity
			data_dict[username]['prict'] += upbitcoinprice * quantity
		else:
			result = {"success": False, "errormessage": "수량이 부족하여 판매하지 못했습니다."}
	else:
		result = {"success": False, "errormessage": "존재하지 않는 아이디입니다."}
	return result
'''
음식 먹었을 때 저장
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
	username = saveinfo['userId']
	foodname = saveinfo['food']
	result = {"success": False, "errormessage": ""}

	if(username in data_dict):
		i = 0
		while(i<len(jsondata1['foods']) and foodname != jsondata1['foods'][i]['name']):
			i += 1

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
		result = {"success": False, "errormessage": "존재하지 않는 아이디입니다."}
	return result

'''
낚싯대 장착할 때 저장
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
		while(j < len(data_dict[username]['inventory']['fishing_rods']) and data_dict[username]['inventory']['fishing_rods'][j]['equipped'] != 1):
			j += 1
		if(data_dict[username]['inventory']['fishing_rods'][i]['durability'] > 0):
			data_dict[username]['inventory']['fishing_rods'][j]['equipped'] = 0
			data_dict[username]['inventory']['fishing_rods'][i]['equipped'] = 1
			result.update({"success": True, "errormessage": ""})
		else:
			result.update({"success": False, "errormessage": "내구도가 부족하여 낚싯대를 장착하지 못했습니다."})
		dict_to_json_file(data_dict)
	else:
		result.update({"success": False, "errormessage": "존재하지 않는 아이디입니다."})
	return result
