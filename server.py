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
@routes.get("/api/v1/visits")
async def api_v1_visits(req):
    row = find_first_row("GeneralInt", 1, "visits")
    datasend = {
        "visits": row[2]
    }
    return web.Response(text=json.dumps(datasend), content_type="text/json")
app.router.add_routes(routes)
if __name__ == "__main__":
    try:
        web.run_app(app)
    finally:
        db.close()