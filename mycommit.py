#!/usr/bin/python3

import logging
from systemd import journal
from zypp_plugin import Plugin
import json

logger = logging.getLogger(__name__)
logger.addHandler(journal.JournalHandler())

class MyPlugin(Plugin):

  def PLUGINBEGIN(self, headers, body):
    logging.info("here bo starts:")
    logging.info(headers)
    self.ack()

  def COMMITBEGIN(self, headers, body):

      logging.info("COMMITBEGIN by bo")
      tmp = json.loads(body)
      tsl = tmp["TransactionStepList"]
      for ts in tsl:
          if "+" in ts["type"]:
            logging.info(ts["solvable"]["n"])
            logger.info("Software installation: %s" % ts["solvable"]["n"])
          if "-" in ts["type"]:
            logging.info(ts["solvable"]["n"])
            logger.info("Software uninstallation: %s" % ts["solvable"]["n"])
      self.ack()

  def COMMITEND(self, headers, body):
      logging.info("COMMITEND by bo")
      self.ack() 
        
  def PLUGINEND(self, headers, body):
    self.ack()

plugin = MyPlugin()
plugin.main()
