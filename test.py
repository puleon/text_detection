import requests


def test_respond():
    url = "http://0.0.0.0:8088/respond"

    request_data = {"image":"./input/example-images/Example-images/ex24.jpg",
            "east":"./input/east_text_detection.pb",
            "min_confidence":0.5, "width":320, "height":320}

    result = requests.post(url, json=request_data).json()

    gold_result = "STARBUCKS COFFEE"

    assert result == gold_result, f"Got\n{result}\n, but expected:\n{gold_result}"

    print("Success")
    

if __name__ == "__main__":
    test_respond()
