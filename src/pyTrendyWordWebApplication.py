# -*- coding: utf8 -*-
import json, sys, logging
import pyUtilsClass
from pyWebAppPages import *

if __name__=="__main__":

    if len(sys.argv) < 5:
        logging.info("Argument error")
        logging.info("    Allowed argument :: [Server] [dbConfig] [host] [port] ")
        exit()

    server = sys.argv[1]
    dbConfigFile = sys.argv[2]
    host = sys.argv[3]
    port = sys.argv[4]

    dbConfig = utils.readJsonFile(utils.getLocalPath() + '/../config/' + dbConfigFile)

    setDBConnection(dbConfig[server])
    app.run(host, port, debug=True)
