from app import app
from unittest import TestCase
from flask import session
from boggle import Boggle


app.config['TESTING'] = True


class AppTestCase(TestCase):
    """Unit tests for app.py"""

  
    def test_homepage(self):
        """Tests data when calling homepage """
        """session settings for games_played and highest_score defined before calling homepage """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['games_played'] = 10
                session['highest_score'] = 20
            
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Boggle Game</h1>', html)
            self.assertEqual(session['games_played'], 10)
            self.assertEqual(session['highest_score'], 20)
            self.assertIn('<span id="highScore" class="ml-2">20</span>', html)
            self.assertIn('<span id="gamesPlayed" class="ml-2">10</span> ', html)
    
    
    def test_check_word(self):
        """Tests API used to check validity of word chosen by player """
        """Board defined in session prior to test being run """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['board'] = [['O', 'P', 'D', 'O', 'G'],
                                    ['R', 'E', 'A', 'H', 'Y'], 
                                    ['T', 'L', 'N', 'Q', 'G'], 
                                    ['L', 'O', 'S', 'Q', 'P'], 
                                    ['S', 'X', 'C', 'N', 'Y']
                                    ]
              
            res = client.get('/check-word?word=red')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json['result'], 'ok')
            res = client.get('/check-word?word=aardvark')
            self.assertEqual(res.json['result'], 'not-on-board')
            res = client.get('/check-word?word=does_not_exist')
            self.assertEqual(res.json['result'], 'not-word')

   
 


