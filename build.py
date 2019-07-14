# a quick hack for building .ftl archives from tiny modules

from os.path import isdir, join
from shutil import copy2, copystat, Error, copytree, ignore_patterns

import os
import fnmatch
import shutil
import zlib
import xml.etree.ElementTree as ET

#########################################
# Parameters
Prefix = 'w_'
Output = 'Vicious Vessels' # aka mod title
ForumLink = 'https://subsetgames.com/forum/viewtopic.php?f=11&t=33380'
AlternateLinks = ['https://github.com/woonaftl/vicious-vessels']
Release = '10.1'
ProjectDesc = "A modification which adds more enemy ships to FTL: \
Advanced Edition without changing the vanilla experience too much or \
disrupting balance.\n\nThe mod is NOT compatible with other overhaul mods \
such as:\nCaptain's Edition\nCaptain's Remix\nStation's Job \
or others\n\nIf you want to contribute to the mod, fork the project or \
use assets in your own mod, follow the Github link. Everyone is welcome!"
ProtectedXML = ( 
    'achievements.xml', 
    'anaerobic_bomber.xml', 
    'anaerobic_cruiser.xml', 
    'anaerobic_cruiser_2.xml', 
    'anaerobic_scout.xml', 
    'animations.xml', 
    'autoBlueprints.xml', 
    'auto_assault.xml', 
    'auto_basic.xml', 
    'blueprints.xml', 
    'bosses.xml', 
    'boss_1.xml', 
    'boss_1_easy.xml', 
    'boss_2.xml', 
    'boss_2_easy.xml', 
    'boss_3.xml', 
    'boss_3_easy.xml', 
    'circle_bomber.xml', 
    'circle_cruiser.xml', 
    'circle_cruiser_2.xml', 
    'circle_cruiser_3.xml', 
    'circle_scout.xml', 
    'crystal_bomber.xml', 
    'crystal_cruiser.xml', 
    'crystal_cruiser_2.xml', 
    'crystal_scout.xml', 
    'dlcAnimations.xml', 
    'dlcBlueprints.xml', 
    'dlcBlueprintsOverwrite.xml', 
    'dlcEvents.xml', 
    'dlcEventsOverwrite.xml', 
    'dlcEvents_anaerobic.xml', 
    'dlcPirateBlueprints.xml', 
    'dlcSounds.xml', 
    'energy_bomber.xml', 
    'energy_bomber_pirate.xml', 
    'energy_cruiser.xml', 
    'energy_cruiser_2.xml', 
    'energy_cruiser_3.xml', 
    'energy_fighter.xml', 
    'energy_fighter_pirate.xml', 
    'events.xml', 
    'events_boss.xml', 
    'events_crystal.xml', 
    'events_engi.xml', 
    'events_fuel.xml', 
    'events_imageList.xml', 
    'events_mantis.xml', 
    'events_nebula.xml', 
    'events_pirate.xml', 
    'events_rebel.xml', 
    'events_rock.xml', 
    'events_ships.xml', 
    'events_slug.xml', 
    'events_zoltan.xml', 
    'fed_bomber.xml', 
    'fed_cruiser.xml', 
    'fed_cruiser_2.xml', 
    'fed_cruiser_3.xml', 
    'fed_scout.xml', 
    'jelly_button.xml', 
    'jelly_button_pirate.xml', 
    'jelly_croissant.xml', 
    'jelly_croissant_pirate.xml', 
    'jelly_cruiser.xml', 
    'jelly_cruiser_2.xml', 
    'jelly_cruiser_3.xml', 
    'jelly_truffle.xml', 
    'jelly_truffle_pirate.xml', 
    'kestral.xml', 
    'kestral_2.xml', 
    'kestral_3.xml', 
    'mantis_bomber.xml', 
    'mantis_bomber_pirate.xml', 
    'mantis_cruiser.xml', 
    'mantis_cruiser_2.xml', 
    'mantis_cruiser_3.xml', 
    'mantis_fighter.xml', 
    'mantis_fighter_pirate.xml', 
    'mantis_scout.xml', 
    'mantis_scout_pirate.xml', 
    'nameEvents.xml', 
    'names.xml', 
    'newEvents.xml', 
    'rebel_long.xml', 
    'rebel_long_pirate.xml', 
    'rebel_squat.xml', 
    'rebel_squat_pirate.xml', 
    'rock_assault.xml', 
    'rock_cruiser.xml', 
    'rock_cruiser_2.xml', 
    'rock_cruiser_3.xml', 
    'rock_fight.xml', 
    'rock_fight_pirate.xml', 
    'rock_scout.xml', 
    'rock_scout_pirate.xml', 
    'rooms.xml', 
    'sector_data.xml', 
    'sounds.xml', 
    'stealth.xml', 
    'stealth_2.xml', 
    'stealth_3.xml', 
    'text-de.xml', 
    'text-es.xml', 
    'text-fr.xml', 
    'text-it.xml', 
    'text-pl.xml', 
    'text-pt.xml', 
    'text-ru.xml', 
    'text-zh-Hans.xml', 
    'text_achievements.xml', 
    'text_blueprints.xml', 
    'text_events.xml', 
    'text_misc.xml', 
    'text_sectorname.xml', 
    'text_tooltips.xml', 
    'text_tutorial.xml', 
    'tutorial.xml'
    )
#########################################
# copying fuctions from stackoverflow

