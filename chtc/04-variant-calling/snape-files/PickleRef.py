import sys
from collections import defaultdict as d
from optparse import OptionParser, OptionGroup
import gzip
import pickle

# Author: Martin Kapun

#########################################################   HELP   #########################################################################
usage = """
        python %prog \
        --ref reference.fa \
        --output output
        """
parser = OptionParser(usage=usage)
helptext = """

H E L P :
_________

                                                                                                                       ##,
                                                                                                              @@@@%((#((((((((@@.
                                                                                                         .@@#(##///#####(((((((((#(%@
                                                                                                      @@&#(##(*********(##(#(#(#(#(##(((@
                                                                                                   #@@#(((((*****,/###(((((((((((((((((((((@
                                                                                                 @@((#(#(##(#(&@@@@@@(/(((((((/((((#(#(#(#(#((&
                                                                                               @@(#((((((((@.,,,,,,,,,,,,.@@/(((((#((((((((((##(&
                                                                                             /@###(#(#(#(##(/((((((//(&@%.,,,.@//((#(#(#(#(#(#(#(#.
                                                                                            @@(((((((#(((((((((((((((((((((%@.,,(@(((((((((((((((((%
                                                                                          #@(((#(##(@@/*/@@#(((((((((((((((((/@.,,%#(((#(#(#(#(#(#((/
                                                                                         @@#(((((@           .@/(((((((((((((((/@,,.&(((((((((((((((%
                                                                                        @((#(##@                @/((((((((((((((*@,,@((#(#(#(#(#(#(#(%
                                                                                      %@(((((#(#      @*         @//(////(((((((((/((((((((((((((((((@
                                                                                     @@((((#(#((                 @@.         (@/(((((#(#(#(#(#(#(#(#(%
                                                                                   .@(#(((((#((@                @               @((((((((((((((((((((#
                                                                                  @@(#(#(#(((/@/(@            @@                 ((((#(#(#(#(#(#(#(((#
                                                                                .@(##(#(/%%#///@(/(/@@.   ,@&((/        @@        @((((((((((((((((((@
                                                                               @@#(#(@(((/((/(/@@/%@@///@/((((/@                 @(#(#(#(#(#(#(#(#((#@
                                                                             .@((((&((@@&&&&@@@#((((//@/((((///(@*              @(#(((((((((((((((((%.
                                                                            @@#(((#&(@@&&&&&&@@@/@((/@/((/@%((((((/@/        ,@(#((#(#(#(#(#(#(#(#((@
                                                                          .@#(((((#%(@&&&&&&&&@@/@@@//%(/(((((((/@/((/(/*/*((((((((((((((((((((((#(&
                                                                         @@((#(#(#(@/(@&&&&&&&&@@@  ,@@#/////((((((/&@&((%@&(((#(#(#(#(#(#(#(#(#((##
                                                                        @#(((((((((/@/#@@&&&&&&&@&@@@. @@  @&  @@&@///((((((((((((((((((((((((((((@
                                                                      %@(((#(((#(#/((%#*@ @&@@&&&&&&@&&&&&&@&@@&&&&&@@@/(@(((#(#(#(#(#(#(#(#(#(((@
                                                                     @&((%%%##(((((((((&%(& ,@@@&@&&&&&@@%%#%@@&&&&&&&&&@(@(#((((((((((((((((((#@
                                                                   .@((%%%%#(((#(((((((((/@/@&  @@/@&@&&&@@&%%%%@@&&&&&@@#(@#((#(#(#(#(#(#(((#(@.
                                                                  @@#((%%%(#((((((((((((((((((//@/ @@.@@&@&@@&%%%@@&&&&&@(#%#((((((((((((((((#&,
                                                                 @(#(#(#(#(#(#(#(((((((((((((((((((/@& @   @@&#%%%@&@&@@#%&#(#(#(#(#(#(#(#(((&*
                                                               ,@(((((((((((((((((((((((((((((((((((((((//%@@@@@@@@@##(@&##((((((((((((((#((@/
                                                              @@##(((#(#(#(#(##((((((((((((((((((((((((((((((#@@@@@@%((((((#(#(#(#(#(#(#(((@,
                                                             @#(((((((((((((((((((((((((((((((((((((((((((((((((##(#(((((((((((((((((((((#@
                                                           ,@#(#(#(#(#(#(#(##((((((((((((((((((((((((((((((((#(#(#(#(#(#(#(#(#(#(#(#((((#@
                                                          @&#(((((((((((((((//(((((((((((((((((((((((((((#((((((((((((((((((((((((((((((@
                                                         @(((#(#(#(#(#(#(#(((((((((((((((((((((((((((((((#(#(#(#(#(#(#(#(#(#(#(#(#(#(((@
                                                       #@(#(((((((((((((#(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((#(@
                                                      @((((#(#(#(#(#(#(#(((((((((((((((((((((((((((((#(#(#(#(#(#(#(#(#(#(#(#(#(#(((((@
                                                    %@#(((((((((((((((#((((((((((((((((((((((((/(((((((((((((((((((((((((((((((((#(#@
                                                   @(((#(#(#(#(#(#(#(#(((((((((((((((((((((((((((((#(#(#(#(#(#(#(#(#(#(#(#(#(#(#((&%
                                                 @%((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((##@.
                                               #@(##(#(#(#(#(#(#(((((((((((((((((((((((((#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(##(@
                                             .@(((((((((((((((((#((((((((((((((((((((#(((((((((((((((((((((((((((((((((((((((#/@
                                            @(##(((((#(#(#(#(##((((((((((((((((((((((#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(((/@
                                          @%(#(%%%#(((((((((#((/(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((#(%
                                        (@#((#((#((((#(#(#(((((((((((((((((((((#(#(#(#(#(#(#(#(#(#(#(#(#(#(((###(#(#(#(#(#(%(
                                      ,@##((((((((((((((((((((((((((((((((((((#((((((((((((((((((((((((((((#%%%(##((((((((&,
                                     @(((#(#(#(#(#(#(##((((((((((((((((((((((((#(#(#(#(#(#(#(#(#(#(#(#(#((%%%%%/(#(#(#(#(@.
                                   @(#(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((//(((((((((((@
                                 @(#(#(#(#(#(#(#(#(((((((((((((((((((((((((((#(#(#(#(#(#(#(#(#(#(#(#(((#(#(#(#(#(#(#(##@
                              ,@(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((##@,
                            @((((#(#(#(#(#(#(#(#(#(((((((((((((((((((((((#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#((@
                          @(#(((((((((((((((((((((((((((((((((((((((((/(((((((((((((((((((((((((((((((((((((((((((@/
                       /@((#(#(#(#(#(#(#(#(#(#((((((((((((((((((((((((##(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(@
                     (@(((((((((((((((((((((#(((((((((((((((((((((((##(((((((((((((((((((((((((((((((((((((((((@(
                   &&#(((#(#(#(#(#(#(((#(((((((((((((((((((((((((((((#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#((@
                 (@#(((((((((((((((#%%%%#(((((((((((((((((/(((#(((((((((((((((((((((((((((((((((((((((((((((&#
               *@#(#(#(#(#(#(#(#(#/%%%%((((((((((((((((((((((#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(@
              @(((%%%%#(((((((((((#(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((#@#
            @#((%%%%%%(#(#(#(#(#(#(((((((((((((((((((((((((#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#((((@
          %&((((((%%#((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((#@(
        .@##(#(#(((((#(#(#((##((((((((((((((((((((/((#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#((((#@
       @&#((((((((((((((((##(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((@
      @((#(#(#(#(#(#(#(###(((((((((((((((((((((((#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#((/@*
     @((((((((((((((((#((((((((((((((((((((((#(((((((((((((((((((((((((((((((((((((((((((((((#(@
    @((#(#(#(#(#(#(#(##((((((((((((((((((((((#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(###@@
   @/(((((((((((((((#(/((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((#@@
  @&(#(#(#(#(#(#(#(#((((((((((((((((((##(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#((@%
  @(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((##%%%%%(((((((((((((#(##@.
 %@((#(#(#(#(#(#(#(#(((((((((((((#(#(#(#(#(#(#(#(#(#(#(#(#(#((%%%%%%%((#(#(#(#(#(#(&@
 @/#((((((((((((((((((((((((#((((((((((((((((((((((((((((((((((%%%%(##(((((((((((@%
 @(#(#(#(#(#(#(#(#(#(#(#(((#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(((#(#(#(#(#(#((#@.
 @((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((&@
 @/#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(##(@,
 /@#((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((#@@
  @((#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#((%@
   @&##(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((@/
     @%#(((#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(##@/
       %@(##(((((((((((((((((((((((((((((((((((((((((((##(#@@
           @@%(((#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(#(((#(&@@(
                (@@@#(#((((#(((((((((((((##(#/%@@@/
                         &@@@@@@@@@@@@@@@/

"""
group=OptionGroup(parser,helptext)

#########################################################   parameters   #########################################################################

parser.add_option("--ref", dest="Ref", help=" The reference genome in FASTA format")
parser.add_option("--output", dest="OUT", help="output prefix")

parser.add_option_group(group)
(options, args) = parser.parse_args()


################################### functions ######################################

def load_data(x):
  ''' import data either from a gzipped or or uncrompessed file or from STDIN'''
  import gzip
  if x=="-":
      y=sys.stdin.decode('ASCII')
  elif x.endswith(".gz"):
      y=gzip.open(x,"rt", encoding="latin-1")
  else:
      y=open(x,"r", encoding="latin-1")
  return y

############################ parse FASTA ###########################################

REFID=d(list)
ID=""
print("****** READING REF ******")
for l in load_data(options.Ref):
    if l.startswith(">"):

        ID=l.rstrip().split()[0][1:]
        print(ID+" started")
        continue

    REFID[ID].extend(list(l.rstrip()))

## write dictionary object to file
with open(options.OUT+".ref","wb") as refout:
    pickle.dump(REFID, refout)
print("****** REF PICKLED ******")

