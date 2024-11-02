from json_util.json_io import dict_to_json_file, json_file_to_dict

"""
인벤토리 조회
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