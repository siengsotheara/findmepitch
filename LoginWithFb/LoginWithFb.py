import facebook

app_id='159985207843693'
at='7b111fdeb43cf6889725a849013d387c'
v='2.7'

graph = facebook.GraphAPI(access_token=at, version=v)


print facebook.FACEBOOK_GRAPH_URL
print facebook.version.__version__

