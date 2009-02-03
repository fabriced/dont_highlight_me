# -*- coding:utf-8 -*-
###############################################################################
# DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
# Version 2, December 2004
#
# Copyright (C) 2008 Fabrice Decroix
#  Everyone is permitted to copy and distribute verbatim or modified
#  copies of this license document, and changing it is allowed as long
#  as the name is changed.
#
#      DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
# TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#      0. You just DO WHAT THE FUCK YOU WANT TO. (but highlight me)
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.
#
###############################################################################

import string
from time import time
import weechat

weechat.register("dont_highlight_me", "0.2", "", "")

# période du vacuum
VACUUM_DELAY = 5
# temps avant lequel un user interdit n'highlightera pas
PREVENT_DELAY = 30

people_not_allowed_to_hl = []
timer_dict = {}


def get_host(masque):
  """ """
  host = masque.split('@')[1]
  return host


def highlight_checker(serveur, args):
  null, channel, message = string.split(args, ":", 2)
  mask, null, channel = string.split(string.strip(channel), " ", 2)
  my_nick = weechat.get_info("nick", serveur)
  message_list = message.split()

  if get_host(mask) in people_not_allowed_to_hl:
    if message_list[0].strip(':,') == my_nick and len(message_list) > 1:
      if timer_dict.has_key(mask):
        timer_dict[mask] = int(time()) + PREVENT_DELAY
        return ":%s PRIVMSG %s :%s" % (mask, channel, " ".join(message_list[1:]))
      else:
        timer_dict[mask] = int(time()) + PREVENT_DELAY
  return args


def no_hl_list(serveur, args):
  """ to know who does not hl """
  weechat.prnt(" ")
  weechat.prnt("Liste des gens qui vont pas me highlighter :")
  for b in people_not_allowed_to_hl:
    weechat.prnt("*  \x02%s\x02   " % b)
  weechat.prnt("Fin de liste.")
  weechat.prnt(" ")
  return weechat.PLUGIN_RC_OK


def no_hl_add(serveur, args):
  """ prevent hl from a host """
  people_not_allowed_to_hl.append(args)
  weechat.prnt("%s est ajouté a la liste." % args)
  weechat.prnt(" ")
  return weechat.PLUGIN_RC_OK


def no_hl_remove(serveur, args):
  """ allow a host to hl when he wants to """
  if args in people_not_allowed_to_hl:
    people_not_allowed_to_hl.remove(args)
  weechat.prnt(" ")
  weechat.prnt("\x02%s\x02 peut a nouveau highlighter" % args)
  weechat.prnt(" ")
  return weechat.PLUGIN_RC_OK


def vacuum():
  to_be_removed = []
  t = int(time())
  for k,v in timer_dict.iteritems():
    if v < t:
      to_be_removed.append(k)
  for key in to_be_removed:
    del timer_dict[key]
  return weechat.PLUGIN_RC_OK


weechat.add_modifier("irc_in", "PRIVMSG", "highlight_checker")
weechat.add_command_handler("no_hl_add", "no_hl_add")
weechat.add_command_handler("no_hl_remove", "no_hl_remove")
weechat.add_command_handler("no_hl_list", "no_hl_list")
weechat.add_timer_handler(VACUUM_DELAY, 'vacuum')
