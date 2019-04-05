
import csv
import os
from flask import render_template, url_for
from myproject import app
from flask_table import Table, Col


@app.route("/")
def hello():
    #users
    characters = []
    with open('characters.csv', 'r') as user_file:
        spam_reader = csv.DictReader(user_file)
        for row in spam_reader:
            characters.append(row)

    #apprearance
    appearances = []
    with open('episode_per_season.csv') as appearance_file:
         spam_reader = csv.DictReader(appearance_file)
         for row in spam_reader:
             appearances.append(row)

    # Declare my table
    class ItemTable(Table):
        border = '1px'
        name = Col('Name')
        district = Col('District')
        mothers_name = Col('Mother\'s Name')
        father_name = Col('Father\'s Name')
        date_added = Col('Date Added')
        episodes_per_season = Col('Episodes Per Season')
        died_in_season = Col('Died in Season')
        

    # Get some objects
    class Item(object):
        def __init__(self, name, district, mothers_name,father_name, date_added, episodes_per_season, died_in_season):
            self.name = name
            self.district = district
            self.mothers_name = mothers_name
            self.father_name = father_name
            self.date_added = date_added
            self.episodes_per_season = episodes_per_season
            self.died_in_season = died_in_season


    user_appearance = []
    for character in characters:
        name = character.get('name')
        character_episodes = []
        for appearance in appearances:
            if appearance.get('user') == name:
                character_episodes.append("%s Episodes in Season %s" %
                                     (appearance.get('no of episodes'), appearance.get('season')))
                if int(appearance.get('died in this season')):
                    character['Death Season'] = appearance.get('season')
        character['Episodes Per Season'] = character_episodes

    page_data = []
    for character in characters:
            data = [Item(character.get('name'), character.get('district'), character.get('mothers name') or 'Unidentified',
                    character.get('fathers name') or 'Unidentified', character.get('date registered'),
                    '<br/><hr/>'.join(character.get('Episodes Per Season')), character.get('Death Season'))
                    ]

            page_data.append(data)

    
    # Populate the table
    page = ItemTable(data)
   
   #
    return render_template('table.html', page = page)