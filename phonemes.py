#!/usr/bin/env python

import subprocess, sqlite3

__all__ = [ 'get_phonemes' ]


db = sqlite3.connect('phonemes.db')
cur = db.cursor()
cur.execute(
  'CREATE TABLE IF NOT EXISTS '
  'Phonemes(Word TEXT PRIMARY KEY, Phonemes TEXT)')


def ask_espeak(word):
  out = subprocess.check_output(
    [ 'espeak', '-q', '-v', 'greek', '--ipa=3', word ])
  return tuple(out.decode('utf-8').strip().split(u'_'))


def ask_cache(word):
  cur = db.cursor()
  cur.execute('SELECT Phonemes FROM Phonemes WHERE Word = ?', (word,))
  row = cur.fetchone()
  return tuple(row[0].split(u'_')) if row is not None else None


def update_cache(word, phonemes):
  cur = db.cursor()
  cur.execute('INSERT INTO Phonemes VALUES (?, ?)', (word, u'_'.join(phonemes)))
  db.commit()


def get_phonemes(word):
  '''
  Breaks `word` into a tuple of phonemes. This expects `word` to already have
  been canonicalized.
  '''
  
  if isinstance(word, str):
    word = word.decode('utf-8')
  
  phonemes = ask_cache(word)
  if phonemes is None:
    phonemes = ask_espeak(word)
    update_cache(word, phonemes)
  return phonemes
