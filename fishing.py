from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from auth.user_auth import register, login, userinfo
from core.check import check_inventory, market, leaderboard
from core.save import fished_successed_save, fished_failed_save, purchase_item, sell_fish, eat_food, change_fishing_rod
from json_util.json_io import json_data_to_dict, dict_to_json_data

server_address = ('localhost', 8080)

class FishingServer(BaseHTTPRequestHandler):
	def make_header(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
		self.send_header('Access-Control-Allow-Headers', 'Content-Type')
		self.end_headers()

	def divide_path(self) -> tuple:
		service_with_query_params = urlparse(self.path)
		servie_name = service_with_query_params.path
		query_params = parse_qs(service_with_query_params.query)

		return servie_name, query_params
	
	def do_GET(self):
		self.make_header()
		service_name, service_query = self.divide_path()
		print(service_query)
		result = {}
		# 상점 불러오기
		if(service_name == "/v1/market"):
			result = market(service_query)
		elif(service_name == "/v1/leaderboard"):
			result = leaderboard(service_query)
		if result:
			result_data = dict_to_json_data(result)
			self.wfile.write(result_data.encode('utf-8'))
	
	def do_POST(self):
		self.make_header()
		service_name, _ = self.divide_path()
		json_data = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
		print(json_data)
		dict_data = json_data_to_dict(json_data)
		result = {}

		# 회원가입
		if(service_name == "/v1/auth/new-user"):
			result = register(dict_data)
		# 로그인
		elif(service_name == "/v1/auth/login"):
			result = login(dict_data)
		# 유저 정보 조회
		elif(service_name == "/v1/game/load"):
			result = userinfo(dict_data)
		# 인벤토리 조회
		elif(service_name == "/v1/game/inventory"):
			result = check_inventory(dict_data)
		# 낚시 성공했을 때 저장
		elif(service_name == "/v1/game/success"):
			result = fished_successed_save(dict_data)
		# 낚시 실패했을 때 저장
		elif(service_name == "/v1/game/fail"):
			result = fished_failed_save(dict_data)
		# 아이템 구매했을 때 저장
		elif(service_name == "/v1/market/item/buy"):
			result = purchase_item(dict_data)
		# 물고기 팔 때 저장
		elif(service_name == "/v1/market/fish/sell"):
			result = sell_fish(dict_data)
		# 음식 먹을 때 저장
		elif(service_name == "/v1/food"):
			result = eat_food(dict_data)
		# 낚싯대 장착할 때 저장
		elif(service_name == "/v1/game/fishing_rod"):
			result = change_fishing_rod(dict_data)
		if result:
			result_data = dict_to_json_data(result)
			self.wfile.write(result_data.encode('utf-8'))
	def do_OPTIONS(self):
		self.make_header()

# POST 요청 데이터 테스트
def test_divide_path(str) -> tuple:
	service_with_query_params = urlparse(str)
	servie_name = service_with_query_params.path
	query_params = parse_qs(service_with_query_params.query)

	return servie_name, query_params

# print(test_divide_path("https://localhost:3000/v1/game/save?id=aaaa&password=bbbb"))	

print(f"서버가 {server_address[0]}:{server_address[1]}에서 열렸습니다.")
httpd = HTTPServer(server_address, FishingServer)
httpd.serve_forever()