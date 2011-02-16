#!/usr/bin/env python

#
# ----------------------------------------------------------------------------
# "THE CLUB-MATE LICENSE" (Revision 23.5):
# Some guys from the c3pb.de wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If you meet one of us some day, and you think
# this stuff is worth it, you can buy them a club-mate in return.
# ----------------------------------------------------------------------------
#

import os
import cherrypy
import ConfigParser
import subprocess

from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('wallhackctl', 'templates'))

links=[]
    
class Root(object):
    @cherrypy.expose
    def index(self, s=None):
        
        if s:
            try:
                x = int(s)
                if  x in range (0,5):
                    print "show: %s" % (s)
                    showScreen (s)
            except:
                # 'source' does not represent an integer
                print "incorrect value for s"
                pass

        template = env.get_template('index.html')
        return template.render(title='CTL', links=links)
        

def showScreen(x):
    screen =  "XK_%s" % (x)
    subprocess.check_call(["/home/chaos/wallhackctl/xfk", "+XK_Meta_L", screen, "-XK_Meta_L"])
    

def main():
    
    # Some global configuration; note that this could be moved into a
    # configuration file
    cherrypy.config.update({
        'server.socket_port' : 80,
	'server.socket_host' : "0.0.0.0",
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),        
    })

    rootconf = {
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    }

    links.append('<a href="?s=1">Clock</a>')
    links.append('<a href="?s=2">Slideshow</a>')
    links.append('<a href="?s=3">3</a>')


    cherrypy.tree.mount(Root(),"/",rootconf)    
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    main()
