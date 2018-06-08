from openexchangerates.exchange import Exchange

##primer uso
app_id = "0bf21ed72c2649b4a5e0f452f4fe283c"
local_dir = "~/.openexchangerates"
exchange = Exchange(local_dir, app_id)
###


exchange= Exchange()

exchange.currencies()

exchange.exchange(1000, "COP", "MXN")