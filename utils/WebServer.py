import web
#http://127.0.0.1:8089/visit/whatever

class WebServer(web.auto_application):
  def run(self, port, *middleware):
      func = self.wsgifunc(*middleware)
      return web.httpserver.runsimple(func, ('0.0.0.0', port))

app = WebServer()

##########################web services
class hello(app.page):
    def GET(self):
        return 'Hello,world'

class visit(app.page):
    path = '/visit/.*'
    def GET(self):
        return 'you are visiting '+web.ctx.path
##########################

def main():
    app.run(port=8089)

if __name__ == "__main__":
    main()
