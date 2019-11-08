import facebook

ACCESS_TOKEN = 'EAAdSXUehRmABAPlnCfxvZBSLZArlIStu5zZCU8nSWhlnk2NoYZBRL2eNZBPn5Q96dHuS2eWoGXxwWeWb7WOqZCimepqFmPjZB9hkbzzVdss2Up3JtlN8JuQKZCXtFdz7lrsau4NcGf68axe0fxwRtdPJe7onpfwTf9FS60cUmZAs9TgZDZD'
MY_FB_ID = '1030515980443558'
QUERY_BOT_FB_ID = '304335633462541'

graph = facebook.GraphAPI(access_token= ACCESS_TOKEN, version= '2.10')

# places = graph.search(type = 'place',
#                       q = 'New York',
#                       fields = 'name,location')
# for place in places['data']:
#     print('{0} {1}'.format(place['name'], place['location'].get('zip')))


def get_access_token(fb_id):
    pages_data = graph.get_object("/me/accounts")  # -> return the info of all the page I'm the admin
    for page in pages_data['data']:
        if page['id'] == fb_id:
            return page['access_token']
    return None

get_access_token(QUERY_BOT_FB_ID)
info = graph.get_object(id = QUERY_BOT_FB_ID)
feed = graph.get_object("/me/name")
print(feed)