def include_patterns(*patterns):
    """ Function that can be used as shutil.copytree() ignore parameter that
    determines which files *not* to ignore, the inverse of "normal" usage.

    This is a factory function that creates a function which can be used as a
    callable for copytree()'s ignore argument, *not* ignoring files that match
    any of the glob-style patterns provided.

    ‛patterns’ are a sequence of pattern strings used to identify the files to
    include when copying the directory tree.

    Example usage:

        copytree(src_directory, dst_directory,
                 ignore=include_patterns('*.sldasm', '*.sldprt'))
    """
    def _ignore_patterns(path, all_names):
        # Determine names which match one or more patterns (that shouldn't be
        # ignored).
        keep = (name for pattern in patterns
                        for name in fnmatch.filter(all_names, pattern))
        # Ignore file names which *didn't* match any of the patterns given that
        # aren't directory names.
        dir_names = (name for name in all_names if isdir(join(path, name)))
        return set(all_names) - set(keep) - set(dir_names)

    return _ignore_patterns

def copytree_multi(src, dst, symlinks=False, ignore=None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    # -------- E D I T --------
    # os.path.isdir(dst)
    if not os.path.isdir(dst):
        os.makedirs(dst)
    # -------- E D I T --------

    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree_multi(srcname, dstname, symlinks, ignore)
            else:
                copy2(srcname, dstname)
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        except Error as err:
            errors.extend(err.args[0])
    try:
        copystat(src, dst)
    except WindowsError:
        pass
    except OSError as why:
        errors.extend((src, dst, str(why)))
    if errors:
        raise Error(errors)

def appendxml(src, dst):
    with open(src, 'r', encoding = 'utf8') as srcfile:
        with open(dst, 'a', encoding = 'utf8') as dstfile: 
            for line in srcfile:
                if line.strip('\n').lower() != '<?xml version="1.0" encoding="utf-8"?>':
                    dstfile.write(line)


#########################################
# main

# clean up
if os.path.isdir(Output):
    shutil.rmtree(Output)

# init
authorslist = []
changelist = []
Err = []
TopFolders = []

# scanning folder
for i in os.listdir():
    if i[:len(Prefix)] == Prefix and os.path.isdir(i):
        TopFolders.append(i)

# copying stuff
os.makedirs(os.path.join(Output, 'data'))

for i in sorted(TopFolders):
    HasMetadata = False
    for j in os.listdir(i):
        jPath = os.path.join(i, j)
        jPathOut = os.path.join(Output, j)
        if j == 'img' and os.path.isdir(jPath):
            copytree_multi(jPath, jPathOut, ignore = include_patterns('*.png'))
        elif j == 'audio' and os.path.isdir(jPath):
            copytree_multi(jPath, jPathOut, ignore = include_patterns('*.ogg', '*.wav'))
        elif j == 'fonts' and os.path.isdir(jPath):
            copytree_multi(jPath, jPathOut, ignore = include_patterns('*.font', '*.ttf'))
        elif j == 'data' and os.path.isdir(jPath):
            for k in os.listdir(jPath):
                kPath = os.path.join(jPath, k)
                kPathOut = os.path.join(jPathOut, k)
                if k[-4:] == '.txt' and os.path.isfile(kPath):
                    shutil.copy2(kPath, kPathOut)
                elif k[-4:] == '.xml' and os.path.isfile(kPath):
                    if not k in ProtectedXML:
                        appendxml(kPath, kPathOut)
                    else:
                        Err.append(kPath + ' is a protected .xml file. Use .append.')
                elif k[-11:] == '.xml.append' and os.path.isfile(kPath):
                    appendxml(kPath, kPathOut)
                elif not os.path.isfile(kPath):
                    Err.append(kPath + ' is not a file.')
                else:
                    Err.append(kPath + ' is a file with wrong extension.')
        elif j == 'metadata.xml' and os.path.isfile(jPath):
            HasMetadata = True
            tree = ET.parse(jPath)
            root = tree.getroot()
            for author in root.findall('author'):
                if author.text not in authorslist:
                    authorslist.append(author.text)
            for change in root.findall('changelog'):
                changelist.append(change.text)
        else:
            Err.append(jPath + ' should not be there.')
    if HasMetadata == False:
        Err.append(i + ' has no metadata.')

# adding headers to xml files
for i in os.listdir(os.path.join(Output, 'data')):
    iPath = os.path.join(Output, 'data', i)
    if (i[-4:] == '.xml' and os.path.isfile(iPath)) or \
       (i[-11:] == '.xml.append' and os.path.isfile(iPath)):
        with open(iPath, 'r+', encoding = 'utf8') as xmlfile: 
            content = xmlfile.read()
            xmlfile.seek(0, 0)
            xmlfile.write('<?xml version="1.0" encoding="utf-8"?>\n' + content)

# preparing metadata
authorstext = ''
for i, authorname in enumerate(sorted(authorslist)):
    authorstext = authorstext + authorname
    if i < len(authorslist) - 1:
        authorstext = authorstext + ', '

ModDesc = ''

for url in AlternateLinks:
    ModDesc = ModDesc + url + '\n\n'

ModDesc = ModDesc + '\n' + ProjectDesc + '\n\nTHANKS FOR PLAYING\n\nFULL CHANGELOG\n'

for i in changelist:
    ModDesc = ModDesc + i + '\n\n'

# writing metadata (without CDATA but whatever)
os.makedirs(os.path.join(Output, 'mod-appendix'))
metadata = ET.Element('metadata')
ET.SubElement(metadata, 'title').text = Output
ET.SubElement(metadata, 'threadUrl').text = ForumLink
ET.SubElement(metadata, 'author').text = authorstext
ET.SubElement(metadata, 'version').text = Release
ET.SubElement(metadata, 'description').text = ModDesc
tree = ET.ElementTree(metadata)
tree.write(os.path.join(Output, 'mod-appendix', 'metadata.xml'))

# archiving
shutil.make_archive(Output, 'zip', Output)
shutil.rmtree(Output)
os.rename(Output + '.zip', Output + ' ' + Release + '.ftl')

print(Err)
