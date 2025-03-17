from scenex import SceneXplain
sceneX = SceneXplain(api_key="KEY", api_secret="SECRET")
result = sceneX.describe(url="https://example.com/image.jpg")
print(result)