from aiohttp import web
import json
import sqlite3
db = sqlite3.connect("data.db")
app = web.Application()
routes = web.RouteTableDef()
cache = {}
with open("index.html", "rt") as indexpage:
    cache["index"] = indexpage.read()
    indexpage.close()
with open("visits.html", "rt") as visitspage:
    cache["visits"] = visitspage.read()
    visitspage.close()
with open("dataint.html", "rt") as datapage:
    cache["dataint"] = datapage.read()
    datapage.close()
with open("dataint.js", "rt") as datascript:
    cache["datascript"] = datascript.read()
    datascript.close()
def find_first_row(table, column, equals):
    cursor = db.execute("SELECT * FROM " + table)
    for row in cursor:
        if row[column] == equals:
            return row
@routes.get("/")
async def root(req):
    return web.Response(text=cache["index"], content_type="text/html")
@routes.get("/visits")
async def visits(req):
    row = find_first_row("GeneralInt", 1, "visits")
    visitscpy = row[2]
    res = web.Response(text=cache["visits"].format(str(visitscpy)), content_type="text/html")
    visitscpy += 1
    db.execute("UPDATE GeneralInt SET value=" + str(visitscpy) + " WHERE key=\"visits\"")
    db.commit()
    return res
@routes.get("/dataint")
async def dataint(req):
    row = find_first_row("GeneralInt", 1, "data")
    return web.Response(text=cache["dataint"].format(str(row[2])), content_type="text/html")
@routes.get("/scripts/dataint.js")
async def scripts_dataint(req):
    return web.Response(text=cache["datascript"], content_type="text/javascript")
@routes.get("/api/v1/visits")
async def api_v1_visits(req):
    row = find_first_row("GeneralInt", 1, "visits")
    datasend = {
        "visits": row[2]
    }
    return web.Response(text=json.dumps(datasend), content_type="text/json")
@routes.get("/api/v1/data/increase")
async def api_v1_data_increase(req):
    try:
        row = find_first_row("GeneralInt", 1, "data")
        datacpy = row[2]
        datacpy += 1
        db.execute("UPDATE GeneralInt SET value=" + str(datacpy) + " WHERE key=\"data\"")
        db.commit()
        status = {
            "success": True
        }
        return web.Response(text=json.dumps(status), content_type="text/json")
    except:
        status = {
            "success": False
        }
        return web.Response(text=json.dumps(status), content_type="text/json")
@routes.get("/api/v1/data/decrease")
async def api_v1_data_decrease(req):
    try:
        row = find_first_row("GeneralInt", 1, "data")
        datacpy = row[2]
        datacpy -= 1
        db.execute("UPDATE GeneralInt SET value=" + str(datacpy) + " WHERE key=\"data\"")
        db.commit()
        status = {
            "success": True
        }
        return web.Response(text=json.dumps(status), content_type="text/json")
    except:
        status = {
            "success": False
        }
        return web.Response(text=json.dumps(status), content_type="text/json")
app.router.add_routes(routes)
if __name__ == "__main__":
    try:
        web.run_app(app)
    finally:
        db.close()